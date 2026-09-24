# Plano de Atividades e Divisão do Grupo

## Integrantes
| Integrante | Frente principal |
|---|---|
| **Breno Luna** | ETL, modelagem e estrutura do repositório |
| **Paula Carlesso** | Análise exploratória, dashboard Power BI e documentação |

## Etapas
| # | Etapa | Entregável | Responsável | Prazo | Status |
|---|---|---|---|---|---|
| 1 | Tema e escopo | `docs/escopo.md` | Breno e Paula | — | ✅ |
| 2 | Definição da base e do rótulo | `docs/dicionario-de-dados.md` | Breno e Paula | — | ✅ |
| 3 | Pipeline de ETL com quarentena | `src/etl/` | Breno | — | ✅ |
| 4 | Engenharia de atributos sem vazamento | `src/features/build_features.py` | Breno | — | ✅ |
| 5 | Treino e comparação de modelos | `src/models/train_model.py` | Breno | — | ✅ |
| 6 | Avaliação e escolha do limiar | `src/models/evaluate.py` | Breno | — | ✅ |
| 7 | **Rodar sobre a base real do curso** | `data/processed/` preenchido | | | ⬜ |
| 8 | EDA sobre a base real | `notebooks/01_analise_exploratoria.ipynb` executado | Paula | | ⬜ |
| 9 | Dashboard Power BI | `powerbi/dashboard-fraudes.pbix` | Paula | | ⬜ |
| 10 | Relatório final e apresentação | `reports/` + slides | Breno e Paula | | ⬜ |

## Próximo passo concreto

A etapa 7 destrava tudo o que falta. São três comandos:

```bash
python -m src.etl.run_pipeline
python -m src.models.train_model
python -m src.models.evaluate
```

O primeiro baixa os seis CSVs do Drive automaticamente. Se algum nome de coluna
divergir do esperado, o validador de schema avisa qual é, e o ajuste é feito em
`SCHEMA_ESPERADO` dentro de `src/config.py`.

Com isso rodando, os números reais aparecem e as etapas 8, 9 e 10 podem começar
em paralelo.

## Observações
- Trabalhar em branches por etapa (`etl`, `modelagem`, `dashboard`) e abrir PR para `main`.
- Limpar as saídas dos notebooks antes do commit — evita conflito impossível de resolver.
- Atualizar o **Status** desta tabela a cada acompanhamento.
