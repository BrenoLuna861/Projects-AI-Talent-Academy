import pandas as pd

from src.features.build_features import (
    construir_features,
    features_historicas_cartao,
    features_temporais,
)


def _df():
    return pd.DataFrame({
        "id_transacao": [1, 2, 3, 4],
        "id_cartao": [10, 10, 10, 11],
        "id_lojista": [100, 100, 100, 101],
        "valor": [100.0, 200.0, 3.0, 50.0],
        "data_hora": pd.to_datetime([
            "2026-01-01 02:00:00",
            "2026-01-01 10:00:00",
            "2026-01-01 11:00:00",
            "2026-01-02 15:00:00",
        ]),
        "canal": ["online", "presencial", "online", "online"],
        "fraude": [1, 0, 0, 0],
    })


def test_madrugada():
    df = features_temporais(_df())
    assert df["madrugada"].tolist() == [1, 0, 0, 0]


def test_media_do_cartao_nao_usa_o_futuro():
    """A primeira transação do cartão não pode ter média — não há passado."""
    df = features_historicas_cartao(_df())
    primeira = df[df["id_cartao"] == 10].iloc[0]
    segunda = df[df["id_cartao"] == 10].iloc[1]
    assert pd.isna(primeira["media_valor_cartao_ate_agora"])
    assert segunda["media_valor_cartao_ate_agora"] == 100.0


def test_taxa_do_lojista_nao_vaza_o_rotulo():
    """A taxa histórica da própria linha não pode incluir o rótulo dela."""
    df = construir_features(_df(), coluna_alvo="fraude")
    primeira = df[df["id_lojista"] == 100].iloc[0]
    assert pd.isna(primeira["taxa_contestacao_lojista_ate_agora"])


def test_canal_online_binario():
    df = construir_features(_df(), coluna_alvo="fraude")
    assert set(df["canal_online"].unique()) <= {0, 1}
