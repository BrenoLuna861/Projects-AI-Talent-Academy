import pandas as pd

from src.etl.transform import separar_quarentena


def _base():
    return pd.DataFrame({
        "id_transacao": [1, 2, 2, 4, 5],
        "id_cartao": [10, 11, 11, 12, 13],
        "id_lojista": [100, 101, 101, 102, 103],
        "valor": [50.0, 20.0, 20.0, 0.0, None],
        "data_hora": ["2026-01-01 10:00:00"] * 5,
        "canal": ["online"] * 5,
    })


def test_quarentena_nao_perde_linha():
    validas, rejeitadas = separar_quarentena(_base())
    assert len(validas) + len(rejeitadas) == 5


def test_quarentena_separa_os_motivos():
    _, rejeitadas = separar_quarentena(_base())
    motivos = set(rejeitadas["motivo_rejeicao"])
    assert "id_transacao duplicado" in motivos
    assert "valor menor ou igual a zero" in motivos
    assert "campo obrigatorio nulo" in motivos


def test_validas_ficam_com_tipos_convertidos():
    validas, _ = separar_quarentena(_base())
    assert str(validas["data_hora"].dtype).startswith("datetime64")
    assert validas["valor"].dtype == float
