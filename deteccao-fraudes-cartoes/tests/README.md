# tests — Testes automatizados

```bash
pytest -q
```

## O que está coberto

| Arquivo | Testa |
|---|---|
| `test_transform.py` | Quarentena não perde linha, separa os quatro motivos, converte tipos |
| `test_features.py` | Marcação de madrugada, ausência de vazamento na média do cartão e na taxa do lojista, canal binário |
| `test_build_dataset.py` | Rótulo marca só as contestadas e ignora contestação órfã |

Os dois testes de vazamento são os mais importantes do projeto. Eles verificam
que a **primeira** transação de cada cartão e de cada lojista não tem média nem
taxa histórica preenchida — se tiver, é porque o `shift(1)` foi perdido em
alguma alteração e o modelo passou a enxergar o futuro. Esse tipo de bug não
quebra nada: ele só faz as métricas ficarem ótimas e o modelo falhar na vida
real.

## O que vale acrescentar

- Contagem de linhas preservada entre unify e features.
- `exportar_predicoes` gerando exatamente as colunas esperadas pelo Power BI.
- `escolher_limiar` devolvendo corte válido quando nenhum limiar atinge o recall mínimo.
