class Leitura:
    
    contagem = 0
    
    def __init__(self, ID, timestamp):
        Leitura.contagem += 1
        
        self.ID = ID
        self.timestamp = timestamp

        self.distancias = []

    def adicionarDistancia(self, ID, valor):
        distancia = Distancia(ID, valor)

        self.distancias.append(distancia)

class Distancia:

    contagem = 0

    def __init__(self, ID, valor):
        Distancia.contagem += 1

        self.ID = ID
        self.valor = valor
        
