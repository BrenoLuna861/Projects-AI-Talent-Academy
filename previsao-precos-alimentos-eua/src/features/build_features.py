"""Monta a base de modelagem: uma linha por (série, mês-base).

O modelo não prevê o preço direto, e sim a variação em log entre o mês-base t
e o mês t + HORIZONTE. Assim o kWh (US$ 0,20) e a libra de sirloin
(US$ 14,59) ficam na mesma escala e dá para treinar um modelo só para todas.

Regra: toda feature da linha t usa só informação disponível até t.
"""
import numpy as np
import pandas as pd

from src.config import HORIZONTE, SERIE_GASOLINA
from src.utils.logger import get_logger

log = get_logger(__name__)

FEATURES_NUMERICAS = [
    "ret_1",
    "ret_3",
    "ret_6",
    "ret_12",
    "dist_media_12",
    "vol_6",
    "sazonal_ano_anterior",
    "ret_3_categoria",
    "gasolina_ret_3",
    "gasolina_ret_12",
    "mes_alvo_sin",
    "mes_alvo_cos",
]
FEATURES_CATEGORICAS = ["categoria"]


def _features_da_serie(g: pd.DataFrame, h: int) -> pd.DataFrame:
    g = g.sort_values("data").copy()
    lp = np.log(g["preco"])

    g["ret_1"] = lp.diff(1)
    g["ret_3"] = lp.diff(3)
    g["ret_6"] = lp.diff(6)
    g["ret_12"] = lp.diff(12)
    g["dist_media_12"] = lp - np.log(g["preco"].rolling(12, min_periods=10).mean())
    g["vol_6"] = g["ret_1"].rolling(6, min_periods=5).std()
    # o que aconteceu nesta mesma janela do ano passado (t-12 -> t-12+h)
    g["sazonal_ano_anterior"] = lp.shift(12 - h) - lp.shift(12)

    # alvo e informações do mês-alvo (olham para frente de propósito)
    g["data_alvo"] = g["data"] + pd.DateOffset(months=h)
    g["preco_alvo"] = g["preco"].shift(-h)
    g["alvo_imputado"] = g["imputado"].shift(-h)
    g["alvo"] = lp.shift(-h) - lp
    return g


def adicionar_gasolina(base: pd.DataFrame, precos: pd.DataFrame) -> pd.DataFrame:
    gas = precos.loc[precos["serie_id"] == SERIE_GASOLINA, ["data", "preco"]].sort_values("data")
    if gas.empty:
        raise ValueError(f"Série de gasolina {SERIE_GASOLINA} não encontrada")
    lg = np.log(gas.set_index("data")["preco"])
    extra = pd.DataFrame({"gasolina_ret_3": lg.diff(3), "gasolina_ret_12": lg.diff(12)}).reset_index()
    return base.merge(extra, on="data", how="left")


def adicionar_media_categoria(base: pd.DataFrame) -> pd.DataFrame:
    """Média do ret_3 da categoria no mesmo mês-base (sem olhar para frente)."""
    media = base.groupby(["categoria", "data"])["ret_3"].transform("mean")
    base["ret_3_categoria"] = media
    return base


def construir_base(precos: pd.DataFrame, series_modelagem, h: int = HORIZONTE) -> pd.DataFrame:
    dados = precos[precos["serie_id"].isin(series_modelagem)]
    base = pd.concat(
        [_features_da_serie(g, h) for _, g in dados.groupby("serie_id", sort=False)],
        ignore_index=True,
    )
    base = adicionar_gasolina(base, precos)
    base = adicionar_media_categoria(base)

    mes = base["data_alvo"].dt.month
    base["mes_alvo_sin"] = np.sin(2 * np.pi * mes / 12)
    base["mes_alvo_cos"] = np.cos(2 * np.pi * mes / 12)

    base = base.rename(columns={"data": "data_base"})
    colunas = (
        ["serie_id", "item", "categoria", "data_base", "data_alvo", "preco", "imputado",
         "preco_alvo", "alvo_imputado", "alvo"]
        + [c for c in FEATURES_NUMERICAS]
    )
    base = base[colunas]
    log.info("Base de modelagem: %s linhas, %s séries, horizonte %s meses",
             len(base), base["serie_id"].nunique(), h)
    return base


def linhas_utilizaveis(base: pd.DataFrame) -> pd.DataFrame:
    """Linhas com todas as features e alvo real (não interpolado)."""
    ok = base[FEATURES_NUMERICAS + ["alvo"]].notna().all(axis=1)
    ok &= base["alvo_imputado"].eq(False)
    return base[ok]


def linhas_para_previsao(base: pd.DataFrame, tolerancia_meses: int = 2) -> pd.DataFrame:
    """Último mês-base de cada série com features completas (alvo ainda desconhecido).

    Série cujo último mês utilizável ficou muito para trás (buraco recente)
    fica de fora: prever a partir de um preço de um ano atrás não faz sentido.
    """
    tem_features = base[FEATURES_NUMERICAS].notna().all(axis=1)
    ultimas = base[tem_features].sort_values("data_base").groupby("serie_id").tail(1)
    limite = base["data_base"].max() - pd.DateOffset(months=tolerancia_meses)
    atrasadas = ultimas["data_base"] < limite
    if atrasadas.any():
        log.warning("Sem previsão (dados recentes incompletos): %s", ", ".join(ultimas.loc[atrasadas, "item"]))
    return ultimas[~atrasadas]
