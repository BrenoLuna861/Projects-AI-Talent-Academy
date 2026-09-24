# Dashboard Power BI

O `.pbix` é montado pela Paula a partir dos CSVs de `data/processed/powerbi/`.
Antes de abrir, rodar o pipeline completo (ver README principal).

## Importação

Obter dados > Pasta > `data/processed/powerbi/` e carregar todos os CSVs.
Conferir no Power Query:

- `data`, `data_base`, `data_alvo`: tipo **Data**
- `preco*`, `faixa_*`, `erro*`, métricas: **Número decimal** (o CSV usa ponto como separador;
  se o Power BI estiver em pt-BR, usar *Alterar tipo > Usando localidade > Inglês (EUA)*)
- `imputado`, `ativa`, `serie_agregada`: **Verdadeiro/Falso**

## Calendário

Tabela calculada:

```DAX
dCalendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2015, 1, 1 ), DATE ( 2026, 12, 1 ) ),
    "ano", YEAR ( [Date] ),
    "mes", MONTH ( [Date] ),
    "mes_ano", FORMAT ( [Date], "mmm/yy" )
)
```

Renomear a coluna `Date` para `data` e marcar como tabela de datas.

## Relacionamentos

| De | Para | Cardinalidade |
|---|---|---|
| `fato_precos[serie_id]` | `dim_item[serie_id]` | muitos para um |
| `previsao_futura[serie_id]` | `dim_item[serie_id]` | muitos para um |
| `previsoes_teste[serie_id]` | `dim_item[serie_id]` | muitos para um |
| `metricas_por_item[serie_id]` | `dim_item[serie_id]` | muitos para um |
| `sazonalidade[serie_id]` | `dim_item[serie_id]` | muitos para um |
| `fato_precos[data]` | `dCalendario[data]` | muitos para um |
| `previsoes_teste[data_alvo]` | `dCalendario[data]` | muitos para um |

`metricas_modelos` e `metricas_por_categoria` ficam soltas (só filtram por modelo/categoria
dentro da própria tabela).

Filtrar a categoria sempre por `dim_item[categoria]`, que já vem corrigida.

## Medidas

Todas em [`medidas.dax`](medidas.dax). As páginas e indicadores estão descritos em
[`../docs/indicadores-dashboard.md`](../docs/indicadores-dashboard.md).

## Cuidados

- Na página de desempenho, sempre deixar uma segmentação de `modelo`; sem ela, o WAPE mistura todos os modelos.
- Meses interpolados (`imputado = TRUE`) devem aparecer com marcador diferente no gráfico de linha. Out/2025 é quase todo interpolado.
- Não comparar primeiro mês com último mês de itens sazonais; usar `variacao_12m_pct` da `dim_item`.
