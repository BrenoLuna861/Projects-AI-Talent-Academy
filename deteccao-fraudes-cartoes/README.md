# Detecção de Fraudes em Cartões — Machine Learning + Dashboard

Projeto do grupo no **AI Talent Academy**. O objetivo é identificar transações
potencialmente fraudulentas com cartões de crédito usando Machine Learning e
apresentar os resultados em um **dashboard no Power BI**.

---

## 1. Escopo

| Item | Definição |
|---|---|
| Problema | Classificação binária: transação **legítima** x **fraudulenta** |
| Dados | Base pública de transações de cartão de crédito (ver `docs/dicionario-de-dados.md`) |
| Saída do modelo | Probabilidade de fraude + classe prevista por transação |
| Entrega analítica | Dashboard Power BI com KPIs de fraude e de desempenho do modelo |
| Fora do escopo (v1) | Scoring em tempo real / API em produção |

Escopo detalhado: [`docs/escopo.md`](docs/escopo.md)

## 2. Pipeline

```
data/raw  ──▶  ETL (Python)  ──▶  data/processed  ──▶  Modelo ML  ──▶  Power BI
                src/etl/                               src/models/     powerbi/
```

1. **Extract** — leitura da base bruta (`src/etl/extract.py`)
2. **Transform** — limpeza, tipagem, tratamento de desbalanceamento, features (`src/etl/transform.py`, `src/features/build_features.py`)
3. **Load** — gravação dos datasets tratados em `data/processed/` (`src/etl/load.py`)
4. **Modelagem** — treino, validação e comparação de algoritmos (`src/models/train_model.py`)
5. **Avaliação** — métricas apropriadas a classes desbalanceadas (`src/models/evaluate.py`)
6. **Dashboard** — Power BI consome `data/processed/` e os arquivos de resultados (`powerbi/`)

## 3. Estrutura do repositório

```
deteccao-fraudes-cartoes/
├── data/
│   ├── raw/            # base original (não versionada)
│   ├── interim/        # dados intermediários do ETL
│   ├── processed/      # datasets prontos para modelo e Power BI
│   └── external/       # dados de apoio (ex.: tabelas auxiliares)
├── notebooks/
│   ├── 01_analise_exploratoria.ipynb
│   ├── 02_preparacao_dados.ipynb
│   ├── 03_modelagem.ipynb
│   └── 04_avaliacao_e_export_powerbi.ipynb
├── src/
│   ├── config.py       # caminhos e parâmetros centrais
│   ├── etl/            # extract / transform / load
│   ├── features/       # engenharia de atributos
│   ├── models/         # treino, predição e avaliação
│   └── utils/          # logger e helpers
├── powerbi/            # dashboard, medidas DAX e documentação do modelo semântico
├── reports/
│   ├── figures/        # gráficos gerados
│   └── acompanhamento/ # relatórios de acompanhamento do grupo
├── docs/               # escopo, indicadores, dicionário de dados, plano de atividades
└── tests/              # testes das funções de ETL e features
```

## 4. Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

python -m src.etl.run_pipeline          # executa o ETL completo
python -m src.models.train_model        # treina e salva o modelo
python -m src.models.evaluate           # gera métricas e exports para o Power BI
```

Depois, abrir `powerbi/dashboard-fraudes.pbix` e atualizar as fontes apontando para `data/processed/`.

## 5. Indicadores do dashboard

Resumo (detalhe em [`docs/indicadores-dashboard.md`](docs/indicadores-dashboard.md)):

- Volume e valor total transacionado no período
- Nº e % de transações classificadas como fraude
- Valor financeiro em risco (soma das transações suspeitas)
- Distribuição de fraudes por faixa de valor, hora do dia e categoria
- Desempenho do modelo: Recall, Precision, F1, AUC-PR e matriz de confusão
- Evolução temporal da taxa de fraude

## 6. Divisão de atividades

Ver [`docs/plano-de-atividades.md`](docs/plano-de-atividades.md).

## 7. Status

Ver [`reports/acompanhamento/`](reports/acompanhamento/) para o histórico de acompanhamentos.
