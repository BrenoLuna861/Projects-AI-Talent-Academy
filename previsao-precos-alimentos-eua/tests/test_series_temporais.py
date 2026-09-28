import numpy as np
import pandas as pd

from src.models.series_temporais import prever_variacao


def _precos(meses=72, seed=1):
    rng = np.random.default_rng(seed)
    datas = pd.date_range("2018-01-01", periods=meses, freq="MS")
    sazonal = 0.05 * np.sin(2 * np.pi * np.arange(meses) / 12)
    preco = 3 * np.exp(np.cumsum(rng.normal(0.003, 0.01, meses)) + sazonal)
    return pd.DataFrame({"serie_id": "S1", "data": datas, "preco": preco})


def test_previsao_nao_usa_precos_depois_do_mes_base():
    precos = _precos()
    teste = pd.DataFrame({"serie_id": ["S1"] * 3, "data_base": pd.to_datetime(["2022-01-01", "2022-02-01", "2022-03-01"])})
    a = prever_variacao(precos, teste, "2021-12-01", "sarima", n_jobs=1)

    alterado = precos.copy()
    alterado.loc[alterado["data"] > "2022-03-01", "preco"] *= 3
    b = prever_variacao(alterado, teste, "2021-12-01", "sarima", n_jobs=1)
    np.testing.assert_allclose(a, b)


def test_sarima_captura_sazonalidade_simples():
    precos = _precos()
    teste = pd.DataFrame({"serie_id": ["S1"], "data_base": pd.to_datetime(["2022-06-01"])})
    ret = prever_variacao(precos, teste, "2021-12-01", "sarima", n_jobs=1)[0]
    s = precos.set_index("data")["preco"]
    real = np.log(s["2022-09-01"] / s["2022-06-01"])
    assert abs(ret - real) < 0.05
