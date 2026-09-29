# Dicionário de dados

## Base bruta: `data/raw/us_average_prices_monthly.csv`

8.869 linhas, 74 séries, jan/2015 a jul/2026. Uma linha por item-mês publicado; quando o
BLS não publica, a linha simplesmente não existe.

| Coluna | Tipo | Descrição |
|---|---|---|
| `date` | data | Primeiro dia do mês de referência |
| `year`, `month` | int | Ano e mês (redundantes com `date`) |
| `item` | texto | Nome do item no BLS, ex.: `Eggs, grade A, large` |
| `unit` | texto | Unidade do preço, ex.: `doz.`, `lb. (453.6 gm)`, `gallon/3.785 liters` |
| `category` | texto | Categoria atribuída pelo autor do dataset (12 valores, com erros) |
| `price` | float | Preço médio em US$ |
| `series_id` | texto | Código da série no BLS, ex.: `APU0000708111` |

Os outros dois arquivos do Kaggle (`_wide` e `_item_summary`) não são usados: o pipeline
recalcula tudo a partir do arquivo longo.

## `data/interim/precos_mensais.parquet`

Grade mensal contínua por série.

| Coluna | Descrição |
|---|---|
| `serie_id` | Código BLS |
| `data` | Mês |
| `preco` | Preço em US$ (vazio se o buraco for maior que 2 meses) |
| `imputado` | `True` se o preço foi interpolado |
| `item`, `unidade` | Do arquivo bruto |
| `categoria` | Categoria corrigida, em português |
| `categoria_original` | Categoria como veio do dataset |

## `data/interim/itens.parquet` (e `powerbi/dim_item.csv`)

Uma linha por série.

| Coluna | Descrição |
|---|---|
| `inicio`, `fim` | Primeiro e último mês publicado |
| `meses_publicados` | Meses com preço real |
| `meses_na_grade`, `meses_faltando` | Tamanho da grade e quantos meses o BLS não publicou |
| `ativa` | Publicada até 2 meses antes do último mês da base |
| `item_pt` | Nome curto em português, para exibir no dashboard. Só no `dim_item.csv` e no `previsao_futura.csv` |
| `serie_agregada` | Série "All ..." que agrega outras (ex.: All Uncooked Beef Steaks) |
| `media_12_inicio`, `media_12_fim` | Média dos 12 primeiros e 12 últimos meses |
| `variacao_12m_pct` | Variação entre as duas médias; vazio para série inativa |
| `motivo_exclusao` | Por que a série não entra na modelagem (`descontinuada`, `historico_curto`, `muitos_buracos`) |
| `vol_mensal_pct` | Desvio-padrão da variação mensal (%). Só no `dim_item.csv` |
| `forca_tendencia`, `forca_sazonalidade` | 0 a 1, da decomposição STL (notebook 05). Só séries modeladas, só no `dim_item.csv` |

## `data/processed/base_modelagem.parquet`

Uma linha por (série, mês-base). Features descritas em `notebooks/02_preparacao_dados.ipynb`.

| Coluna | Descrição |
|---|---|
| `data_base` | Mês em que a previsão é feita (t) |
| `data_alvo` | t + 3 meses |
| `preco`, `preco_alvo` | Preço em t e em t+3 |
| `alvo` | `log(preco_alvo / preco)` |
| `alvo_imputado` | Linhas com alvo interpolado não entram em treino nem teste |

## Saídas para o Power BI (`data/processed/powerbi/`)

**`fato_precos.csv`**: `serie_id`, `data`, `preco`, `imputado`. Histórico completo.

**`previsoes_teste.csv`**: uma linha por série, mês-base e modelo no período de teste.
Modelos: `ingenuo`, `sazonal_ingenuo` (regras), `ridge`, `random_forest`, `gradient_boosting`
(ML), `sarima`, `ets` (série temporal) e `combinado` (média de gradient boosting e SARIMA).

| Coluna | Descrição |
|---|---|
| `preco_base` | Preço no mês-base |
| `preco_real` | Preço que de fato ocorreu em `data_alvo` |
| `preco_previsto` | Previsão do modelo |
| `erro`, `erro_abs`, `erro_pct` | previsto - real, em US$ e em % do real |

**`previsao_futura.csv`**: previsão do modelo final a partir do último mês disponível.
São 59 séries: a alface romana fica de fora porque os meses mais recentes dela estão faltando.

| Coluna | Descrição |
|---|---|
| `preco_previsto` | Previsão para `data_alvo` |
| `faixa_inferior`, `faixa_superior` | Quantis 10% e 90% do erro no teste, por categoria |
| `variacao_prevista_pct` | Variação prevista em relação ao preço atual |

**`metricas_modelos.csv`**: uma linha por corte de teste e modelo (`mae_usd`, `mape`,
`wape`, `vies_pct`, `ganho_vs_ingenuo_pct`, `series_melhor_que_ingenuo_pct`).

**`metricas_por_categoria.csv`** e **`metricas_por_item.csv`**: `mape`, `wape` e nº de
previsões por modelo, no teste principal.

**`sazonalidade.csv`**: `serie_id`, `mes`, `desvio_sazonal_pct` (quanto o preço daquele mês
fica, em média, acima ou abaixo da média móvel de 12 meses).
