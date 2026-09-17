import numpy as np
import pandas as pd

from src.features.build_features import adicionar_faixa_valor, adicionar_hora_do_dia


def test_hora_do_dia_a_partir_de_segundos():
    df = pd.DataFrame({"tempo": [0, 3600, 86399]})
    resultado = adicionar_hora_do_dia(df)
    assert resultado["hora_do_dia"].tolist() == [0, 1, 23]


def test_faixa_valor():
    df = pd.DataFrame({"valor": [10.0, 120.0, 500.0, 5000.0]})
    resultado = adicionar_faixa_valor(df)
    assert resultado["faixa_valor"].tolist() == [
        "ate_50",
        "50_a_200",
        "200_a_1000",
        "acima_1000",
    ]


def test_faixa_valor_sem_coluna():
    df = pd.DataFrame({"outra": [1, 2]})
    assert "faixa_valor" not in adicionar_faixa_valor(df).columns
