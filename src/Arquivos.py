# -*- coding: utf-8 -*-

import logging
from Classes import *

'''
    Modelo do arquivo *.txt:
    timestamp1;ap_id1;simio_id1;distance1;
    timestamp2;ap_id2;simio_id2;distance2;
    timestamp3;ap_id3;simio_id3;distance3;
'''

CAMINHO = "arquivos"
ARQUIVO_TEMP = "temp.txt"
ARQUIVO_BACKUP = "backup.txt"

NEW_LINE = "\n"
CARRIGE_RETURN = "\r"


def pegaLeitura(arquivo=ARQUIVO_TEMP):
    ''' Pega a primeira linha do arquivo especificado
        e a retorna como uma leitura, retirando ela do arquivo.'''

    # O arquivo é trazido todo para memória, espero que isso não seja um problema.
    leituras = abreArquivo(ARQUIVO_TEMP)

    if leituras:
        # Separa cada linha do arquivo lido em leituras diversas.
        leituras = leituras.splitlines()
        leitura = leituras.pop(0)
        logger.debug("Passando a leitura: %s ", leitura)
        limpaArquivo(ARQUIVO_TEMP)

        for linha in leituras:
            escreveArquivo(linha + "/n", ARQUIVO_TEMP)

        # Separa cada unidade de informação da linha lida.
        leitura = leitura.split(";")

        timestamp = leitura.pop(0)
        ap_id = leitura.pop(0)
        simio_id = leitura.pop(0)
        distance = leitura.pop(0)

        leitura = Leitura(timestamp, ap_id, simio_id, distance)

    else:
        logger.debug("Sem leituras para pegar")
        leitura = None

    return leitura


def abreArquivo(arquivo=ARQUIVO_TEMP):
    ''' Abre o arquivo especificado e retorna seu conteúdo.
        Caso o arquivo não exista, um arquivo vazio é criado
        e uma string vazia é retornada. '''

    dados = ''
    try:
        with open(CAMINHO + '/' + arquivo, 'r') as arquivoDados:
            dados = arquivoDados.read()
        logger.info("Acesso ao arquivo: %s ", arquivo)
    except (IOError, FileNotFoundError):
        logger.warning("Arquivo não encontrado: %s ", arquivo)
        open(CAMINHO + '/' + arquivo, 'w').close()
        logger.warning("Arquivo criado: %s ", arquivo)
    except:
        logger.error("Falha ao abrir o arquivo: %s ", arquivo, exc_info=True)
    finally:
        return dados


def escreveArquivo(dados, arquivo=ARQUIVO_TEMP):
    ''' Abre o arquivo especificado e coloca ao final dele "dados".
        Caso o arquivo não exista, um arquivo vazio é criado
        e dados são salvos nele. '''

    try:
        with open(CAMINHO + '/' + arquivo, 'a') as escrita:
            escrita.write(str(dados) + NEW_LINE + CARRIGE_RETURN)
        logger.debug("Relizando escrita de : %s", str(dados))
    except:
        logger.error("Falha ao abrir o arquivo para escrita", exc_info=True)


def limpaArquivo(arquivo):
    try:
        open(CAMINHO + '/' + arquivo, 'w').close()
        logger.debug("Arquivo limpo: %s ", arquivo)
    except:
        logger.error("Falha ao limpar o arquivo: %s ", arquivo, exc_info=True)


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
