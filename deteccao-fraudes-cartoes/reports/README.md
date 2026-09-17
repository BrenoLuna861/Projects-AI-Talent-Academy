# reports — Resultados e acompanhamentos

| Pasta | Conteúdo |
|---|---|
| `figures/` | Gráficos exportados pelos notebooks (PNG/SVG) — matriz de confusão, curva precision-recall, distribuições |
| `acompanhamento/` | Relatórios entregues ao professor/mentor a cada acompanhamento |

## Acompanhamentos

- Nome do arquivo: `AAAA-MM-DD-acompanhamento-NN.md`
- Base: copie `acompanhamento/MODELO-acompanhamento.md`
- Cada entrega citada deve apontar para o caminho do arquivo no repositório — é isso que transforma "definimos o escopo" em evidência verificável.

## Figuras

Gere as figuras pelo notebook, salvando em `reports/figures/`:

```python
from src.config import FIGURES_DIR
plt.savefig(FIGURES_DIR / "matriz-confusao.png", dpi=150, bbox_inches="tight")
```

Use nomes descritivos (`curva-precision-recall-random-forest.png`), não `grafico1.png`.
