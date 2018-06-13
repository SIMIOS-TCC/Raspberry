'''from QueriesMYSQL import *

# Variaveis para testar as conexoes
colunasExemplo = [["ID", "INT NOT NULL AUTO_INCREMENT"], ["nome", "VARCHAR(255) NULL"], ["sobrenome", "VARCHAR(255) NULL"]]
colunasInserir = ["nome", "sobrenome"]
valoresExemplo = [["Tharin", "Vaalanor"], ["Badon", "Patafirme"], ["Eiguer", "Caolho"]]

def main():
    criar("teste", colunasExemplo)

    inserir("teste", colunasInserir, valoresExemplo)

    ler("teste", colunasInserir)

    raw_input("Pressione ENTER para deletar")

    deletar("teste")

    #ler("simio", ["*"])'''

import Arquivos

leitura = Arquivos.pegaDados(Arquivos.DADOS)
print (leitura)
