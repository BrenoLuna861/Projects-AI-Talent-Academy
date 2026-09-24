"""Limpeza, correção de categorias e regularização da grade mensal."""
import numpy as np
import pandas as pd

from src.config import MAX_MESES_INTERPOLACAO, MIN_MESES_HISTORICO
from src.utils.logger import get_logger

log = get_logger(__name__)

RENOMEAR = {
    "date": "data",
    "item": "item",
    "unit": "unidade",
    "category": "categoria_original",
    "price": "preco",
    "series_id": "serie_id",
}

CATEGORIAS = {
    "Bakery and grains": "Padaria e grãos",
    "Beef": "Carne bovina",
    "Dairy and fats": "Laticínios",
    "Drinks": "Bebidas",
    "Eggs": "Ovos",
    "Energy": "Energia",
    "Fruit": "Frutas",
    "Pantry and snacks": "Mercearia",
    "Pork and deli": "Suínos e frios",
    "Poultry": "Aves",
    "Vegetables": "Hortaliças",
}

# Itens que vieram com a categoria errada no dataset (café como "Beef",
# batata chips como "Vegetables") e os que vieram no balaio "Meat, broad category".
CORRECOES_CATEGORIA = {
    "APU0000717311": "Mercearia",       # Coffee
    "APU0000718311": "Mercearia",       # Potato chips
    "APU0000FC2101": "Carne bovina",    # All Uncooked Beef Roasts
    "APU0000FC4101": "Carne bovina",    # All Uncooked Other Beef
    "APU0000FD2101": "Suínos e frios",  # All Ham
}


def padronizar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=RENOMEAR)[list(RENOMEAR.values())].copy()
    df["data"] = pd.to_datetime(df["data"])
    df["categoria"] = df["categoria_original"].map(CATEGORIAS)
    corrigir = df["serie_id"].isin(CORRECOES_CATEGORIA)
    df.loc[corrigir, "categoria"] = df.loc[corrigir, "serie_id"].map(CORRECOES_CATEGORIA)

    sem_categoria = df["categoria"].isna()
    if sem_categoria.any():
        # categoria nova no dataset: mantém o nome original para não perder a linha
        df.loc[sem_categoria, "categoria"] = df.loc[sem_categoria, "categoria_original"]
        log.warning("Categorias sem tradução: %s", df.loc[sem_categoria, "categoria_original"].unique())
    return df


def validar_linhas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa linhas com problema em vez de apagar sem deixar rastro."""
    motivo = pd.Series(pd.NA, index=df.index, dtype="string")
    motivo[df["preco"].isna()] = "preco_nulo"
    motivo[motivo.isna() & (df["preco"] <= 0)] = "preco_nao_positivo"
    motivo[motivo.isna() & df.duplicated(["serie_id", "data"], keep="first")] = "duplicada"

    rejeitadas = df[motivo.notna()].assign(motivo=motivo[motivo.notna()])
    if len(rejeitadas):
        log.warning("%s linhas rejeitadas", len(rejeitadas))
    return df[motivo.isna()].copy(), rejeitadas


def regularizar_grade(df: pd.DataFrame, max_gap: int = MAX_MESES_INTERPOLACAO) -> pd.DataFrame:
    """Coloca cada série numa grade mensal contínua (do 1º ao último mês publicado).

    Buracos curtos são interpolados em escala log e marcados com imputado=True.
    Buracos maiores continuam vazios: melhor perder a linha do que inventar
    um ano inteiro de preço.
    """
    partes = []
    for sid, g in df.groupby("serie_id", sort=False):
        g = g.set_index("data").sort_index()
        grade = pd.date_range(g.index.min(), g.index.max(), freq="MS")
        g = g.reindex(grade)
        g.index.name = "data"

        faltando = g["preco"].isna()
        # tamanho de cada bloco de meses faltando
        bloco = (faltando != faltando.shift()).cumsum()
        tam_bloco = faltando.groupby(bloco).transform("sum")
        preencher = faltando & (tam_bloco <= max_gap)

        log_preco = np.log(g["preco"]).interpolate(method="linear", limit_area="inside")
        g.loc[preencher, "preco"] = np.exp(log_preco[preencher]).round(3)
        g["imputado"] = preencher
        g["serie_id"] = sid
        for col in ("item", "unidade", "categoria", "categoria_original"):
            g[col] = g[col].ffill().bfill()
        partes.append(g.reset_index())

    out = pd.concat(partes, ignore_index=True)
    log.info(
        "Grade mensal: %s linhas | %s interpoladas | %s ainda vazias",
        len(out), int(out["imputado"].sum()), int(out["preco"].isna().sum()),
    )
    return out


def resumir_itens(precos: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por série, usada como dimensão no Power BI e para filtrar a modelagem."""
    ultima_data = precos["data"].max()
    obs = precos[precos["preco"].notna() & ~precos["imputado"]]

    itens = obs.groupby("serie_id").agg(
        item=("item", "first"),
        unidade=("unidade", "first"),
        categoria=("categoria", "first"),
        categoria_original=("categoria_original", "first"),
        inicio=("data", "min"),
        fim=("data", "max"),
        meses_publicados=("preco", "size"),
    )
    total = precos.groupby("serie_id").size()
    itens["meses_na_grade"] = total
    itens["meses_faltando"] = itens["meses_na_grade"] - itens["meses_publicados"]
    # tolera 2 meses de atraso na publicação
    itens["ativa"] = itens["fim"] >= ultima_data - pd.DateOffset(months=2)
    itens["serie_agregada"] = itens["item"].str.startswith("All ")

    var = precos.dropna(subset=["preco"]).groupby("serie_id")["preco"].agg(
        media_12_inicio=lambda s: s.iloc[:12].mean(),
        media_12_fim=lambda s: s.iloc[-12:].mean(),
    )
    itens = itens.join(var)
    # variação entre médias de 12 meses: anula sazonalidade. Só faz sentido em série ativa.
    itens["variacao_12m_pct"] = np.where(
        itens["ativa"],
        (itens["media_12_fim"] / itens["media_12_inicio"] - 1) * 100,
        np.nan,
    ).round(1)
    return itens.reset_index()


def motivo_exclusao_modelagem(itens: pd.DataFrame, min_meses: int = MIN_MESES_HISTORICO) -> pd.Series:
    motivo = pd.Series(pd.NA, index=itens.index, dtype="string")
    motivo[~itens["ativa"]] = "descontinuada"
    motivo[motivo.isna() & (itens["meses_publicados"] < min_meses)] = "historico_curto"
    motivo[motivo.isna() & (itens["meses_faltando"] > itens["meses_na_grade"] * 0.25)] = "muitos_buracos"
    return motivo
