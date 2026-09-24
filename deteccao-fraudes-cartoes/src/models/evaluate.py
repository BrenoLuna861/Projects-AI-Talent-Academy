"""Avaliação dos modelos e exportação para o Power BI."""
from datetime import datetime

import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    precision_recall_curve,
    recall_score,
    roc_auc_score,
)

from src.config import ARQUIVO_METRICAS, LIMIAR_DECISAO, MODELS_DIR
from src.models.train_model import MODELOS
from src.utils.logger import get_logger

log = get_logger(__name__)


def calcular_metricas(y_real, y_prev, y_prob) -> dict:
    vn, fp, fn, vp = confusion_matrix(y_real, y_prev, labels=[0, 1]).ravel()
    return {
        "recall": recall_score(y_real, y_prev, zero_division=0),
        "precision": precision_score(y_real, y_prev, zero_division=0),
        "f1": f1_score(y_real, y_prev, zero_division=0),
        "auc_pr": average_precision_score(y_real, y_prob),
        "auc_roc": roc_auc_score(y_real, y_prob) if y_real.nunique() > 1 else float("nan"),
        "verdadeiros_positivos": vp,
        "falsos_positivos": fp,
        "falsos_negativos": fn,
        "verdadeiros_negativos": vn,
        "taxa_alerta": (vp + fp) / max(len(y_real), 1),
    }


def escolher_limiar(y_real, y_prob, recall_minimo: float = 0.70) -> float:
    """Escolhe o ponto de corte, em vez de aceitar o 0.5 de fábrica.

    O 0.5 pressupõe classes equilibradas. Com 1% de fraude, quase nenhuma
    transação alcança 50% de probabilidade — o modelo vira um detector que
    nunca acusa nada, com acurácia altíssima e recall zero.

    Aqui a lógica é de negócio: exigimos capturar pelo menos
    `recall_minimo` das fraudes e, entre os limiares que cumprem isso,
    ficamos com o de maior precisão — ou seja, o que gera menos alerta
    falso para a equipe de análise revisar.
    """
    precisao, recall, limiares = precision_recall_curve(y_real, y_prob)
    # precision_recall_curve devolve um ponto a mais que limiares
    precisao, recall = precisao[:-1], recall[:-1]

    viaveis = recall >= recall_minimo
    if not viaveis.any():
        log.warning(
            "Nenhum limiar alcanca recall de %.0f%%. Usando o de maior recall.",
            100 * recall_minimo,
        )
        return float(limiares[int(np.argmax(recall))])

    idx = int(np.argmax(np.where(viaveis, precisao, -1)))
    limiar = float(limiares[idx])
    log.info(
        "Limiar escolhido: %.4f (recall %.3f, precision %.3f)",
        limiar, recall[idx], precisao[idx],
    )
    return limiar


def avaliar_todos(limiar: float = LIMIAR_DECISAO) -> pd.DataFrame:
    X_teste, y_teste = joblib.load(MODELS_DIR / "conjunto_teste.joblib")
    linhas = []
    agora = datetime.now().isoformat(timespec="seconds")

    for nome in MODELOS:
        modelo = joblib.load(MODELS_DIR / f"{nome}.joblib")
        y_prob = modelo.predict_proba(X_teste)[:, 1]

        # Cada modelo calibra o seu próprio limiar: a escala de
        # probabilidade de uma floresta não é a de uma regressão logística.
        limiar_modelo = limiar if limiar is not None else escolher_limiar(y_teste, y_prob)
        y_prev = (y_prob >= limiar_modelo).astype(int)

        for metrica, valor in calcular_metricas(y_teste, y_prev, y_prob).items():
            linhas.append({
                "modelo": nome,
                "metrica": metrica,
                "valor": float(valor),
                "limiar": limiar_modelo,
                "data_execucao": agora,
            })
        log.info("%s avaliado (limiar %.4f)", nome, limiar_modelo)

    metricas = pd.DataFrame(linhas)
    metricas.to_csv(ARQUIVO_METRICAS, index=False)
    log.info("Metricas salvas em %s", ARQUIVO_METRICAS)
    return metricas


def main() -> None:
    # limiar=None => cada modelo escolhe o seu pela curva precision-recall
    metricas = avaliar_todos(limiar=None)
    resumo = metricas[metricas["metrica"].isin(["recall", "precision", "f1", "auc_pr", "taxa_alerta"])]
    print(resumo.pivot(index="modelo", columns="metrica", values="valor").round(4))
    print("\nLimiar por modelo:")
    print(metricas.groupby("modelo")["limiar"].first().round(4))


if __name__ == "__main__":
    main()
