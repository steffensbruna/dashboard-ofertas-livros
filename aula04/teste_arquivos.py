with open("favoritos.csv", "a", encoding="utf-8", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["titulo", "preco"])
    escritor.writeheader() # titulo,preco
    escritor.writerow({"titulo": "Dune", "preco": 20.0}) # Dune,20.0