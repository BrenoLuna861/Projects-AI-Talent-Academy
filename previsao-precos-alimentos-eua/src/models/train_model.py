"""Treino dos modelos com separação temporal.

    python -m src.models.train_model

Treino: linhas cujo mês-alvo é <= FIM_TREINO.
Teste:  linhas cujo mês-base é >= FIM_TREINO. Isso garante que, na hora de
        prever, o modelo não viu nenhum preço posterior ao mês-base.
"""
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import ARQUIVO_MODELAGEM, FIM_TREINO, MODELS_DIR, SEED, garantir_pastas
from src.features.build_features import (
    FEATURES_CATEGORICAS,
    FEATURES_NUMERICAS,
    linhas_utilizaveis,
)
from src.utils.logger import get_logger

log = get_logger(__name__)

FEATURES = FEATURES_NUMERICAS + FEATURES_CATEGORICAS


def _preprocessador(escalar: bool) -> ColumnTransformer:
    num = StandardScaler() if escalar else "passthrough"
    return ColumnTransformer(
        [
            ("num", num, FEATURES_NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), FEATURES_CATEGORICAS),
        ]
    )


def criar_modelos() -> dict:
    return {
        "ridge": Pipeline([("prep", _preprocessador(True)), ("reg", Ridge(alpha=10.0))]),
        "random_forest": Pipeline(
            [
                ("prep", _preprocessador(False)),
                ("reg", RandomForestRegressor(
                    n_estimators=400, min_samples_leaf=20, max_features=0.5,
                    n_jobs=-1, random_state=SEED,
                )),
            ]
        ),
        "gradient_boosting": Pipeline(
            [
                ("prep", _preprocessador(False)),
                ("reg", HistGradientBoostingRegressor(
                    learning_rate=0.03, max_iter=400, max_leaf_nodes=15,
                    min_samples_leaf=40, l2_regularization=1.0, random_state=SEED,
                )),
            ]
        ),
    }


# Baselines: não treinam nada, servem de régua.
def prever_ingenuo(X: pd.DataFrame) -> np.ndarray:
    """Preço daqui a h meses = preço de hoje."""
    return np.zeros(len(X))


def prever_sazonal(X: pd.DataFrame) -> np.ndarray:
    """Repete a variação que aconteceu na mesma janela do ano anterior."""
    return X["sazonal_ano_anterior"].to_numpy()


BASELINES = {"ingenuo": prever_ingenuo, "sazonal_ingenuo": prever_sazonal}


def separar_treino_teste(base: pd.DataFrame, fim_treino: str = FIM_TREINO):
    base = linhas_utilizaveis(base)
    corte = pd.Timestamp(fim_treino)
    treino = base[base["data_alvo"] <= corte]
    teste = base[base["data_base"] >= corte]
    return treino, teste


def main() -> None:
    garantir_pastas()
    base = pd.read_parquet(ARQUIVO_MODELAGEM)
    treino, teste = separar_treino_teste(base)
    log.info(
        "Treino: %s linhas (alvo até %s) | Teste: %s linhas (base a partir de %s)",
        len(treino), treino["data_alvo"].max().date(), len(teste), teste["data_base"].min().date(),
    )

    for nome, modelo in criar_modelos().items():
        modelo.fit(treino[FEATURES], treino["alvo"])
        joblib.dump(modelo, MODELS_DIR / f"{nome}.joblib")
        log.info("%s treinado", nome)

    teste.to_parquet(MODELS_DIR / "conjunto_teste.parquet", index=False)


if __name__ == "__main__":
    main()
