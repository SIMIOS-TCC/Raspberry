class Leitura:

    contagem = 0
    leiturasNaoRealizadas = []

    def __init__(self, dateTime, ap_id, simio_id, rssi):
        Leitura.contagem += 1

        self.dateTime = dateTime
        self.ap_id = ap_id
        self.simio_id = simio_id

        self.distance = str(Leitura.coverteEmDistancia(int(rssi)))

        Leitura.logger.debug("Leitura criada: %s" % self)
        Leitura.leiturasNaoRealizadas.append(self)

    def __str__(self):
        return "dateTime: " + str(self.dateTime) + ";" + "ap_id: " + str(self.ap_id) + ";" + "simio_id: " + str(self.simio_id) + ";" + "distance: " + str(self.distance) + ";"

    @staticmethod
    def coverteEmDistancia(rssi):
        #RSSI = -10*n*log10(d) + A
        return 10**((rssi - Leitura.RSSI_1M)/(-10*Leitura.CONSTANTE_ELETROMAGNETICA))


class PortTest:
    """ Classe para testar a porta serial sem Conexao Serial"""

    posicao = -1
    mensagem = "12;12;00001;00010.34;12;-2345;65536;34;00010;65536."

    resultados = []

    def read(self):
        PortTest.posicao += 1
        if len(PortTest.mensagem) <= PortTest.posicao:
            return ''
        else:
            return PortTest.mensagem[PortTest.posicao]

    def write(self, mensagem):
        PortTest.resultados.append(mensagem)
