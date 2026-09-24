"""Pipeline completo: extract -> quarentena -> unify -> rotulo -> features -> load."""
from src.config import (
    ARQUIVO_DATASET,
    ARQUIVO_REJEITADAS,
    ARQUIVO_VALIDAS,
    COLUNA_ALVO,
)
from src.etl.build_dataset import adicionar_rotulo, unificar
from src.etl.extract import carregar_tabelas
from src.etl.load import salvar
from src.etl.transform import separar_quarentena
from src.features.build_features import construir_features
from src.utils.logger import get_logger

log = get_logger(__name__)


def main() -> None:
    dfs = carregar_tabelas()

    validas, rejeitadas = separar_quarentena(dfs["transacoes"])
    salvar(validas, ARQUIVO_VALIDAS)
    salvar(rejeitadas, ARQUIVO_REJEITADAS)

    base = unificar(dfs, validas)
    base = adicionar_rotulo(base, dfs["contestacoes"])
    base = construir_features(base, coluna_alvo=COLUNA_ALVO)

    salvar(base, ARQUIVO_DATASET)

    # Reconciliação final: o dataset de modelagem tem que ter o mesmo
    # número de linhas das transações válidas.
    assert len(base) == len(validas), "linhas perdidas entre unify e features"
    log.info("Pipeline concluido. Dataset: %s linhas", len(base))


if __name__ == "__main__":
    main()
