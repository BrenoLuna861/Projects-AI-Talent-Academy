"""Gera uma base sintética com o mesmo schema da base do curso.

Serve para rodar o pipeline inteiro sem depender do Google Drive — em
testes, em CI, ou quando alguém do grupo ainda não baixou os CSVs.
NÃO substitui a base real: os números que saem daqui não valem como
resultado do projeto.

Uso:
    python -m tools.gerar_dados_exemplo --linhas 20000 --destino data/raw
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def gerar(linhas: int = 20_000, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)

    n_clientes, n_cartoes, n_lojistas, n_categorias = 400, 600, 200, 8

    categorias = pd.DataFrame({
        "id_categoria": range(1, n_categorias + 1),
        "nome": [f"categoria_{i}" for i in range(1, n_categorias + 1)],
    })
    clientes = pd.DataFrame({
        "id_cliente": range(1, n_clientes + 1),
        "nome": [f"cliente_{i}" for i in range(1, n_clientes + 1)],
        "telefone": rng.choice([None, "8799999999"], n_clientes, p=[0.1, 0.9]),
    })
    cartoes = pd.DataFrame({
        "id_cartao": range(1, n_cartoes + 1),
        "id_cliente": rng.integers(1, n_clientes + 1, n_cartoes),
    })
    lojistas = pd.DataFrame({
        "id_lojista": range(1, n_lojistas + 1),
        "nome": [f"lojista_{i}" for i in range(1, n_lojistas + 1)],
        "id_categoria": rng.integers(1, n_categorias + 1, n_lojistas),
    })

    inicio = pd.Timestamp("2026-01-01")
    minutos = np.sort(rng.integers(0, 60 * 24 * 180, linhas))
    transacoes = pd.DataFrame({
        "id_transacao": range(1, linhas + 1),
        "id_cartao": rng.integers(1, n_cartoes + 1, linhas),
        "id_lojista": rng.integers(1, n_lojistas + 1, linhas),
        "valor": np.round(rng.lognormal(3.8, 1.1, linhas), 2),
        "data_hora": inicio + pd.to_timedelta(minutos, unit="m"),
        "canal": rng.choice(["presencial", "online"], linhas, p=[0.6, 0.4]),
    })

    # Sinal plantado de propósito, para o pipeline ter o que aprender:
    # madrugada + online + valor muito baixo ou muito alto elevam o risco.
    hora = transacoes["data_hora"].dt.hour
    risco = (
        0.004
        + 0.03 * ((hora >= 1) & (hora < 3))
        + 0.02 * (transacoes["canal"] == "online")
        + 0.05 * (transacoes["valor"] <= 5)
        + 0.02 * (transacoes["valor"] > 1500)
    )
    contestada = rng.random(linhas) < risco
    contestacoes = pd.DataFrame({
        "id_transacao": transacoes.loc[contestada, "id_transacao"].values,
        "motivo": "nao reconhece a compra",
    })

    # Sujeira proposital, para a quarentena ter o que separar
    sujas = transacoes.sample(max(linhas // 200, 1), random_state=seed).copy()
    sujas["valor"] = 0
    transacoes = pd.concat([transacoes, sujas], ignore_index=True)

    return {
        "transacoes": transacoes,
        "cartoes": cartoes,
        "clientes": clientes,
        "lojistas": lojistas,
        "categorias": categorias,
        "contestacoes": contestacoes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--linhas", type=int, default=20_000)
    parser.add_argument("--destino", type=str, default="data/raw")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    destino = Path(args.destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nome, df in gerar(args.linhas, args.seed).items():
        df.to_csv(destino / f"{nome}.csv", index=False)
        print(f"{nome}.csv: {len(df)} linhas")


if __name__ == "__main__":
    main()
