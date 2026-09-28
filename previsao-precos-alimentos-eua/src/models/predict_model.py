"""Previsão para os próximos meses + exportação das tabelas do Power BI.

    python -m src.models.predict_model

O modelo final é o de menor WAPE médio considerando todos os cortes do
backtest (não só o teste principal), e é retreinado com todo o histórico.
Pode ser um modelo de ML, um clássico (SARIMA/ETS) ou a combinação dos dois.
"""
import numpy as np
import pandas as pd

from src.config import (
    ARQUIVO_ITENS,
    ARQUIVO_MODELAGEM,
    ARQUIVO_PRECOS,
    HORIZONTE,
    POWERBI_DIR,
    garantir_pastas,
)
from src.features.analise_series import forcas
from src.features.build_features import linhas_para_previsao, linhas_utilizaveis
from src.models import series_temporais
from src.models.train_model import BASELINES, FEATURES, criar_modelos
from src.utils.logger import get_logger

log = get_logger(__name__)


def escolher_modelo(metricas: pd.DataFrame) -> str:
    candidatos = metricas[~metricas["modelo"].isin(BASELINES)]
    media = candidatos.groupby("modelo")["wape"].mean().sort_values()
    log.info("WAPE médio nos cortes:\n%s", media.round(3).to_string())
    return media.index[0]


def prever_variacao_futura(nome: str, base: pd.DataFrame, precos: pd.DataFrame, futuro: pd.DataFrame) -> np.ndarray:
    """Variação prevista (log) do mês-base de `futuro` até mês-base + HORIZONTE."""
    partes = ["gradient_boosting", "sarima"] if nome == "combinado" else [nome]
    rets = []
    for parte in partes:
        if parte in series_temporais.METODOS:
            r = []
            for _, linha in futuro.iterrows():
                y = series_temporais.serie_log(precos, linha["serie_id"])
                y = y[y.index <= linha["data_base"]]
                media, _, _ = series_temporais.prever_futuro(y, parte)
                r.append(media - y.iloc[-1])
            rets.append(np.array(r))
        else:
            treino = linhas_utilizaveis(base)
            modelo = criar_modelos()[parte]
            modelo.fit(treino[FEATURES], treino["alvo"])
            rets.append(modelo.predict(futuro[FEATURES]))
    return np.mean(rets, axis=0)


def faixas_de_erro(prev_teste: pd.DataFrame, modelo: str) -> pd.DataFrame:
    """Quantis 10% e 90% de (real / previsto) no teste, por categoria.

    Com faixa única, aves (que quase não mexe) e energia ficariam com a
    mesma incerteza. Categoria com menos de 12 linhas no teste usa a geral.
    """
    d = prev_teste[prev_teste["modelo"] == modelo]
    razao = d["preco_real"] / d["preco_previsto"]
    geral = razao.quantile([0.10, 0.90]).to_numpy()

    faixas = razao.groupby(d["categoria"]).quantile([0.10, 0.90]).unstack()
    faixas.columns = ["q10", "q90"]
    poucos = d.groupby("categoria").size() < 12
    faixas.loc[poucos[poucos].index] = geral
    return faixas


def exportar_dimensoes() -> None:
    itens = pd.read_parquet(ARQUIVO_ITENS)
    precos = pd.read_parquet(ARQUIVO_PRECOS).sort_values(["serie_id", "data"])

    lp = np.log(precos["preco"])
    precos["var_mensal"] = lp.groupby(precos["serie_id"]).diff()
    vol = precos.groupby("serie_id")["var_mensal"].std().mul(100).round(2)
    itens["vol_mensal_pct"] = itens["serie_id"].map(vol)

    # força de tendência e sazonalidade (STL), só para as séries modeladas
    modeladas = itens.loc[itens["motivo_exclusao"].isna(), "serie_id"]
    f = {sid: forcas(precos.loc[precos["serie_id"] == sid].set_index("data")["preco"].asfreq("MS")) for sid in modeladas}
    itens["forca_tendencia"] = itens["serie_id"].map(lambda s: f.get(s, (None, None))[0])
    itens["forca_sazonalidade"] = itens["serie_id"].map(lambda s: f.get(s, (None, None))[1])
    itens.to_csv(POWERBI_DIR / "dim_item.csv", index=False)

    fato = precos.dropna(subset=["preco"])[["serie_id", "data", "preco", "imputado"]]
    fato.to_csv(POWERBI_DIR / "fato_precos.csv", index=False)

    # desvio de cada mês em relação à média móvel centrada de 12 meses
    media_movel = precos.groupby("serie_id")["preco"].transform(lambda s: s.rolling(12, center=True).mean())
    precos["desvio"] = (lp - np.log(media_movel)) * 100
    saz = (
        precos.assign(mes=precos["data"].dt.month)
        .groupby(["serie_id", "mes"])["desvio"].mean().round(2)
        .rename("desvio_sazonal_pct").reset_index()
    )
    saz.to_csv(POWERBI_DIR / "sazonalidade.csv", index=False)
    log.info("dim_item (%s), fato_precos (%s) e sazonalidade exportados", len(itens), len(fato))


def main() -> None:
    garantir_pastas()
    metricas = pd.read_csv(POWERBI_DIR / "metricas_modelos.csv")
    prev_teste = pd.read_csv(POWERBI_DIR / "previsoes_teste.csv")
    nome = escolher_modelo(metricas)
    log.info("Modelo final: %s", nome)

    base = pd.read_parquet(ARQUIVO_MODELAGEM)
    precos = pd.read_parquet(ARQUIVO_PRECOS)
    futuro = linhas_para_previsao(base)
    ret = prever_variacao_futura(nome, base, precos, futuro)
    faixas = faixas_de_erro(prev_teste, nome)

    saida = futuro[["serie_id", "item", "categoria", "data_base", "data_alvo", "preco"]].rename(
        columns={"preco": "preco_base"}
    )
    saida["modelo"] = nome
    saida["horizonte_meses"] = HORIZONTE
    saida["preco_previsto"] = (saida["preco_base"] * np.exp(ret)).round(3)
    q = saida["categoria"].map(faixas["q10"]).fillna(faixas["q10"].median())
    saida["faixa_inferior"] = (saida["preco_previsto"] * q).round(3)
    q = saida["categoria"].map(faixas["q90"]).fillna(faixas["q90"].median())
    saida["faixa_superior"] = (saida["preco_previsto"] * q).round(3)
    saida["variacao_prevista_pct"] = ((np.exp(ret) - 1) * 100).round(2)

    saida.to_csv(POWERBI_DIR / "previsao_futura.csv", index=False)
    log.info(
        "Previsão para %s séries (alvo mais comum: %s)",
        len(saida), saida["data_alvo"].mode().iloc[0].date(),
    )
    exportar_dimensoes()


if __name__ == "__main__":
    main()
