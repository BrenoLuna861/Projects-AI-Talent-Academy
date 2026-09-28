"""Modelos clássicos de série temporal, um por item.

Diferente do modelo global de ML (um modelo para todos os itens, com features),
aqui cada série tem seu próprio modelo, ajustado só com o histórico dela:

- SARIMA(1,1,1)(0,1,1)12 no log do preço: o preço de amanhã depende do de hoje
  (parte autorregressiva), dos erros recentes (média móvel) e do mesmo mês do
  ano anterior (parte sazonal). As diferenças (d=1, D=1) tiram tendência e
  sazonalidade para a série ficar estacionária.
- ETS (Holt-Winters) com tendência amortecida e sazonalidade de 12 meses:
  suavização exponencial, dá mais peso às observações recentes.

Protocolo igual ao do ML, para a comparação ser justa: os parâmetros são
estimados só com dados até o corte; depois, para cada mês-base t do teste,
o modelo é "alimentado" com os preços até t (sem reestimar nada) e prevê t+3.
"""
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.config import HORIZONTE

METODOS = ("sarima", "ets")


def serie_log(precos: pd.DataFrame, serie_id: str) -> pd.Series:
    s = precos.loc[precos["serie_id"] == serie_id].set_index("data")["preco"]
    return np.log(s.asfreq("MS"))


def criar_modelo(y: pd.Series, metodo: str):
    if metodo == "sarima":
        return SARIMAX(y, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12))
    if metodo == "ets":
        return ExponentialSmoothing(y, trend=True, damped_trend=True, seasonal=12)
    raise ValueError(f"método desconhecido: {metodo}")


def _prever_serie(y: pd.Series, datas_base, corte, metodo: str, h: int) -> list:
    with warnings.catch_warnings():
        # séries curtas às vezes não convergem 100%; o resultado ainda é usável
        warnings.simplefilter("ignore")
        ajuste = criar_modelo(y[y.index <= corte], metodo).fit(disp=False)
        saida = []
        for t in datas_base:
            filtrado = ajuste.apply(y[y.index <= t])
            previsto = filtrado.forecast(h).iloc[-1]
            saida.append((t, previsto - y[t]))
    return saida


def prever_variacao(
    precos: pd.DataFrame, teste: pd.DataFrame, corte, metodo: str, h: int = HORIZONTE, n_jobs: int = -1
) -> np.ndarray:
    """Variação prevista (log) para cada linha de `teste`, na mesma ordem."""
    corte = pd.Timestamp(corte)
    grupos = list(teste.groupby("serie_id")["data_base"])
    resultados = Parallel(n_jobs=n_jobs)(
        delayed(_prever_serie)(serie_log(precos, sid), list(datas), corte, metodo, h)
        for sid, datas in grupos
    )
    linhas = [
        (sid, t, r)
        for (sid, _), res in zip(grupos, resultados)
        for t, r in res
    ]
    prev = pd.DataFrame(linhas, columns=["serie_id", "data_base", "ret"])
    return teste[["serie_id", "data_base"]].merge(prev, how="left")["ret"].to_numpy()


def prever_futuro(y: pd.Series, metodo: str, h: int = HORIZONTE):
    """Ajusta com toda a série `y` (log do preço) e devolve (previsão, limite 10%, limite 90%) em log."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ajuste = criar_modelo(y, metodo).fit(disp=False)
        fc = ajuste.get_forecast(h)
    media = fc.predicted_mean.iloc[-1]
    inf, sup = fc.conf_int(alpha=0.2).iloc[-1]
    return media, inf, sup
