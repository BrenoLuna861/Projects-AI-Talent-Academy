import numpy as np
import pandas as pd

from src.config import SERIE_GASOLINA
from src.features.build_features import FEATURES_NUMERICAS, construir_base
from src.models.train_model import separar_treino_teste


def _precos(meses=48, seed=0):
    rng = np.random.default_rng(seed)
    datas = pd.date_range("2018-01-01", periods=meses, freq="MS")
    partes = []
    for sid, cat in [("S1", "Ovos"), ("S2", "Ovos"), (SERIE_GASOLINA, "Energia")]:
        preco = 2 * np.exp(np.cumsum(rng.normal(0, 0.03, meses)))
        partes.append(pd.DataFrame({
            "serie_id": sid, "data": datas, "preco": preco, "imputado": False,
            "item": sid, "categoria": cat,
        }))
    return pd.concat(partes, ignore_index=True)


def test_alvo_e_log_da_variacao_no_horizonte():
    precos = _precos()
    base = construir_base(precos, ["S1"], h=3)
    s1 = precos[precos["serie_id"] == "S1"].reset_index(drop=True)
    linha = base.iloc[10]
    esperado = np.log(s1.loc[13, "preco"] / s1.loc[10, "preco"])
    assert np.isclose(linha["alvo"], esperado)
    assert linha["data_alvo"] == s1.loc[13, "data"]


def test_features_nao_olham_para_frente():
    """Mudar os preços depois de t não pode mudar nenhuma feature da linha t."""
    precos = _precos()
    t = pd.Timestamp("2020-06-01")
    base_a = construir_base(precos, ["S1", "S2"], h=3)

    alterado = precos.copy()
    futuro = alterado["data"] > t
    alterado.loc[futuro, "preco"] *= 5
    base_b = construir_base(alterado, ["S1", "S2"], h=3)

    a = base_a[base_a["data_base"] == t].set_index("serie_id")[FEATURES_NUMERICAS]
    b = base_b[base_b["data_base"] == t].set_index("serie_id")[FEATURES_NUMERICAS]
    pd.testing.assert_frame_equal(a, b)


def test_treino_nao_enxerga_periodo_de_teste():
    base = construir_base(_precos(), ["S1", "S2"], h=3)
    treino, teste = separar_treino_teste(base, "2020-12-01")
    assert treino["data_alvo"].max() <= teste["data_base"].min()
