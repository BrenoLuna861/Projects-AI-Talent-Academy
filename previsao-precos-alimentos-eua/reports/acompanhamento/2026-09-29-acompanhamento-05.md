# Acompanhamento 05 - 29/09/2026

**Integrantes:** Breno Luna e Paula Carlesso

## O que o grupo concluiu desde o último acompanhamento?

Montamos o dashboard no Power BI, completamos a análise exploratória com os pontos pedidos na
revisão e deixamos o repositório com tudo o que é preciso para abrir o painel.

## Principais entregas/evidências

| Entrega | Onde |
|---|---|
| Dashboard com 4 páginas (Panorama, Série temporal, Previsão, Confiabilidade), menu lateral e identidade visual da White Cube | `powerbi/dashboard/` |
| CSVs do dashboard versionados | `data/processed/powerbi/` |
| Índice de completude das séries | `notebooks/01_analise_exploratoria.ipynb`, seção 2 |
| Volatilidade em gráfico (15 mais voláteis) e por categoria | notebook 01, seção 6 |
| Gasolina no mesmo formato da sazonalidade: mapa de correlação com os alimentos e padrão sazonal dos combustíveis | notebook 01, seção 8 |
| Público-alvo do projeto | `docs/escopo.md` |

## Resultados

- Completude: 86% da base no período todo; mediana de 99% por série. Cinco séries ficam abaixo de 75% e saem da modelagem.
- Volatilidade típica de 2,8% ao mês; ovos, hortaliças, energia e frutas ficam bem acima.
- A gasolina fica cerca de 7% mais barata em dez/jan e 5% mais cara em jun/jul (temporada de viagens nos EUA).

## Dificuldades encontradas

- O Power BI Desktop recusou abrir o projeto por diferença de versão do modelo (1600 x 1606). Resolvido atualizando o nível de compatibilidade.
- A coluna com o nome dos produtos em português (`item_pt`) não existe no CSV original do Kaggle; ela é criada no ETL. O dashboard usa os CSVs tratados.

## Próximas etapas

| Etapa | Responsável | Prazo |
|---|---|---|
| Revisão final do layout do dashboard | Paula | 30/09 |
| Slides e ensaio da apresentação | Breno e Paula | 30/09 |
| Entrega | Breno e Paula | 01/10 |
