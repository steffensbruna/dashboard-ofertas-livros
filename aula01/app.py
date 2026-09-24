"""Dashboard de Livros: app Streamlit.
"""

import streamlit as st
import dados

st.set_page_config(layout="wide")
st.title("📚 Dashboard de Livros")
st.write("Se você está vendo esta página, o seu ambiente está pronto! 🎉")

catalogo = dados.ler_livrosv3()

col1, col2, col3, col4 = st.columns(4)
qtd_livros = len(catalogo)
col1.metric(label="Quantidade de Livros", value=qtd_livros)

preco_medio = dados.calcular_preco_medio(catalogo)
col2.metric(label="Preço Médio", value=f"£ {preco_medio:.2f}")

qtd_cinco_estrelas = dados.contar_cinco_estrelas(catalogo)
col3.metric(label="Livros com 5 estrelas", value=qtd_cinco_estrelas)

nome_livro, preco = dados.livro_mais_caro(catalogo)
col4.metric("Livro Mais Caro",f"£ {preco}",nome_livro)

st.dataframe(catalogo)