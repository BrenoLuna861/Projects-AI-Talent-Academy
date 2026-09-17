"""Treino e comparação de modelos de classificação de fraude."""
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.config import (
    ARQUIVO_TRATADO,
    COLUNA_ALVO,
    MODELS_DIR,
    SEED,
    TAMANHO_TESTE,
)
from src.utils.logger import get_logger

log = get_logger(__name__)

# Modelos comparados. class_weight="balanced" compensa o desbalanceamento
# sem precisar reamostrar; SMOTE pode ser testado como alternativa.
MODELOS = {
    "regressao_logistica": Pipeline(
        [
            ("escala", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000, class_weight="balanced", random_state=SEED
                ),
            ),
        ]
    ),
    "random_forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced_subsample",
        n_jobs=-1,
        random_state=SEED,
    ),
}


def separar_dados(df: pd.DataFrame):
    X = df.drop(columns=[COLUNA_ALVO]).select_dtypes(include="number")
    y = df[COLUNA_ALVO]
    return train_test_split(
        X, y, test_size=TAMANHO_TESTE, stratify=y, random_state=SEED
    )


def treinar(nome: str, modelo, X_treino, y_treino):
    log.info("Treinando %s...", nome)
    modelo.fit(X_treino, y_treino)
    caminho = MODELS_DIR / f"{nome}.joblib"
    joblib.dump(modelo, caminho)
    log.info("Modelo salvo em %s", caminho)
    return modelo


def main() -> None:
    df = pd.read_parquet(ARQUIVO_TRATADO)
    X_treino, X_teste, y_treino, y_teste = separar_dados(df)
    joblib.dump((X_teste, y_teste), MODELS_DIR / "conjunto_teste.joblib")
    for nome, modelo in MODELOS.items():
        treinar(nome, modelo, X_treino, y_treino)


if __name__ == "__main__":
    main()
