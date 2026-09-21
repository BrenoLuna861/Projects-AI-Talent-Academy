# Aula 08 — Análise de Dados em Python (pandas)

**Grupo 1 — Breno Luna e Paula Carlesso**

Avaliação prática de pandas: 20 perguntas sobre a base de fraude em cartão usada
ao longo das aulas 2, 5, 6 e 7 do AI Talent Academy.

## Arquivo

| Arquivo | Descrição |
|---|---|
| `aula_08_analise_de_dados.py` | Notebook exportado do Google Colab, com as 20 respostas resolvidas |

## Base de dados

Seis tabelas em CSV, baixadas automaticamente do Google Drive pelas primeiras
células do script:

`transacoes` · `clientes` · `cartoes` · `lojistas` · `categorias` · `contestacoes`

## O que o script responde

| Bloco | Perguntas | Conteúdo |
|---|---|---|
| Carregando e explorando | 1–4 | Contagem de linhas, `dtype`, média e desvio padrão, valores ausentes |
| Filtrando e selecionando | 5–8 | Filtros por valor, `value_counts`, busca por id, valores distintos |
| Agregando | 9–12 | `groupby`, `idxmax`, merge de três tabelas, `pivot_table` |
| Juntando tabelas | 13–15 | Merge encadeado, anti-join para achar clientes e lojistas sem movimento |
| Visualizando | 16–17 | Percentil 95 e histograma dos valores |
| Investigação | 18–20 | Taxa de contestação por lojista, transações de madrugada e detecção do padrão de **teste de cartão** |

As três últimas perguntas são a parte interessante: saem da estatística
descritiva e entram em detecção de comportamento suspeito — um lojista com taxa
de contestação fora da curva, concentração de transações entre 1h e 3h da manhã,
e cartões com 4 ou mais transações de até R$ 5 no mesmo lojista no mesmo dia.

## Como executar

O script foi gerado pelo Colab e depende do ambiente dele (`/content/csv` e o
download via `gdown`). O caminho mais simples é abrir no Google Colab e rodar as
células em ordem.

Para rodar localmente, instale as dependências e ajuste `PASTA_DADOS` para a
pasta onde os CSVs estiverem:

```bash
pip install pandas matplotlib gdown
```
