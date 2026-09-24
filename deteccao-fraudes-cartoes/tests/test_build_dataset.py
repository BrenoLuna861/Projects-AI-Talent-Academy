import pandas as pd

from src.etl.build_dataset import adicionar_rotulo


def test_rotulo_marca_apenas_as_contestadas():
    transacoes = pd.DataFrame({"id_transacao": [1, 2, 3]})
    contestacoes = pd.DataFrame({"id_transacao": [2]})
    resultado = adicionar_rotulo(transacoes, contestacoes)
    assert resultado["fraude"].tolist() == [0, 1, 0]


def test_rotulo_ignora_contestacao_de_transacao_inexistente():
    transacoes = pd.DataFrame({"id_transacao": [1, 2]})
    contestacoes = pd.DataFrame({"id_transacao": [99]})
    assert adicionar_rotulo(transacoes, contestacoes)["fraude"].sum() == 0
