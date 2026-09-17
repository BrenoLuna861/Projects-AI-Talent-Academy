# src — Código do pipeline

Pacote Python do projeto. Sempre executar a partir da raiz do projeto para que os
imports `src.*` funcionem:

```bash
python -m src.etl.run_pipeline
python -m src.models.train_model
python -m src.models.evaluate
```

## Módulos

| Caminho | Responsabilidade |
|---|---|
| `config.py` | Caminhos, nome da coluna alvo, seed, tamanho do teste e limiar de decisão — **único lugar** onde caminhos são escritos |
| `etl/extract.py` | Leitura da base bruta |
| `etl/transform.py` | Duplicatas, nulos e padronização de tipos |
| `etl/load.py` | Gravação do dataset tratado em `data/processed/` |
| `etl/run_pipeline.py` | Orquestra extract → transform → features → load |
| `features/build_features.py` | `hora_do_dia`, `faixa_valor` e demais atributos derivados |
| `models/train_model.py` | Treino e persistência dos modelos comparados |
| `models/predict_model.py` | Predições e export do `predicoes.csv` para o Power BI |
| `models/evaluate.py` | Recall, precision, F1, AUC-PR e matriz de confusão |
| `utils/logger.py` | Logger padronizado |

## Convenções

- Nenhum caminho absoluto fora de `config.py`.
- Funções pequenas e testáveis: o que recebe e devolve um `DataFrame` pode ser testado em `tests/`.
- `SEED = 42` em tudo que tiver aleatoriedade, para os resultados serem reproduzíveis entre os integrantes.
- Novo algoritmo entra no dicionário `MODELOS` de `train_model.py` — a avaliação percorre esse dicionário automaticamente.
