# Previsão de preços de alimentos e energia nos EUA

Projeto final do **AI Talent Academy**, Grupo 1.

**Autores:** Breno Luna ([@BrenoLuna861](https://github.com/BrenoLuna861)) · Paula Carlesso

Análise de série temporal e previsão do preço médio de 60 itens do dia a dia nos EUA
(ovos, leite, carne, café, gasolina, energia elétrica...) com 3 meses de antecedência,
a partir da série mensal do Bureau of Labor Statistics de 2015 a 2026. Comparamos
modelos clássicos de série temporal (SARIMA, Holt-Winters) com machine learning, e os
resultados vão para um dashboard no Power BI.

---

## Por que esse tema

A ideia inicial era detecção de fraude em cartão, mas as bases públicas desse tema já
foram exploradas à exaustão. Por sugestão do professor, trocamos por uma base recente
(atualizada em set/2026), de fonte oficial e ainda pouco trabalhada no Kaggle:
[US Grocery and Gas Prices 2015-2026](https://www.kaggle.com/datasets/harshitsama/us-grocery-and-gas-prices-2015-2026).

A pergunta do projeto: **dá para prever o preço de um item de mercado 3 meses à frente
melhor do que simplesmente repetir o preço de hoje?**

## Resultado em uma frase

Dá, mas pouco e não em tudo. O modelo final, a média das previsões de um gradient
boosting (ML) e de um SARIMA por item, erra em média 3,8% contra 4,1% da regra ingênua
e ganha dela nos 4 períodos de teste. O ganho vem quase todo de frutas (sazonalidade),
ovos e carnes; em aves, bebidas e laticínios repetir o último preço continua sendo melhor.

| Modelo | Tipo | WAPE médio nos 4 cortes | Ganho sobre o ingênuo |
|---|---|---|---|
| **combinado (GB + SARIMA)** | híbrido | **3,80%** | **7,4%** |
| gradient_boosting | ML | 3,88% | 5,5% |
| random_forest | ML | 3,92% | 4,3% |
| ingênuo (preço de hoje) | regra | 4,10% | - |
| sarima | série temporal | 4,13% | -0,6% |
| ridge | ML | 4,21% | -2,5% |
| ets (Holt-Winters) | série temporal | 4,26% | -3,8% |
| sazonal ingênuo | regra | 5,47% | -33% |

Detalhes em [`notebooks/04_avaliacao_e_export_powerbi.ipynb`](notebooks/04_avaliacao_e_export_powerbi.ipynb)
e [`notebooks/05_series_temporais_e_granularidade.ipynb`](notebooks/05_series_temporais_e_granularidade.ipynb).

## Série temporal e granularidade

O notebook 05 olha os dados como série temporal:

- **Decomposição STL** de cada série em tendência, sazonalidade e ruído. Quase todas têm
  tendência forte; sazonalidade forte só em frutas, presunto e energia elétrica.
- **Estacionariedade (ADF):** o preço não é estacionário em 92% das séries; a variação
  mensal é em 87%. Por isso os modelos trabalham com variação, não com o preço.
- **Autocorrelação (ACF/PACF):** o preço de hoje explica quase todo o de amanhã (0,95 no
  1º lag da gasolina), o que torna o ingênuo um adversário difícil.
- **Granularidade temporal:** para prever o preço médio do próximo trimestre, usar dados
  mensais erra 2,6-2,7%, contra 3,3% usando dados já agregados por trimestre. Mantivemos
  a granularidade mensal, a mais fina disponível. Anual deixa só ~11 pontos por série.
- **Granularidade de produto:** séries agregadas ("All uncooked ground beef") são menos
  voláteis e mais previsíveis que os itens específicos que resumem.

## Pipeline

```
data/raw  ->  ETL  ->  grade mensal  ->  features  ->  modelos  ->  CSVs  ->  Power BI
              src/etl                    src/features  src/models   data/processed/powerbi
```

1. **Extract** (`src/etl/extract.py`): lê o CSV longo e confere o schema.
2. **Transform** (`src/etl/transform.py`):
   - corrige categorias erradas do dataset (café veio como "Beef", batata chips como "Vegetables");
   - separa linhas inválidas em vez de apagar;
   - coloca cada série numa grade mensal e interpola buracos de até 2 meses
     (o principal é out/2025, quando o shutdown do governo americano interrompeu a coleta);
   - resume cada série e marca quais ficam fora da modelagem (descontinuadas ou com buracos demais).
3. **Features** (`src/features/build_features.py`): variações recentes, distância da média
   de 12 meses, volatilidade, sazonalidade do ano anterior, média da categoria e gasolina.
   Toda feature usa só informação disponível no mês-base (tem teste para isso).
4. **Modelos** (`src/models/`): ML global para todas as séries (`train_model.py`), SARIMA e
   Holt-Winters por item (`series_temporais.py`) e a combinação dos dois, todos prevendo a
   variação em 3 meses. Separação temporal e backtest com 4 cortes.
5. **Exportação**: tabelas prontas para o Power BI em `data/processed/powerbi/`.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Baixe o dataset do Kaggle e extraia os CSVs em `data/raw/` (ver [`data/README.md`](data/README.md)). Depois:

```bash
python -m src.etl.run_pipeline      # ETL + base de modelagem
python -m src.models.train_model    # treino (corte dez/2024)
python -m src.models.evaluate       # teste + backtest (~4 min, por causa do SARIMA/ETS)
python -m src.models.predict_model  # modelo final, previsão e exportação
pytest                              # testes
```

No total leva uns 5 minutos num notebook comum.

## Estrutura

```
├── data/
│   ├── raw/          CSVs do Kaggle (não versionados)
│   ├── interim/      grade mensal e tabela de itens
│   └── processed/    base de modelagem e powerbi/
├── docs/             escopo, dicionário de dados, indicadores, plano de atividades
├── notebooks/        01 EDA, 02 preparação, 03 modelagem, 04 avaliação/exportação,
│                     05 série temporal e granularidade
├── powerbi/          medidas DAX e orientação do dashboard
├── reports/          figuras e acompanhamentos do grupo
├── src/              código do pipeline
└── tests/
```

## Divisão do trabalho

| Autor | Frentes |
|---|---|
| Breno Luna | ETL, modelagem e estrutura do repositório |
| Paula Carlesso | Análise exploratória, dashboard Power BI e documentação |

Detalhe em [`docs/plano-de-atividades.md`](docs/plano-de-atividades.md).

## Limitações

- Preços **nominais**. Nada foi corrigido pela inflação (o CPI subiu ~35% no período).
- **Média nacional**: esconde diferenças grandes entre regiões, marcas e tamanhos de embalagem.
- A faixa de previsão no dashboard vem dos quantis do erro no teste. É uma referência prática, não um intervalo de confiança formal.
- Granularidade limitada ao que o BLS publica: mensal e nacional. Não há dado semanal nem por região no dataset.
- A combinação GB + SARIMA foi escolhida depois de ver o backtest. Os mesmos 4 cortes serviram para escolher e para medir, então o ganho real tende a ser um pouco menor que 7%.
- Quem define o preço é o mercado; o modelo só enxerga o histórico do próprio preço, da categoria e da gasolina. Choques como gripe aviária ou tarifas não estão nos dados.

## Fonte

U.S. Bureau of Labor Statistics, Average Price Data (AP), U.S. city average, mensal,
sem ajuste sazonal. Compilado no Kaggle por harshitsama (licença CC0).
