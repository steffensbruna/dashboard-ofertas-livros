"""Dashboard de Livros: app Streamlit.
"""

import streamlit as st

import dados

def montar_tabela(livros):
    tabela = []
    for livro in livros:
        linha = {
            "Título": livro["titulo"],
            "Categoria": livro["categoria"],
            "Nota": livro["nota"] * "⭐",
            "Preço": f"£ {livro["preco"]:.2f}",
            "Faixa": classificar_preco(livro["preco"])
        }
        tabela.append(linha)
    return tabela

def classificar_preco(preco):
    if preco < 20:
        return "Barato"
    elif preco <= 40:
        return "Preço Médio"
    else:
        return "Caro"

def contar_por_faixa_dict(livros):
    contagem = {}
    for livro in livros:
        faixa = classificar_preco(livros["preco"])
        if faixa in contagem:
            contagem[faixa] = contagem[faixa] + 1
        else:
            contagem[faixa] = 1
    
    return contagem

def contar_por_faixa(livros):
    conta_caros = 0
    conta_medios = 0
    conta_baratos = 0
    for livro in livros:
        if classificar_preco(livro["preco"]) == "Barato":
            conta_baratos += 1
        elif classificar_preco(livro["preco"]) == "Preço Médio":
            conta_medios += 1
        if classificar_preco(livro["preco"]) == "Caro":
            conta_caros += 1
    return conta_baratos, conta_medios, conta_caros

def main():
    st.set_page_config(page_title="Dashboard de Livros", page_icon="📚", layout="wide")
    st.title("📚 Dashboard de Livros")

    livros = dados.carregar_livros()

    col1, col2, col3, col4 = st.columns(4)
    qtd_livros = len(livros)
    col1.metric("Total de Livros", qtd_livros)

    preco_medio = dados.calcular_preco_medio(livros)
    col2.metric("Preço médio", f"£ {preco_medio:.2f}")

    cinco_estrelas = dados.contar_cinco_estrelas(livros)
    col3.metric("Qtd. livros 5 Estrelas", cinco_estrelas)

    mais_caro = dados.encontrar_mais_caro(livros)
    col4.metric("Livro mais caro", f"£ {mais_caro["preco"]}")
    col4.caption(mais_caro["titulo"])

    st.dataframe(montar_tabela(livros))


if __name__ == "__main__":
    main()
