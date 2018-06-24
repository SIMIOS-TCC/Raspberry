# -*- coding: utf-8 -*-

import Arquivos
import QueriesMYSQL
import logging
CAMINHO = 'arquivos/'

DB_INSERIR = "simio_distance"
COLUNAS_INSERIR = ["simio_id1", "simio_id2", "distance"]

def Main():
    Arquivos.colheDados() #Para pegar todas as novas leituras.

    leitura = Arquivos.pegaLeitura()

    while leitura:
        distancia = leitura.distancia

        if checaCampos(leitura):

            linha = leitura.ID +';'+ leitura.timestamp +';'+ distancia.ID +';'+ distancia.valor + '\n'

            if QueriesMYSQL.inserir(DB_INSERIR, COLUNAS_INSERIR, [[leitura.ID, distancia.ID, distancia.valor]]):
                Arquivos.escreveArquivo(linha, Arquivos.ARQUIVO_BACKUP) #Salva a linha atual para a posteridade
        
            else:
                Arquivos.escreveArquivo(linha, Arquivos.ARQUIVO_TEMP)

        else:
            logger.Warning("Campos com valores inválidos: %s, %s, %s .", (leitura.ID, distancia.ID, distancia.valor))

        leitura = Arquivos.pegaLeitura()

def checaInt(string):
    '''Checa se um string representa um inteiro
        antes de passá-lo com em uma query'''
    
    try:    inteiro = int(string)
    except: return False
    return  True

def checaFloat(string):
    '''Checa se um string representa um float
        antes de passá-lo com em uma query'''
    
    try:    decimal = float(string)
    except: return False
    return  True

def checaCampos(leitura):

    if checaInt(leitura.ID) and checaInt(leitura.distancia.ID) and checaFloat(leitura.distancia.valor):
        return True
    
    else:
        return False

def iniciaLogger():
    ''' Inicia as opções para o logger.
        Reunidas aqui para organização.
        Retorna o logger para ser usado pelo módulo. '''

    logger = logging.getLogger(__name__)# Pega no nome do módulo para o logger.   
    logger.setLevel(logging.DEBUG)      # Define o nível mínimo de filtro dos logs (deixar sempre em DEBUG).

    # Cria um logger para a tela
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG) #Mudar para INFO, WARNING ou ERROR em produção.
    formatter = logging.Formatter( '%(levelname)-8s : %(message)s' )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)

    # Cria um logger para arquivo
    handler = logging.FileHandler(CAMINHO + '/' + 'registro.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter( '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

logger = iniciaLogger()

Main()
