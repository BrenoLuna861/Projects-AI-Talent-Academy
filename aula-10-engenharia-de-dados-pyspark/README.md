# Aula 10 — Engenharia de Dados com PySpark

**Grupo 1 — Breno Luna e Paula Carlesso**

Pipeline completo de engenharia de dados em Spark sobre a base de fraude em
cartão, em escala de 1 milhão de transações.

## Arquivo

| Arquivo | Descrição |
|---|---|
| `aula_10_engenharia_de_dados_pyspark.py` | Notebook exportado do Google Colab, com o pipeline dos seis passos |

## O pipeline

| Passo | Etapa | O que faz |
|---|---|---|
| 0 | Ambiente | Instala JDK 17 e PySpark, cria a `SparkSession` |
| 1 | **Extract** | Lê as seis tabelas CSV e imprime o schema de cada uma |
| 2 | **Transform com quarentena** | Marca cada transação com o motivo do problema em vez de descartar |
| 3 | **Unify** | Junta as tabelas e corrige a colisão de nomes de coluna |
| 4 | **Bifurcação** | Separa trilha normal e trilha de atenção por regra de negócio |
| 5 | **Load** | Grava o resultado em múltiplos destinos |
| 6 | **Reconciliação** | Confere que nenhuma linha sumiu ou duplicou no caminho |

## Quarentena de dados

O ponto central da aula. Em vez de `.dropna()` e `.filter()` — que apagam as
linhas problemáticas sem deixar rastro —, cada transação recebe uma coluna
`motivo_rejeicao` (campo obrigatório nulo, `id_transacao` duplicado, etc.) e o
pipeline separa `transacoes_validas` de `transacoes_rejeitadas`.

A diferença aparece quando alguém pergunta *"por que sumiram 40 mil linhas?"*:
com quarentena, a resposta está na tabela; sem ela, não há como responder.

O passo 6 fecha o raciocínio com um `assert` de reconciliação — a soma das
trilhas tem que bater com o total unificado, senão o pipeline falha em vez de
entregar número errado em silêncio.

## Perguntas de conferência

1. Quantas transações ficaram em quarentena e quantas foram para a trilha de atenção
2. Qual lojista teve o maior valor total transacionado considerando só a trilha normal

## Como executar

Exportado do Colab — a forma mais direta é abrir lá e rodar as células em ordem,
já que o passo 0 instala o Java e o Spark na própria sessão.

Localmente é preciso ter **Java 17** e PySpark:

```bash
pip install pyspark gdown
```
