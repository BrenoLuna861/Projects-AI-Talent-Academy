"""Avaliação no período de teste + backtest com vários cortes.

    python -m src.models.evaluate

Todas as métricas são calculadas no preço (US$), não no log-retorno, para
ficarem legíveis no dashboard.
"""
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

from src.config import ARQUIVO_MODELAGEM, ARQUIVO_PRECOS, FIM_TREINO, MODELS_DIR, POWERBI_DIR, garantir_pastas
from src.models import series_temporais
from src.models.train_model import (
    BASELINES,
    FEATURES,
    criar_modelos,
    separar_treino_teste,
)
from src.utils.logger import get_logger

log = get_logger(__name__)

# Cortes extras para ver se o resultado se sustenta em outros anos.
# Cada um testa os 12 meses-base seguintes.
CORTES_BACKTEST = ["2021-12-01", "2022-12-01", "2023-12-01"]


def prever_todos(teste: pd.DataFrame, modelos: dict, precos: pd.DataFrame | None = None, corte=None) -> pd.DataFrame:
    """Uma linha por (série, mês-base, modelo) com o preço previsto.

    Com `precos` e `corte`, inclui também os modelos clássicos (SARIMA e ETS)
    e a combinação gradient boosting + SARIMA (média das duas previsões).
    """
    saidas = []
    previsoes = {nome: f(teste) for nome, f in BASELINES.items()}
    for nome, modelo in modelos.items():
        previsoes[nome] = modelo.predict(teste[FEATURES])
    if precos is not None:
        for metodo in series_temporais.METODOS:
            previsoes[metodo] = series_temporais.prever_variacao(precos, teste, corte, metodo)
            log.info("%s: %s previsões", metodo, len(teste))
        if "gradient_boosting" in previsoes:
            previsoes["combinado"] = (previsoes["gradient_boosting"] + previsoes["sarima"]) / 2

    for nome, ret in previsoes.items():
        s = teste[["serie_id", "item", "categoria", "data_base", "data_alvo", "preco", "preco_alvo"]].copy()
        s["modelo"] = nome
        s["preco_previsto"] = (s["preco"] * np.exp(ret)).round(3)
        saidas.append(s)

    out = pd.concat(saidas, ignore_index=True).rename(
        columns={"preco": "preco_base", "preco_alvo": "preco_real"}
    )
    out["erro"] = out["preco_previsto"] - out["preco_real"]
    out["erro_abs"] = out["erro"].abs()
    out["erro_pct"] = out["erro"] / out["preco_real"] * 100
    return out


def calcular_metricas(prev: pd.DataFrame) -> pd.DataFrame:
    g = prev.groupby("modelo")
    m = pd.DataFrame(
        {
            "mae_usd": g["erro_abs"].mean(),
            "mape": g["erro_pct"].apply(lambda s: s.abs().mean()),
            "wape": g.apply(lambda d: d["erro_abs"].sum() / d["preco_real"].sum() * 100, include_groups=False),
            "vies_pct": g["erro_pct"].mean(),
        }
    )
    if "ingenuo" in m.index:
        m["ganho_vs_ingenuo_pct"] = (1 - m["wape"] / m.loc["ingenuo", "wape"]) * 100

        # em quantas séries o modelo erra menos que o ingênuo
        por_serie = prev.groupby(["modelo", "serie_id"])["erro_abs"].mean().unstack("modelo")
        m["series_melhor_que_ingenuo_pct"] = (
            por_serie.lt(por_serie["ingenuo"], axis=0).mean() * 100
        )
        m.loc["ingenuo", "series_melhor_que_ingenuo_pct"] = np.nan
    return m.round(3).reset_index()


def metricas_por_grupo(prev: pd.DataFrame, coluna: str) -> pd.DataFrame:
    g = prev.groupby([coluna, "modelo"])
    return pd.DataFrame(
        {
            "mape": g["erro_pct"].apply(lambda s: s.abs().mean()),
            "wape": g.apply(lambda d: d["erro_abs"].sum() / d["preco_real"].sum() * 100, include_groups=False),
            "n": g.size(),
        }
    ).round(3).reset_index()


def backtest(base: pd.DataFrame, precos: pd.DataFrame, cortes=CORTES_BACKTEST) -> pd.DataFrame:
    resultados = []
    for corte in cortes:
        treino, teste = separar_treino_teste(base, corte)
        fim_janela = pd.Timestamp(corte) + pd.DateOffset(months=12)
        teste = teste[teste["data_base"] < fim_janela]

        modelos = criar_modelos()
        for modelo in modelos.values():
            modelo.fit(treino[FEATURES], treino["alvo"])
        m = calcular_metricas(prever_todos(teste, modelos, precos, corte))
        m.insert(0, "corte", corte)
        resultados.append(m)
        log.info("Backtest corte %s: %s linhas de teste", corte, len(teste))
    return pd.concat(resultados, ignore_index=True)


def main() -> None:
    garantir_pastas()
    teste = pd.read_parquet(MODELS_DIR / "conjunto_teste.parquet")
    modelos = {nome: joblib.load(MODELS_DIR / f"{nome}.joblib") for nome in criar_modelos()}

    precos = pd.read_parquet(ARQUIVO_PRECOS)
    prev = prever_todos(teste, modelos, precos, FIM_TREINO)
    metricas = calcular_metricas(prev)
    metricas.insert(0, "corte", FIM_TREINO)
    log.info("Teste principal (corte %s):\n%s", FIM_TREINO, metricas.to_string(index=False))

    base = pd.read_parquet(ARQUIVO_MODELAGEM)
    bt = backtest(base, precos)
    todas = pd.concat([bt, metricas], ignore_index=True)
    todas["data_execucao"] = datetime.now().isoformat(timespec="seconds")

    prev.to_csv(POWERBI_DIR / "previsoes_teste.csv", index=False)
    todas.to_csv(POWERBI_DIR / "metricas_modelos.csv", index=False)
    metricas_por_grupo(prev, "categoria").to_csv(POWERBI_DIR / "metricas_por_categoria.csv", index=False)
    metricas_por_grupo(prev, "serie_id").to_csv(POWERBI_DIR / "metricas_por_item.csv", index=False)
    log.info("Arquivos de avaliação salvos em data/processed/powerbi/")


if __name__ == "__main__":
    main()
