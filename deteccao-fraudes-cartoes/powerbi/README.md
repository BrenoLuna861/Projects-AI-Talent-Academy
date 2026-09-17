# Dashboard Power BI — Detecção de Fraudes

## Fontes de dados
O dashboard consome os arquivos gerados pelo pipeline Python:

| Tabela | Arquivo | Papel |
|---|---|---|
| `fTransacoes` | `data/processed/transacoes_tratadas.parquet` | Fato — transações tratadas |
| `fPredicoes` | `data/processed/predicoes.csv` | Fato — saída do modelo |
| `fMetricas` | `data/processed/metricas_modelo.csv` | Métricas de desempenho |
| `dCalendario` | Tabela DAX (`powerbi/dax/dCalendario.dax`) | Dimensão de datas |

## Modelo semântico
```
dCalendario[data] 1 ──── * fTransacoes[data]
fTransacoes[id_transacao] 1 ──── 1 fPredicoes[id_transacao]
```
- Relacionamento `fTransacoes` ↔ `fPredicoes` por `id_transacao` (cardinalidade 1:1, filtro único).
- `fMetricas` fica desconectada (tabela de apoio para a página de desempenho).
- Marcar `dCalendario` como tabela de datas.

## Passo a passo
1. **Obter dados → Pasta/Arquivo** apontando para `data/processed/`.
2. Ajustar tipos no Power Query (valor como decimal, datas como data/hora).
3. Criar `dCalendario` com o script em `powerbi/dax/dCalendario.dax`.
4. Colar as medidas de `powerbi/dax/medidas.dax` em uma tabela de medidas.
5. Montar as três páginas descritas em `docs/indicadores-dashboard.md`.
6. Salvar como `powerbi/dashboard-fraudes.pbix` (arquivo grande: considerar `.pbip` para versionar melhor no Git).

## Versionamento
O formato `.pbix` é binário e gera conflitos no Git. Sempre que possível,
salvar em **formato PBIP** (`Arquivo → Salvar como → Projeto do Power BI`),
que grava os metadados em arquivos de texto versionáveis.

## Padrão visual
- Fraude sempre na mesma cor de destaque (ex.: vermelho); legítima em cinza/neutro.
- KPIs no topo, detalhamento abaixo.
- Todo percentual acompanhado do número absoluto — 3% de fraude significa coisas diferentes em 1.000 e em 1.000.000 de transações.
