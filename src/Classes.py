class Leitura:

    contagem = 0

    def __init__(self, timestamp, ap_id, simio_id, distance):
        Leitura.contagem += 1

        self.timestamp = timestamp
        self.ap_id = ap_id
        self.simio_id = simio_id
        self.distance = distance

    def __str__(self):
        return self.timestamp + ";" + self.ap_id + ";" + self.simio_id + ";" + self.distance + ";"


class Distancia:

    contagem = 0

    def __init__(self, ID, valor):
        Distancia.contagem += 1

        self.ID = ID
        self.valor = valor
