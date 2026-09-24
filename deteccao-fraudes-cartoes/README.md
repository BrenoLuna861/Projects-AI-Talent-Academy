# Detecção de Fraudes em Cartões — Machine Learning + Dashboard

Projeto do **AI Talent Academy** — Grupo 1.

**Autores:** Breno Luna ([@BrenoLuna861](https://github.com/BrenoLuna861)) · Paula Carlesso

Modelo de classificação que estima a probabilidade de uma transação de cartão
ser fraudulenta, sobre a base relacional usada ao longo do curso, com os
resultados apresentados em um dashboard no Power BI.

---

## 1. Base e rótulo

Seis tabelas: `transacoes`, `cartoes`, `clientes`, `lojistas`, `categorias` e
`contestacoes` — as mesmas das aulas 2, 5, 6, 7, 8, 9 e 10.

O rótulo vem da tabela `contestacoes`: transação contestada = `fraude = 1`. É um
proxy, com limitações documentadas em [`docs/escopo.md`](docs/escopo.md) — nem
toda contestação é fraude, e nem toda fraude é contestada.

## 2. Pipeline

```
data/raw ──▶ quarentena ──▶ unify ──▶ rótulo ──▶ features ──▶ modelo ──▶ Power BI
  6 CSVs     src/etl/       src/etl/  contestacoes  src/features/  src/models/
```

| Etapa | Módulo | O que faz |
|---|---|---|
| Extract | `src/etl/extract.py` | Baixa do Drive se faltar e valida o schema das 6 tabelas |
| Quarentena | `src/etl/transform.py` | Marca `motivo_rejeicao` e separa válidas de rejeitadas |
| Unify | `src/etl/build_dataset.py` | Junta as tabelas resolvendo a colisão de `nome` |
| Rótulo | `src/etl/build_dataset.py` | `fraude = 1` para transações contestadas |
| Features | `src/features/build_features.py` | Atributos construídos só com o passado de cada transação |
| Treino | `src/models/train_model.py` | Split temporal + 3 algoritmos |
| Avaliação | `src/models/evaluate.py` | Métricas de base desbalanceada + escolha do limiar |
| Export | `src/models/predict_model.py` | Gera os CSVs que o Power BI consome |

Herda duas ideias direto das aulas: a **quarentena de dados** do pipeline
PySpark da Aula 10, e os **padrões suspeitos** investigados na Aula 08 (teste de
cartão, concentração de madrugada, taxa de contestação por lojista), que aqui
viram features do modelo.

## 3. Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python -m src.etl.run_pipeline      # ETL completo (baixa os CSVs na primeira vez)
python -m src.models.train_model    # treina os 3 modelos
python -m src.models.evaluate       # métricas + escolha do limiar
python -m src.models.predict_model  # exporta para o Power BI
```

Sem acesso ao Drive, dá para rodar tudo com dados sintéticos de mesmo schema:

```bash
python -m tools.gerar_dados_exemplo --linhas 20000 --destino data/raw
```

> Os números que saem da base sintética **não valem como resultado** — ela serve
> só para validar que o código roda.

## 4. Decisões que sustentam o resultado

**Split temporal.** Os últimos 25% do período viram teste. Fraude evolui; split
aleatório faria o modelo treinar com o futuro e inflaria as métricas.

**Nenhuma feature olha o futuro.** Média do cartão, contagem de transações e
taxa de contestação do lojista usam `expanding().shift(1)`. A taxa do lojista é
o caso mais perigoso: sem o `shift`, o rótulo da linha entra na feature que
deveria prevê-lo.

**O limiar é escolhido, não herdado.** Com ~1% de fraude, quase nada alcança 50%
de probabilidade — no limiar padrão o modelo simplesmente nunca acusa. O
`escolher_limiar()` exige um recall mínimo (70% por padrão) e, entre os cortes
que cumprem isso, fica com o de maior precisão, que é o que menos sobrecarrega
quem revisa os alertas.

**Acurácia não aparece.** Prever "nunca é fraude" acerta 99% das vezes e não
serve para nada. As métricas são recall, precision, F1 e AUC-PR.

## 5. Estrutura

```
deteccao-fraudes-cartoes/
├── data/              raw · interim (quarentena) · processed (dataset e saídas)
├── docs/              escopo, dicionário de dados, indicadores, plano
├── notebooks/         EDA, preparação, modelagem, avaliação
├── powerbi/           medidas DAX, modelo semântico e layout
├── reports/           figuras e relatórios de acompanhamento
├── src/               config, etl, features, models, utils
├── tests/             testes de quarentena, features e rótulo
└── tools/             gerador de base sintética
```

## 6. Indicadores do dashboard

Volume e valor transacionado · taxa de alerta e valor em risco · fraude por
faixa de valor, hora e categoria · transações de madrugada e padrão de teste de
cartão · recall, precision, F1 e matriz de confusão. Detalhe em
[`docs/indicadores-dashboard.md`](docs/indicadores-dashboard.md).

## 7. Divisão de atividades

| Autor | Frentes |
|---|---|
| **Breno Luna** | ETL, modelagem e estrutura do repositório |
| **Paula Carlesso** | Análise exploratória, dashboard Power BI e documentação |

Detalhe por etapa em [`docs/plano-de-atividades.md`](docs/plano-de-atividades.md).

## 8. Status

Pipeline, modelos e avaliação implementados e testados (`pytest -q`) com base
sintética. Falta rodar sobre a base real do curso e construir o `.pbix`.
Histórico em [`reports/acompanhamento/`](reports/acompanhamento/).
