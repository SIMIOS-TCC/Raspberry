class Leitura:

    contagem = 0
    leiturasNaoRealizadas = []

    def __init__(self, timestamp, ap_id, simio_id, distance):
        Leitura.contagem += 1

        self.timestamp = timestamp
        self.ap_id = ap_id
        self.simio_id = simio_id
        self.distance = distance

        Leitura.logger.debug("Leitura criada: %s" % self)
        Leitura.leiturasNaoRealizadas.append(self)

    def __str__(self):
        return "timestamp: " + str(self.timestamp) + ";" + "ap_id: " + str(self.ap_id) + ";" + "simio_id: " + str(self.simio_id) + ";" + "distance: " + str(self.distance) + ";"


class Distancia:

    contagem = 0

    def __init__(self, ID, valor):
        Distancia.contagem += 1

        self.ID = ID
        self.valor = valor


class PortTest:
    """ Classe para testar a porta serial sem Conexao Serial"""

    posicao = -1
    mensagem = "13;12;12.45;12345678>34;12;12.45;12345678;34;67.90;90123456>"

    resultados = []

    def read(self):
        PortTest.posicao += 1
        if len(PortTest.mensagem) <= PortTest.posicao:
            return ''
        else:
            return PortTest.mensagem[PortTest.posicao]

    def write(self, mensagem):
        PortTest.resultados.append(mensagem)
