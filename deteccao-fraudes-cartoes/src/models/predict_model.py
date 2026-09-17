"""Geração de predições para o dashboard."""
import joblib
import pandas as pd

from src.config import ARQUIVO_PREDICOES, LIMIAR_DECISAO, MODELS_DIR
from src.utils.logger import get_logger

log = get_logger(__name__)


def prever(nome_modelo: str, X: pd.DataFrame, limiar: float = LIMIAR_DECISAO):
    modelo = joblib.load(MODELS_DIR / f"{nome_modelo}.joblib")
    probabilidades = modelo.predict_proba(X)[:, 1]
    return probabilidades, (probabilidades >= limiar).astype(int)


def exportar_predicoes(
    nome_modelo: str, X: pd.DataFrame, y_real: pd.Series | None = None
) -> pd.DataFrame:
    """Exporta o CSV consumido pelo Power BI."""
    prob, classe = prever(nome_modelo, X)
    saida = pd.DataFrame(
        {
            "id_transacao": X.index,
            "probabilidade_fraude": prob,
            "classe_prevista": classe,
            "modelo": nome_modelo,
        }
    )
    if y_real is not None:
        saida["classe_real"] = y_real.values
    saida.to_csv(ARQUIVO_PREDICOES, index=False)
    log.info("Predições exportadas para %s", ARQUIVO_PREDICOES)
    return saida
