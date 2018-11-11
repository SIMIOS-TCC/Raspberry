# -*- coding: utf-8 -*-

import Arquivos
import QueriesMYSQL
import ConexaoSerial
from Classes import *

import logging

CAMINHO = 'arquivos/'
DB_INSERIR = "simio_distance"
COLUNAS_INSERIR = ["simio_id1", "simio_id2", "distance"]

SEPARADOR_VALORES_LIDOS = ";"

leiturasIncompletas = []


def Main():

    logger.debug("Tentando se conectar com o port serial...")
    portSerial = ConexaoSerial.abrePort()

    if (portSerial == False):
        logger.warning("Houve um erro ao abrir o port serial.")

    else:
        logger.debug("Conectado com o port serial")
        loopLeitura(portSerial)


def loopLeitura(portSerial):
    """ Executa o loop de coleta de leitura e seu subsequente processamento."""

    while True:
        mensagem = ConexaoSerial.lerLinhaSeparada(portSerial)

        if mensagem:
            logger.debug("Próxima leitura a ser processada: ", str(mensagem))
            leitura = instanciaLeitura(mensagem)
        elif leiturasIncompletas:
            leitura = leiturasIncompletas.pop(0)
        else:
            leitura = None

        processaLeitura(leitura)


def instanciaLeitura(mensagem):
    # Separa cada unidade de informação da linha lida.
    mensagem = mensagem.split(SEPARADOR_VALORES_LIDOS)

    try:
        timestamp = mensagem.pop(0)
        ap_id = mensagem.pop(0)
        simio_id = mensagem.pop(0)
        distance = mensagem.pop(0)

        leitura = Leitura(timestamp, ap_id, simio_id, distance)
    except:
        logger.warning("Leitura mal formatada.")
        leitura = None

    return leitura


def processaLeitura(leitura):
    if leitura and checaCampos(leitura):

         if QueriesMYSQL.inserirDistancia(leitura.ap_id, leitura.simio_id, leitura.distance, leitura.timestamp):
            logger.debug("Passando leitura para BD ", str(leitura))

        else:
            Arquivos.escreveArquivo(
                str(leitura) + '\n', Arquivos.ARQUIVOS_TEMP)
            leiturasIncompletas.push(leitura)

    else:
        logger.warning(
            "Campos com valores inválidos ou leitura inválida: ", str(leitura))


def checaInt(string):
    '''Checa se um string representa um inteiro
        antes de passá-lo com em uma query'''

    try:
        inteiro = int(string)
    except:
        return False
    return True


def checaFloat(string):
    '''Checa se um string representa um float
        antes de passá-lo com em uma query'''

    try:
        decimal = float(string)
    except:
        return False
    return True


def checaCampos(leitura):

    # if checaInt(leitura.ID) and checaInt(leitura.distancia.ID) and checaFloat(leitura.distancia.valor):
    return True

    # else:
    #    return False


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
    handler = logging.FileHandler(CAMINHO + '/' + 'registro.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = iniciaLogger()

Main()
