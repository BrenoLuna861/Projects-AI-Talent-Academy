# Notebooks

Ordem de execução — cada notebook assume que o anterior já rodou.

| Notebook | O que faz | Entrada | Saída |
|---|---|---|---|
| `01_analise_exploratoria.ipynb` | EDA: volume, nulos, desbalanceamento, distribuição de valores e fraudes por hora | `data/raw/` | Gráficos em `reports/figures/` e conclusões para o ETL |
| `02_preparacao_dados.ipynb` | Aplica e valida o pipeline de `src/etl/` | `data/raw/` | `data/processed/transacoes_tratadas.parquet` |
| `03_modelagem.ipynb` | Treina e compara os algoritmos candidatos | `data/processed/` | Modelos em `models/` + tabela comparativa |
| `04_avaliacao_e_export_powerbi.ipynb` | Curva precision-recall, escolha do limiar e export para o BI | `models/` | `predicoes.csv` e `metricas_modelo.csv` |

## Regras do grupo

- **Notebook explora; `src/` executa.** Quando um trecho virar rotina, mova para um módulo em `src/` e importe de volta no notebook. Isso evita código duplicado e mantém o pipeline reproduzível.
- **Limpe as saídas antes do commit** (`Kernel → Restart & Clear Output`). Notebook com output gera diffs enormes e conflitos praticamente insolúveis no Git.
- **Um notebook por vez, por pessoa.** Dois integrantes editando o mesmo `.ipynb` na mesma branch quase sempre termina em conflito manual.
- Todo notebook começa com `sys.path.append("..")` para enxergar o pacote `src`.
