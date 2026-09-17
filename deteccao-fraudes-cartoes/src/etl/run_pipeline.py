"""Executa o ETL completo: extract -> transform -> features -> load."""
from src.etl.extract import carregar_dados_brutos
from src.etl.load import salvar_tratado
from src.etl.transform import transformar
from src.features.build_features import construir_features
from src.utils.logger import get_logger

log = get_logger(__name__)


def main() -> None:
    df = carregar_dados_brutos()
    df = transformar(df)
    df = construir_features(df)
    salvar_tratado(df)
    log.info("Pipeline de ETL concluído.")


if __name__ == "__main__":
    main()
