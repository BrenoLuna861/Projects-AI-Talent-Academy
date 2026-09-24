# src — Código do pipeline

Execute sempre a partir da raiz do projeto, para os imports `src.*` funcionarem:

```bash
python -m src.etl.run_pipeline      # ETL completo
python -m src.models.train_model    # treino
python -m src.models.evaluate       # métricas + limiar
python -m src.models.predict_model  # export para o Power BI
```

## Módulos

| Caminho | Responsabilidade |
|---|---|
| `config.py` | Caminhos, IDs do Drive, `SCHEMA_ESPERADO`, seed, proporção de teste — **único lugar** com caminho escrito |
| `utils/schema.py` | Valida as colunas de cada tabela e falha com mensagem útil |
| `utils/logger.py` | Logger padronizado |
| `etl/extract.py` | Baixa os CSVs do Drive se faltarem e carrega as seis tabelas |
| `etl/transform.py` | Quarentena: marca `motivo_rejeicao` e separa válidas de rejeitadas |
| `etl/build_dataset.py` | Unifica as tabelas e cria o rótulo a partir de `contestacoes` |
| `etl/load.py` | Grava parquet/CSV |
| `etl/run_pipeline.py` | Orquestra tudo, com `assert` de reconciliação |
| `features/build_features.py` | Features e a lista `COLUNAS_MODELO` |
| `models/train_model.py` | Split temporal + dicionário `MODELOS` |
| `models/evaluate.py` | Métricas e `escolher_limiar()` |
| `models/predict_model.py` | Exporta `predicoes.csv` e `transacoes_dashboard.csv` |

## Convenções

- **Nenhum caminho absoluto fora de `config.py`.**
- **Nenhuma feature pode usar o futuro.** Todo agregado histórico usa `expanding().shift(1)`. Quem adicionar feature nova precisa respeitar isso — é a diferença entre métrica real e métrica ilusória.
- `SEED = 42` em tudo que tem aleatoriedade.
- Algoritmo novo entra no dicionário `MODELOS` de `train_model.py`; a avaliação percorre esse dicionário sozinha.
- Mudou nome de coluna na base? Ajuste `SCHEMA_ESPERADO` em `config.py` — o validador acusa antes do pipeline quebrar.
