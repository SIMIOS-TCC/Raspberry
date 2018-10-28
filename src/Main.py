# -*- coding: utf-8 -*-

import Arquivos
import QueriesMYSQL
import logging
CAMINHO = 'arquivos/'

#colunasExemplo = [["simio_id1", "INT NOT NULL AUTO_INCREMENT"], ["ID1", "INT NOT NULL"], ["distancia1", "INT NOT NULL"]]
colunasInserir = ["simio_id1", "simio_id2", "distance"]


def Main():
    Arquivos.colheDados()  # Para pegar todas as novas leituras.

    leitura = Arquivos.pegaLeitura()

    while leitura:

        if checaCampos(leitura):

            if QueriesMYSQL.inserirDistancia(leitura.ap_id, leitura.simio_id, leitura.distance, leitura.timestamp):
                pass

            else:
                Arquivos.escreveArquivo(
                    str(leitura) + '\n', Arquivs.ARQUIVOS_TEMP)

        else:
            logger.Warning("Campos com valores inválidos: ", leitura)


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
