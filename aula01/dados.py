"""Leitura dos arquivos CSV do projeto.
"""

from pathlib import Path
import csv

# Pasta onde este arquivo .py está. Assim o programa encontra o CSV
# mesmo quando é executado a partir de outra pasta (como no Streamlit Cloud).
PASTA = Path(__file__).parent
CAMINHO_LIVROS = PASTA / "livros.csv"

def ler_livrosv3():
    livros =[]
    try:
        with open(CAMINHO_LIVROS, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                livros.append(linha)
    except FileNotFoundError:
        print("O arquivo livros.csv não foi encontrada")
    except Exception as error:
        print("Algum erro aconteceu na leitura do arquivo", error)
    finally:
        if arquivo is not None:
            arquivo.close()
    return livros

def calcular_preco_medio(livros):
    soma: float = 0
    for livro in livros:
        preco_original: str = livro["preco"]
        preco_original_limpo: str = preco_original.replace("£","")
        preco_num: float = float(preco_original_limpo)
        soma += preco_num
    
    preco_medio: float = soma / len(livros)
    return preco_medio

def contar_cinco_estrelas(livros):
    contador: int = 0
    for livro in livros:
        nota_limpa: str = livro["nota"].lower().strip()
        if nota_limpa == "five":
            contador += 1
    return contador

def livro_mais_caro(livros):
    titulo: str = ""
    preco_mais_caro: float = 0.0
    
    for livro in livros:
        preco_original: str = livro["preco"]
        preco_original_limpo: float = float(preco_original.replace("£",""))
        
        if preco_original_limpo > preco_mais_caro:
            preco_mais_caro = preco_original_limpo
            titulo = livro["titulo"]

    return titulo, preco_mais_caro





def ler_livrosv2(caminho): #uma forma MUITO mais elegante de fazer a leitura do arquivo
    with open(caminho, "r", encoding="utf-8") as arquivo:
        print(arquivo.readline())

def ler_livrosv1(caminho):
    arquivo = None
    try:
        arquivo = open(caminho, "r", encoding="utf-8")
        print(arquivo.read())
    except FileNotFoundError:
        print("O arquivo livros.csv não foi encontrada")
    except Exception as error:
        print("Algum erro aconteceu na leitura do arquivo", error)
    finally:
        if arquivo is not None:
            arquivo.close()



if __name__ == "__main__":
    livros = ler_livrosv3()
    print(f"A quantidade de livros da coleção é de {len(livros)} livros")
    preco_medio: float = calcular_preco_medio(livros)