# -*- coding: utf-8 -*-

import Arquivos
import QueriesMYSQL
import ConexaoSerial
from Classes import *

# Checar se o banco de dados comporta o tipo enviado.
import time
import logging
import datetime

CAMINHO_ARQUIVOS = 'arquivos/'
SEPARADOR_VALORES_LIDOS = ";"

CONSTANTE_ELETROMAGNETICA = 3.4
RSSI_1M = -60

caracteresPorCampo = {"ApId": 3, "SimioId": 3,
                      "RSSI": 3, "campoDeltaTimestamp": 6}


def Main():
    portSerial = loopConexao()

    while True:
        try:
            # Quando uma conexão for estabelecida:
            loopLeitura(portSerial)
        except KeyboardInterrupt:
            break
        except:
            portSerial = loopConexao()


def loopConexao():
    portSerial = False

    while portSerial == False:
        portSerial = ConexaoSerial.abrePort()
    #ConexaoSerial.enviaACK(portSerial, True)
    return portSerial


def loopLeitura(portSerial):
    """ Executa o loop de coleta de leitura e seu subsequente processamento."""

    while True:
        # Pega a mensagem recebida do port aberto:
        mensagemSerial = ConexaoSerial.lerLinhaSeparada(portSerial)

        if mensagemSerial is not None:
            # Instancia uma nova leitura a partir da mensagemSerial:
            instanciaLeitura(mensagemSerial, portSerial)

        elif Leitura.leiturasNaoRealizadas:
            # Se não há mais mensagens sendo recebidas, passa a processar as leituras já guardadas:
            logger.debug("Pegando leituras não realizadas.")
            leitura = Leitura.leiturasNaoRealizadas.pop(0)
            processaLeitura(leitura)

        else:
            logger.debug("Nenhuma mensagem serial recebida...")
            time.sleep(1)
            logger.debug("Tentando novamente...")


def instanciaLeitura(mensagem, portSerial):
    logger.debug("Processando a mensagem: %s" % str(mensagem))

    # Separa cada unidade de informação da linha lida:
    mensagem = mensagem.split(SEPARADOR_VALORES_LIDOS)

    if "\x00" in mensagem:
        mensagem.remove("\x00")

    mensagens = [mensagem[:len(mensagem)//4], mensagem[len(mensagem)//4:2*len(mensagem)//4],
                 mensagem[2*len(mensagem)//4:3*len(mensagem)//4], mensagem[3*len(mensagem)//4:]]

    for mensagem in mensagens:
        if (checaMensagem(mensagem)):
            ap_id = mensagem.pop(0)
            for _ in range(len(mensagem)//3):
                simio_id = mensagem.pop(0)
                rssi = mensagem.pop(0)
                deltaTimestamp = mensagem.pop(0)
                # Antes de mais nada, corrige o timestamp:
                timestamp = timestampCorrigido(int(deltaTimestamp))
                # Coloca em um formato para mandar para o Banco:
                dateTime = datetime.datetime.fromtimestamp(
                    timestamp).strftime('%Y-%m-%d %H:%M:%S')

                leitura = Leitura(ap_id=ap_id, simio_id=simio_id,
                                  rssi=rssi, dateTime=dateTime)

                Arquivos.escreveArquivo(str(leitura), Arquivos.ARQUIVO_BACKUP)
                logger.info("Leitura: %s" % str(leitura))

        else:
            logger.warning("Leitura mal formatada.")
            leitura = None


def checaMensagem(mensagem):
    """ Formato canônico da mensagem: [idAP,idSimio1,dist1,deltaTimestamp1,idSimios2,dist2,deltaTimestamp2,...] """

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
    if len(mensagem) < 4:
        logger.warning("Mensagem muito curta: %s" % str(mensagem))
        return True
    else:
        return False


def isCamposFaltando(mensagem):
    if (len(mensagem)-1) % 3 != 0:
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

    for numCampo in range(len(mensagem[1:])//3):

        campoSimioId = mensagem[1:][numCampo*3 + 0]
        if len(campoSimioId) != caracteresPorCampo["SimioId"] or not isInt(campoSimioId):
            logger.warning("Campo 'SimioId' mal formatado na mensagem: %s" %
                           str(campoSimioId))
            return True

        campoDistancia = mensagem[1:][numCampo*3 + 1]
        if len(campoDistancia) != caracteresPorCampo["RSSI"] or not isInt(campoDistancia):
            logger.warning("Campo 'RSSI' mal formatado na mensagem: %s" %
                           str(campoDistancia))
            return True

        campoDeltaTimestamp = mensagem[1:][numCampo*3 + 2]
        if len(campoDeltaTimestamp) != caracteresPorCampo["campoDeltaTimestamp"] or not isInt(campoDeltaTimestamp):
            logger.warning(
                "Campo 'campoDeltaTimestamp' mal formatado na mensagem: %s" % str(campoDeltaTimestamp))
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


def timestampCorrigido(deltaTimestamp):
    # Correção para o tempo global:
    timestampRaspberry = time.time()

    timestamp_Corrigido = timestampRaspberry - deltaTimestamp

    return timestamp_Corrigido


def processaLeitura(leitura):
    if leitura:

        if QueriesMYSQL.inserirDistancia(leitura.ap_id, leitura.simio_id, leitura.distance, leitura.dateTime):
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

Leitura.CONSTANTE_ELETROMAGNETICA = CONSTANTE_ELETROMAGNETICA
Leitura.RSSI_1M = RSSI_1M

Main()
