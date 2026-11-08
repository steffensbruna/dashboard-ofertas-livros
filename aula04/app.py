"""Dashboard de Livros: app Streamlit.

Para rodar (com o ambiente virtual ativado):  streamlit run aula04/app.py
"""

import streamlit as st

import dados


def calcular_preco_medio(livros):
    """Soma os preços de todos os livros e divide pelo total."""
    soma = 0
    for livro in livros:
        soma = soma + livro["preco"]
    return soma / len(livros)


def contar_cinco_estrelas(livros):
    """Conta quantos livros têm a nota máxima."""
    quantidade = 0
    for livro in livros:
        if livro["nota"] == 5:
            quantidade = quantidade + 1
    return quantidade


def classificar_preco(preco):
    """Classifica um preço em libras em uma faixa de texto."""
    if preco < 20:
        return "Barato"
    elif preco <= 40:
        return "Médio"
    else:
        return "Caro"


def contar_por_faixa(livros):
    """Conta quantos livros existem em cada faixa de preço: {"Caro": 403, ...}"""
    contagem = {}
    for livro in livros:
        faixa = classificar_preco(livro["preco"])
        if faixa in contagem:
            contagem[faixa] = contagem[faixa] + 1
        else:
            contagem[faixa] = 1
    return contagem


def montar_tabela(livros):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis."""
    tabela = []
    for livro in livros:
        linha = {
            "Título": livro["titulo"],
            "Categoria": livro["categoria"],
            "Nota": "⭐" * livro["nota"],
            "Preço": f"£ {livro['preco']:.2f}",
            "Faixa": classificar_preco(livro["preco"]),
        }
        tabela.append(linha)
    return tabela

def montar_tabela_favoritos(favoritos):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis."""
    tabela = []
    for titulo, favorito in favoritos.items():
        linha = {
            "Título": titulo,
            "Preço": f"£ {favorito['preco']:.2f}",
            "Status": favorito["status"],
            "Comentário": favorito["comentario"],
        }
        tabela.append(linha)
    return tabela

def somar_favoritos(favoritos):
    """Soma o preço de todos os favoritos."""
    total = 0
    for favorito in favoritos.values():
        total = total + favorito["preco"]
    return total


def buscar_por_titulo(livros, busca):
    """Devolve só os livros cujo título contém o texto buscado."""
    resultado = []
    for livro in livros:
        # Compara tudo em minúsculas: "harry" encontra "Harry Potter"
        if busca.lower() in livro["titulo"].lower():
            resultado.append(livro)
    return resultado


def listar_categorias(livros):
    """Devolve as categorias dos livros, sem repetição e em ordem alfabética."""
    categorias = []
    for livro in livros:
        if livro["categoria"] not in categorias:
            categorias.append(livro["categoria"])
    categorias.sort()
    return categorias


def filtrar_por_categoria(livros, categoria):
    """Devolve só os livros da categoria escolhida. Com "Todas", devolve todos."""
    if categoria == "Todas":
        return livros
    resultado = []
    for livro in livros:
        if livro["categoria"] == categoria:
            resultado.append(livro)
    return resultado

#ABA CATÁLOGO
def mostrar_catalogo(livros):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de livros", len(livros))
    col2.metric("Preço médio", f"£{round(calcular_preco_medio(livros), 2)}")
    col3.metric("Livros com 5 estrelas", contar_cinco_estrelas(livros))
    
    mais_caro = dados.encontrar_mais_caro(livros)
    col4.metric("Livro mais caro", f"£{mais_caro["preco"]}")
    col4.caption(mais_caro["titulo"])
    
    col_busca, col_categoria = st.columns(2)
    busca = col_busca.text_input("🔎 Buscar pelo título")
    categoria = col_categoria.selectbox("📂 Categoria", ["Todas"] + listar_categorias(livros))

    # Cada filtro recebe o resultado do anterior
    encontrados = filtrar_por_categoria(livros, categoria)
    encontrados = buscar_por_titulo(encontrados, busca)

    def encontrar_livro(livros, titulo):
        """Devolve o primeiro livro com esse título."""
        for livro in livros:
            if livro["titulo"] == titulo:
                return livro

    def listar_titulos(encontrados):
        titulos = []
        for livro in encontrados:
            titulos.append(livro['titulo'])
        return titulos

    if len(encontrados) == 0:
        st.warning("Nenhum livro encontrado.")
    else:
        st.caption(f"{len(encontrados)} livros encontrados")
        st.dataframe(montar_tabela(encontrados), hide_index=True, width="stretch")
        
        titulo = st.selectbox("Escolha um livro", listar_titulos(encontrados))
        
        if st.button("⭐ Adicionar aos Favoritos"):
            favoritos = dados.carregar_favoritos()
            if titulo in favoritos:
                st.warning("Esse livro já está nos favoritos.")
            else:
                dados.salvar_favorito(encontrar_livro(encontrados, titulo))
                st.success("Livro adicionado!")

#ABA FAVORITOS
def mostrar_favoritos():
    """Mostra os favoritos salvos."""
    favoritos = dados.carregar_favoritos()
    if len(favoritos) == 0:
        st.info("Nenhum favorito ainda.")
        return
    col1, col2 = st.columns(2)
    col1.metric("Favoritos", len(favoritos))
    col2.metric("Total", f"£ {somar_favoritos(favoritos):.2f}")
    st.dataframe(montar_tabela_favoritos(favoritos), hide_index=True, width="stretch")
    
    titulo = st.selectbox("Escolha um favorito", list(favoritos.keys()))
    favorito = favoritos[titulo]

    STATUS = ["Quero ler", "Lendo", "Lido"]
    
    status = st.selectbox("Status", STATUS, index=STATUS.index(favorito["status"]))
    comentario = st.text_input("Comentário", favorito["comentario"])

    if st.button("💾 Salvar alterações"):
        favorito.update({"status": status, "comentario": comentario})
        dados.gravar_favoritos(favoritos)
        st.rerun()
    if st.button("🗑️ Remover"):
        del favoritos[titulo]
        dados.gravar_favoritos(favoritos)
        st.rerun()


def main():
    st.set_page_config(page_title="Dashboard de Livros", page_icon="📚", layout="wide")
    st.title("📚 Dashboard de Livros")

    livros = dados.carregar_livros()

    aba_catalogo, aba_favoritos = st.tabs([" Catálogo", " Favoritos"])
    
    with aba_catalogo:
        mostrar_catalogo(livros)
    with aba_favoritos:
        mostrar_favoritos()

if __name__ == "__main__":
    main()
