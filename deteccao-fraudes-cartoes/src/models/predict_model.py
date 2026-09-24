"""Predições e exportação das tabelas que alimentam o Power BI."""
import joblib
import pandas as pd

from src.config import (
    ARQUIVO_PREDICOES,
    ARQUIVO_TRANSACOES_BI,
    COLUNA_ALVO,
    LIMIAR_DECISAO,
    MODELS_DIR,
)
from src.features.build_features import COLUNAS_MODELO
from src.models.evaluate import escolher_limiar
from src.utils.logger import get_logger

log = get_logger(__name__)

COLUNAS_DASHBOARD = [
    "id_transacao", "id_cartao", "id_lojista", "id_cliente",
    "valor", "data_hora", "canal", "nome_lojista", "nome_categoria",
    "hora_do_dia", "faixa_valor", "madrugada", "padrao_teste_cartao",
]


def exportar(nome_modelo: str = "random_forest", limiar: float | None = None) -> None:
    """Gera predicoes.csv e transacoes_dashboard.csv.

    limiar=None => calcula o ponto de corte pela curva precision-recall,
    em vez de usar o 0.5 de fábrica (ver src/models/evaluate.py).
    """
    modelo = joblib.load(MODELS_DIR / f"{nome_modelo}.joblib")
    teste = pd.read_parquet(MODELS_DIR / "teste_completo.parquet")

    probabilidade = modelo.predict_proba(teste[COLUNAS_MODELO])[:, 1]
    if limiar is None:
        limiar = escolher_limiar(teste[COLUNA_ALVO], probabilidade)

    predicoes = pd.DataFrame({
        "id_transacao": teste["id_transacao"].values,
        "probabilidade_fraude": probabilidade,
        "classe_prevista": (probabilidade >= limiar).astype(int),
        "classe_real": teste[COLUNA_ALVO].values,
        "modelo": nome_modelo,
    })
    predicoes.to_csv(ARQUIVO_PREDICOES, index=False)
    log.info("Predicoes: %s (%s linhas)", ARQUIVO_PREDICOES.name, len(predicoes))

    colunas = [c for c in COLUNAS_DASHBOARD if c in teste.columns]
    teste[colunas].to_csv(ARQUIVO_TRANSACOES_BI, index=False)
    log.info("Tabela do dashboard: %s", ARQUIVO_TRANSACOES_BI.name)


if __name__ == "__main__":
    exportar()
