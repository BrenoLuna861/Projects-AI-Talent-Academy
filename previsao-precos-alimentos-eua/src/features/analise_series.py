"""Ferramentas de análise de série temporal usadas no notebook 05 e no dashboard."""
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller


def trecho_continuo(y: pd.Series) -> pd.Series:
    """Maior trecho sem buracos da série (STL e ADF não aceitam valores vazios)."""
    vazio = y.isna()
    bloco = vazio.cumsum()
    trechos = y[~vazio].groupby(bloco[~vazio])
    maior = max(trechos, key=lambda kv: len(kv[1]))[1]
    return maior


def decompor(y: pd.Series, periodo: int = 12):
    """STL no log do preço: tendência + sazonalidade + resto."""
    return STL(np.log(trecho_continuo(y)), period=periodo, robust=True).fit()


def forcas(y: pd.Series, periodo: int = 12) -> tuple[float, float]:
    """Força da tendência e da sazonalidade (0 a 1), como em Hyndman & Athanasopoulos.

    F = 1 - var(resto) / var(componente + resto). Perto de 1: o componente
    domina a série; perto de 0: a série é basicamente ruído em torno dele.
    """
    d = decompor(y, periodo)
    r = d.resid
    ft = max(0.0, 1 - r.var() / (d.trend + r).var())
    fs = max(0.0, 1 - r.var() / (d.seasonal + r).var())
    return round(ft, 3), round(fs, 3)


def adf_pvalor(y: pd.Series) -> float:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return float(adfuller(trecho_continuo(y).dropna(), autolag="AIC")[1])


def agregar(precos: pd.DataFrame, freq: str) -> pd.DataFrame:
    """Média do preço por série em outra granularidade ('QS' trimestre, 'YS' ano).

    Período com algum mês faltando fica vazio, para não comparar um trimestre
    de 3 meses com um de 1 mês.
    """
    g = precos.set_index("data").groupby("serie_id")["preco"]
    media = g.resample(freq).mean()
    meses = g.resample(freq).count()
    esperado = {"QS": 3, "YS": 12}[freq]
    media[meses < esperado] = np.nan
    return media.rename("preco").reset_index()
