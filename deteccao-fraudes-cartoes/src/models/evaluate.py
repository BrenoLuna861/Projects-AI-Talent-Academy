"""Avaliação dos modelos e exportação das métricas para o Power BI."""
from datetime import datetime

import joblib
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.config import ARQUIVO_METRICAS, MODELS_DIR
from src.models.train_model import MODELOS
from src.utils.logger import get_logger

log = get_logger(__name__)


def calcular_metricas(y_real, y_prev, y_prob) -> dict:
    vn, fp, fn, vp = confusion_matrix(y_real, y_prev).ravel()
    return {
        "recall": recall_score(y_real, y_prev, zero_division=0),
        "precision": precision_score(y_real, y_prev, zero_division=0),
        "f1": f1_score(y_real, y_prev, zero_division=0),
        "auc_pr": average_precision_score(y_real, y_prob),
        "auc_roc": roc_auc_score(y_real, y_prob),
        "verdadeiros_positivos": vp,
        "falsos_positivos": fp,
        "falsos_negativos": fn,
        "verdadeiros_negativos": vn,
    }


def main() -> None:
    X_teste, y_teste = joblib.load(MODELS_DIR / "conjunto_teste.joblib")
    linhas = []
    agora = datetime.now().isoformat(timespec="seconds")
    for nome in MODELOS:
        modelo = joblib.load(MODELS_DIR / f"{nome}.joblib")
        y_prob = modelo.predict_proba(X_teste)[:, 1]
        y_prev = modelo.predict(X_teste)
        for metrica, valor in calcular_metricas(y_teste, y_prev, y_prob).items():
            linhas.append(
                {
                    "modelo": nome,
                    "metrica": metrica,
                    "valor": float(valor),
                    "data_execucao": agora,
                }
            )
        log.info("%s avaliado.", nome)
    pd.DataFrame(linhas).to_csv(ARQUIVO_METRICAS, index=False)
    log.info("Métricas salvas em %s", ARQUIVO_METRICAS)


if __name__ == "__main__":
    main()
