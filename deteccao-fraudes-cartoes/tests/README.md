# tests — Testes automatizados

Rodar a partir da raiz do projeto:

```bash
pytest -q
```

## O que já está coberto

| Arquivo | Testa |
|---|---|
| `test_features.py` | Derivação de `hora_do_dia` e das faixas de valor |
| `test_transform.py` | Remoção de duplicatas e padronização de tipos |

## O que vale testar a seguir

- Nenhuma linha perdida ou duplicada ao longo do pipeline de ETL.
- Coluna alvo contendo apenas 0 e 1 após o `transform`.
- `exportar_predicoes` gerando exatamente as colunas que o Power BI espera.

Testes aqui não são burocracia: eles pegam o erro silencioso — uma feature que
some, um filtro que corta linhas demais — que só apareceria no dashboard com o
número errado já na tela.
