"""Treino com split temporal e comparação de modelos."""
import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import (
    ARQUIVO_DATASET,
    COLUNA_ALVO,
    COLUNA_TEMPO,
    MODELS_DIR,
    PROPORCAO_TESTE,
    SEED,
)
from src.features.build_features import COLUNAS_MODELO
from src.utils.logger import get_logger

log = get_logger(__name__)

# class_weight compensa o desbalanceamento sem reamostrar.
# SMOTE fica como alternativa a testar — ver docs/escopo.md.
MODELOS = {
    "regressao_logistica": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("escala", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)),
    ]),
    "random_forest": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=5,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=SEED,
        )),
    ]),
    "gradient_boosting": Pipeline([
        ("clf", HistGradientBoostingClassifier(random_state=SEED)),  # lida com NaN sozinho
    ]),
}


def separar_temporal(df: pd.DataFrame, proporcao_teste: float = PROPORCAO_TESTE):
    """Divide por tempo, não aleatoriamente.

    Fraude evolui: padrão de ataque muda de um mês para o outro. Um split
    aleatório deixa o modelo treinar com transações posteriores às do
    teste — o resultado fica bonito e não se sustenta em produção.
    """
    df = df.sort_values(COLUNA_TEMPO).reset_index(drop=True)
    corte = int(len(df) * (1 - proporcao_teste))
    data_corte = df.loc[corte, COLUNA_TEMPO]

    treino = df.iloc[:corte]
    teste = df.iloc[corte:]

    log.info(
        "Split temporal em %s | treino: %s linhas (%.2f%% fraude) | teste: %s linhas (%.2f%% fraude)",
        data_corte, len(treino), 100 * treino[COLUNA_ALVO].mean(),
        len(teste), 100 * teste[COLUNA_ALVO].mean(),
    )

    X_treino = treino[COLUNAS_MODELO]
    X_teste = teste[COLUNAS_MODELO]
    return X_treino, X_teste, treino[COLUNA_ALVO], teste[COLUNA_ALVO], teste


def main() -> None:
    df = pd.read_parquet(ARQUIVO_DATASET)
    X_treino, X_teste, y_treino, y_teste, teste_completo = separar_temporal(df)

    joblib.dump((X_teste, y_teste), MODELS_DIR / "conjunto_teste.joblib")
    teste_completo.to_parquet(MODELS_DIR / "teste_completo.parquet", index=False)

    for nome, modelo in MODELOS.items():
        log.info("Treinando %s...", nome)
        modelo.fit(X_treino, y_treino)
        joblib.dump(modelo, MODELS_DIR / f"{nome}.joblib")
        log.info("Salvo: %s.joblib", nome)


if __name__ == "__main__":
    main()
