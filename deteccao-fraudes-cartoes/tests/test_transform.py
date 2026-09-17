import pandas as pd

from src.etl.transform import remover_duplicatas, padronizar_tipos


def test_remover_duplicatas():
    df = pd.DataFrame({"a": [1, 1, 2]})
    assert len(remover_duplicatas(df)) == 2


def test_padronizar_tipos():
    df = pd.DataFrame({"classe": [0, 1, 0]})
    assert padronizar_tipos(df)["classe"].dtype == "int8"
