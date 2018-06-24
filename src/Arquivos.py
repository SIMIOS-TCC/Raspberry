# -*- coding: utf-8 -*-

import logging
from Classes import *

CAMINHO = "arquivos"
ARQUIVO_DADOS = "dados.txt"
ARQUIVO_TEMP = "temp.txt"
ARQUIVO_BACKUP = "backup.txt"

def pegaLeitura(arquivo = ARQUIVO_TEMP):
    ''' Pega a primeira linha do arquivo especificado
        e a retorna como uma leitura, retirando ela do arquivo.'''

    leituras = abreArquivo(ARQUIVO_TEMP)#O arquivo é trazido todo para memória, espero que isso não seja um problema.
    
    if leituras:
        leituras = leituras.splitlines() #Separa cada linha do arquivo lido em leituras diversas.
        leitura = leituras.pop(0)
        logger.debug("Passando a leitura: %s ", leitura)
        limpaArquivo(ARQUIVO_TEMP)

        for linha in leituras:
            escreveArquivo(linha + '\n', ARQUIVO_TEMP)

        leitura = leitura.split(";")    #Separa cada unidade de informação da linha lida.
        ID = leitura.pop(0)             #A primeira informação é o ID de quem registrou as distâncias.
        timestamp = leitura.pop(0)      #A segunda é o timestamp de quando foi feito o registro.
        ID_distancia = leitura.pop(0)
        valor_distancia = leitura.pop(0)

        leitura = Leitura(ID, timestamp)
        leitura.adicionarDistancia(ID_distancia, valor_distancia)
        
    else:
        logger.debug("Sem leituras para pegar")
        leitura = None
    
    return leitura

def colheDados():
    ''' Colhe as leituras do arquivo de dados
        e as coloca no arquivo temporário.
        Separa as informações em leituras diferentes,
        para que cada linha do temp seja um query'''
    
    dados = abreArquivo(ARQUIVO_DADOS)
    limpaArquivo(ARQUIVO_DADOS)

    if dados:
        logger.debug("Colhendo dados: %s \n", dados)

        dados = dados.splitlines() #Separa cada linha do arquivo lido em leituras diversas.
        for dado in dados:
            dado = dado.split(";")  #Separa cada unidade de informação da linha lida.
            ID = dado.pop(0)        #A primeira informação é o ID de quem registrou as distâncias.
            timestamp = dado.pop(0) #A segunda é o timestamp de quando foi feito o registro.

            for item in range(len(dado)//2):
                linha = ID +';'+ timestamp +';'+ dado.pop(0) +';'+ dado.pop(0) + '\n'
                escreveArquivo(linha, ARQUIVO_TEMP) #Cada linha do arquivo temp contém os dados de uma query.
    else:
        logger.debug("Sem dados para colher")
    
def abreArquivo(arquivo = ARQUIVO_DADOS):
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
        open (CAMINHO + '/' + arquivo, 'w').close()
        logger.warning("Arquivo criado: %s ", arquivo)
    except:
        logger.error("Falha ao abrir o arquivo: %s ", arquivo, exc_info=True)
    finally:
        return dados

def escreveArquivo(dados, arquivo = ARQUIVO_TEMP):
    ''' Abre o arquivo especificado e coloca ao final dele "dados".
        Caso o arquivo não exista, um arquivo vazio é criado
        e dados são salvos nele. '''

    try:
        with open(CAMINHO + '/' + arquivo, 'a') as escrita:
            escrita.write(dados)
        logger.debug("Relizando escrita de : %s", dados)
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
