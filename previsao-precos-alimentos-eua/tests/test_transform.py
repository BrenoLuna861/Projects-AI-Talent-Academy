import numpy as np
import pandas as pd

from src.etl.transform import padronizar, regularizar_grade, resumir_itens, validar_linhas


def _bruto(linhas):
    return pd.DataFrame(linhas, columns=["date", "year", "month", "item", "unit", "category", "price", "series_id"])


def _serie(sid, datas, precos, item="X", categoria="Padaria e grãos"):
    return pd.DataFrame({
        "serie_id": sid, "data": pd.to_datetime(datas), "preco": precos,
        "item": item, "unidade": "lb.", "categoria": categoria, "categoria_original": "Bakery and grains",
    })


def test_corrige_categoria_do_cafe():
    df = _bruto([["2020-01-01", 2020, 1, "Coffee", "lb.", "Beef", 5.0, "APU0000717311"]])
    assert padronizar(df)["categoria"].iloc[0] == "Mercearia"


def test_traduz_categoria():
    df = _bruto([["2020-01-01", 2020, 1, "Eggs", "doz.", "Eggs", 2.0, "APU0000708111"]])
    assert padronizar(df)["categoria"].iloc[0] == "Ovos"


def test_validar_linhas_separa_duplicada_e_preco_invalido():
    df = _serie("A", ["2020-01-01", "2020-01-01", "2020-02-01"], [1.0, 1.0, -3.0])
    ok, rej = validar_linhas(df)
    assert len(ok) == 1
    assert sorted(rej["motivo"]) == ["duplicada", "preco_nao_positivo"]


def test_buraco_curto_e_interpolado():
    df = _serie("A", ["2020-01-01", "2020-03-01"], [1.0, 4.0])
    out = regularizar_grade(df, max_gap=2)
    fev = out[out["data"] == "2020-02-01"].iloc[0]
    assert fev["imputado"]
    assert np.isclose(fev["preco"], 2.0)  # média geométrica: interpolação em log


def test_buraco_longo_fica_vazio():
    df = _serie("A", ["2020-01-01", "2020-06-01"], [1.0, 2.0])
    out = regularizar_grade(df, max_gap=2)
    assert out["preco"].isna().sum() == 4
    assert not out["imputado"].any()


def test_serie_descontinuada_nao_e_ativa():
    precos = pd.concat([
        _serie("A", pd.date_range("2020-01-01", "2023-12-01", freq="MS"), 1.0),
        _serie("B", pd.date_range("2020-01-01", "2021-06-01", freq="MS"), 1.0),
    ]).assign(imputado=False)
    itens = resumir_itens(precos).set_index("serie_id")
    assert itens.loc["A", "ativa"]
    assert not itens.loc["B", "ativa"]
    assert np.isnan(itens.loc["B", "variacao_12m_pct"])
