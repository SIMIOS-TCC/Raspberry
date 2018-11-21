class Leitura:

    contagem = 0
    leiturasNaoRealizadas = []

    # Valores default:
    CONSTANTE_ELETROMAGNETICA = 3.4
    RSSI_1M = -60

    def __init__(self, ap_id, simio_id, rssi, dateTime):
        Leitura.contagem += 1

        self.ap_id = ap_id
        self.simio_id = simio_id

        self.distance = str(Leitura.coverteEmDistancia(int(rssi)))
        self.rssi = rssi

        self.dateTime = dateTime

        #Leitura.logger.debug("Leitura criada: %s" % self)
        Leitura.leiturasNaoRealizadas.append(self)

    def __str__(self):
        returnString = ""
        returnString += "ap_id:" + str(self.ap_id) + "; "
        returnString += "simio_id:" + str(self.simio_id) + "; "
        returnString += "distance:" + str(self.distance) + "; "
        returnString += "dateTime:" + str(self.dateTime) + "; "
        returnString += "RSSI:" + str(self.rssi) + "."
        return returnString

    @staticmethod
    def coverteEmDistancia(rssi):
        #RSSI = -10*n*log10(d) + A
        return 10**((rssi - Leitura.RSSI_1M)/(-10*Leitura.CONSTANTE_ELETROMAGNETICA))


class PortTest:
    """ Classe para testar a porta serial sem Conexao Serial"""

    posicao = -1
    mensagem = "123;123;00001;00010.345;123;-2345;65536;345;00010;65536."

    resultados = []

    def read(self):
        PortTest.posicao += 1
        if len(PortTest.mensagem) <= PortTest.posicao:
            return ''
        else:
            return PortTest.mensagem[PortTest.posicao]

    def write(self, mensagem):
        PortTest.resultados.append(mensagem)
