# -*- coding: utf-8 -*-

import Arquivos
import QueriesMYSQL
import ConexaoSerial
from Classes import *

import time
import logging
import datetime

CAMINHO_ARQUIVOS = 'arquivos/'
SEPARADOR_VALORES_LIDOS = ";"

caracteresPorCampo = {"ApId": 2, "ApTimestamp": 8,
                      "SimioId": 2, "Distancia": 5, "Timestamp": 8}

fazerConversaoTimestampDate = False


def Main():
    portSerial = False

    while portSerial == False:
        portSerial = ConexaoSerial.abrePort()

    # Quando uma conexão for estabelecida:
    loopLeitura(portSerial)


def loopLeitura(portSerial):
    """ Executa o loop de coleta de leitura e seu subsequente processamento."""

    while True:
        # Pega a mensagem recebida do port aberto:
        mensagem = ConexaoSerial.lerLinhaSeparada(portSerial)

        if mensagem is not None:
            # Instancia uma nova leitura a partir da mensagem:
            leitura = instanciaLeitura(mensagem, portSerial)

        elif Leitura.leiturasNaoRealizadas:
            # Se não há mais mensagens sendo recebidas, passa a processar as leituras já guardadas:
            logger.debug("Pegando leituras não realizadas.")
            leitura = Leitura.leiturasNaoRealizadas.pop(0)
            processaLeitura(leitura)

        else:
            logger.debug("Nenhuma mensagem recebida...")
            time.sleep(1)
            logger.debug("Tentando novamente...")
            input()


def instanciaLeitura(mensagem, portSerial):
    global fazerConversaoTimestampDate
    logger.debug("Processando a mensagem: %s" % str(mensagem))

    # Separa cada unidade de informação da linha lida:
    mensagem = mensagem.split(SEPARADOR_VALORES_LIDOS)

    if "\x00" in mensagem:
        mensagem.remove("\x00")

    if (checaMensagem(mensagem)):
        ConexaoSerial.enviaACK(portSerial, True)

        ap_id = mensagem.pop(0)
        ap_timestamp = mensagem.pop(0)
        for _ in range(len(mensagem)//3):
            simio_id = mensagem.pop(0)
            distance = mensagem.pop(0)
            timestamp_leitura = mensagem.pop(0)
            timestamp = timestampCorrigido(ap_timestamp, timestamp_leitura)

            if fazerConversaoTimestampDate:
                timestamp = datetime.datetime.fromtimestamp(timestamp)

            leitura = Leitura(timestamp, ap_id, simio_id, distance)

    else:
        ConexaoSerial.enviaACK(portSerial, False)

        logger.warning("Leitura mal formatada.")
        leitura = None

    return leitura


def checaMensagem(mensagem):
    """ Formato canônico da mensagem: [idAP,ApTimestamp,idSimio1,dist1,timestamp1,idSimios2,dist2,timestamp2,...] """

    if isMensagemPequena(mensagem):
        return False

    elif isCamposFaltando(mensagem):
        return False

    elif isCamposMalFormatados(mensagem):
        return False

    else:
        logger.debug("Mensagem bem formatada: %s" % str(mensagem))
        return True


def isMensagemPequena(mensagem):
    if len(mensagem) < 5:
        logger.warning("Mensagem muito curta: %s" % str(mensagem))
        return True
    else:
        return False


def isCamposFaltando(mensagem):
    if (len(mensagem)-2) % 3 != 0:
        logger.warning("Faltam campos na mensagem: %s" % str(mensagem))
        return True
    else:
        return False


def isCamposMalFormatados(mensagem):

    campoApId = mensagem[0]
    if len(campoApId) != caracteresPorCampo["ApId"]:
        logger.warning("Campo 'ApId' mal formatado na mensagem: %s" %
                       str(campoApId))
        return True

    campoApTimestamp = mensagem[1]
    if len(campoApTimestamp) != caracteresPorCampo["ApTimestamp"]:
        logger.warning("Campo 'campoApTimestamp' mal formatado na mensagem: %s" %
                       str(campoApTimestamp))
        return True

    for numCampo in range(len(mensagem[2:])//3):

        campoSimioId = mensagem[2:][numCampo*3 + 0]
        if len(campoSimioId) != caracteresPorCampo["SimioId"] or not isInt(campoSimioId):
            logger.warning("Campo 'SimioId' mal formatado na mensagem: %s" %
                           str(campoSimioId))
            return True

        campoDistancia = mensagem[2:][numCampo*3 + 1]
        if len(campoDistancia) != caracteresPorCampo["Distancia"] or not isFloat(campoDistancia):
            logger.warning("Campo 'Distancia' mal formatado na mensagem: %s" %
                           str(campoDistancia))
            return True

        campoTimestamp = mensagem[2:][numCampo*3 + 2]
        if len(campoTimestamp) != caracteresPorCampo["Timestamp"] or not isInt(campoTimestamp):
            logger.warning(
                "Campo 'Timestamp' mal formatado na mensagem: %s" % str(campoTimestamp))
            return True

    return False


def isInt(string):
    '''Checa se um string representa um inteiro
    antes de passá-lo com em uma query'''

    try:
        inteiro = int(string)
    except:
        return False
    return True


def isFloat(string):
    '''Checa se um string representa um float
    antes de passá-lo com em uma query'''

    try:
        decimal = float(string)
    except:
        return False
    return True


def timestampCorrigido(ap_timestamp, timestamp_leitura):

    timestampRaspberry = time.time()

    timestamp_Corrigido = timestampRaspberry - \
        (ap_timestamp - timestamp_leitura)

    return timestamp_Corrigido


def processaLeitura(leitura):
    if leitura:

        if QueriesMYSQL.inserirDistancia(leitura.ap_id, leitura.simio_id, leitura.distance, leitura.timestamp):
            logger.debug("Passando leitura para BD %s" % str(leitura))

        else:
            Arquivos.escreveArquivo(
                str(leitura) + '\n', Arquivos.ARQUIVO_TEMP)
            Leitura.leiturasNaoRealizadas.append(leitura)

    else:
        logger.warning(
            "Campos com valores inválidos ou leitura inválida: %s" % str(leitura))


def iniciaLogger():
    ''' Inicia as opções para o logger.
        Reunidas aqui para organização.
        Retorna o logger para ser usado pelo módulo. '''

    # Pega no nome do módulo para o logger.
    logger = logging.getLogger(__name__)
    # Define o nível mínimo de filtro dos logs (deixar sempre em DEBUG).
    logger.setLevel(logging.DEBUG)

    # Cria um logger para a tela
    handler = logging.StreamHandler()
    # Mudar para INFO, WARNING ou ERROR em produção.
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s : %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Cria um logger para arquivo
    handler = logging.FileHandler(CAMINHO_ARQUIVOS + '/' + 'registro.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = iniciaLogger()
Leitura.logger = logger
ConexaoSerial.logger = logger

Main()
