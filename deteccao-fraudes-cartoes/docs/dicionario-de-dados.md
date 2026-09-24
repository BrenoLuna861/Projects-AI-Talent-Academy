# Dicionário de Dados

**Autores:** Breno Luna e Paula Carlesso

Base relacional de fraude em cartão usada ao longo do AI Talent Academy
(aulas 2, 5, 6, 7, 8, 9 e 10). Seis tabelas em CSV, baixadas do Google Drive
pelo próprio pipeline (`src/etl/extract.py`).

> Os tipos abaixo são os observados nos notebooks das aulas. Se algum nome de
> coluna divergir, ajuste `SCHEMA_ESPERADO` em `src/config.py` — o validador
> em `src/utils/schema.py` acusa a diferença antes do pipeline quebrar.

## Tabelas brutas — `data/raw/`

### `transacoes.csv` — tabela fato
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_transacao` | int | Chave primária |
| `id_cartao` | int | FK para `cartoes` |
| `id_lojista` | int | FK para `lojistas` |
| `valor` | float | Valor da transação em R$ |
| `data_hora` | string → datetime | Momento da transação (convertido no ETL) |
| `canal` | string | `presencial` ou `online` |

### `cartoes.csv`
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_cartao` | int | Chave primária |
| `id_cliente` | int | FK para `clientes` |

### `clientes.csv`
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_cliente` | int | Chave primária |
| `nome` | string | Nome do titular |
| `telefone` | string | Contém nulos (visto na Aula 08) |

### `lojistas.csv`
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_lojista` | int | Chave primária |
| `nome` | string | Renomeado para `nome_lojista` no unify |
| `id_categoria` | int | FK para `categorias` |

### `categorias.csv`
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_categoria` | int | Chave primária |
| `nome` | string | Renomeado para `nome_categoria` no unify |

### `contestacoes.csv` — origem do rótulo
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_transacao` | int | FK para `transacoes` — presença aqui define `fraude = 1` |

> **Colisão de nomes:** `nome` existe em `clientes`, `lojistas` e `categorias`.
> Sem renomear no merge, o pandas cria `nome_x` e `nome_y` e o código fica
> ilegível — foi exatamente o tropeço do Passo 3 da Aula 10. O `unificar()`
> em `src/etl/build_dataset.py` renomeia antes de juntar.

## Quarentena — `data/interim/`

`transacoes_rejeitadas.parquet` guarda as linhas que não entraram no dataset,
com a coluna `motivo_rejeicao`:

| Motivo | Regra |
|---|---|
| `campo obrigatorio nulo` | Falta `id_transacao`, `id_cartao`, `id_lojista`, `valor` ou `data_hora` |
| `id_transacao duplicado` | O id aparece mais de uma vez |
| `valor menor ou igual a zero` | `valor <= 0` |
| `data_hora invalida` | Não converte para datetime |

`transacoes_validas.parquet` tem o complemento. As duas somadas sempre batem
com o total original — há um `assert` garantindo isso.

## Dataset de modelagem — `data/processed/dataset_modelagem.parquet`

Features usadas pelo modelo (`COLUNAS_MODELO` em `src/features/build_features.py`):

| Feature | O que mede | Por que |
|---|---|---|
| `valor`, `log_valor` | Valor bruto e em escala log | A distribuição tem cauda longa |
| `hora_do_dia`, `dia_semana`, `fim_de_semana` | Quando aconteceu | Fraude se concentra em horários atípicos |
| `madrugada` | Entre 1h e 3h | Padrão achado na Aula 08 |
| `canal_online` | Online x presencial | Canal sem cartão presente tem risco diferente |
| `valor_baixo` | Até R$ 5 | Valor típico de teste de cartão |
| `media_valor_cartao_ate_agora` | Gasto médio anterior do cartão | Referência do comportamento normal |
| `razao_valor_media_cartao` | Valor / média histórica | Detecta salto fora do padrão |
| `qtd_transacoes_cartao_ate_agora` | Histórico do cartão | Cartão novo tem menos base de comparação |
| `minutos_desde_ultima_do_cartao` | Intervalo desde a última compra | Rajada de compras é sinal |
| `baixos_no_dia_ate_agora` | Transações de até R$5 no mesmo cartão/lojista/dia | Contagem do padrão de teste |
| `padrao_teste_cartao` | Flag do padrão da Aula 08 | 4+ ocorrências no mesmo dia |
| `qtd_transacoes_lojista_ate_agora` | Volume histórico do lojista | Contextualiza a taxa abaixo |
| `taxa_contestacao_lojista_ate_agora` | Contestações anteriores do lojista | Lojista problemático concentra fraude |

**Todas as features históricas usam `expanding().shift(1)`** — ou seja, só
informação anterior àquela transação. Sem isso, o modelo enxergaria o futuro
e as métricas seriam mentira.

## Saídas para o Power BI — `data/processed/`

### `predicoes.csv`
| Coluna | Descrição |
|---|---|
| `id_transacao` | Chave de ligação com `transacoes_dashboard` |
| `probabilidade_fraude` | Score entre 0 e 1 |
| `classe_prevista` | 1 = alerta, no limiar escolhido |
| `classe_real` | Rótulo observado (contestação) |
| `modelo` | Algoritmo que gerou a previsão |

### `transacoes_dashboard.csv`
Transações do período de teste com os campos de negócio: `valor`, `data_hora`,
`canal`, `nome_lojista`, `nome_categoria`, `hora_do_dia`, `faixa_valor`,
`madrugada`, `padrao_teste_cartao`.

### `metricas_modelo.csv`
| Coluna | Descrição |
|---|---|
| `modelo` | Nome do algoritmo |
| `metrica` | recall, precision, f1, auc_pr, auc_roc, matriz de confusão, taxa_alerta |
| `valor` | Valor da métrica |
| `limiar` | Ponto de corte usado |
| `data_execucao` | Timestamp |
