# -*- coding: utf-8 -*-
import logging
from Classes import *

CAMINHO = "arquivos"
ARQUIVO_DADOS = "dados.txt"
ARQUIVO_BACKUP = "backup.txt"

def pegaDados():
    ''' Pega os dados do arquivo de dados especificado
        e retorna uma Leitura dos dados.
        Alem disso, faz um backup e limpa o arquivo de dados.'''

    info = [] #Guardara as informações a serem passadas como dados.
    
    dados = abreArquivo(ARQUIVO_DADOS)
    logger.debug("Pegando dados: %s \n", dados)
    
    if dados:
        
        backup(dados)
        limpaArquivo(ARQUIVO_DADOS)
        
        dados = dados.splitlines() #Separa cada linha do arquivo lido em leituras diversas.
        for dado in dados:
            dado = dado.split(";")  #Separa cada unidade de informação da linha lida.
            ID = dado.pop(0)        #A primeira informação é o ID de quem registrou as distâncias.
            timestamp = dado.pop(0) #A segunda é o timestamp de quando foi feito o registro.
            
            leitura = Leitura(ID, timestamp)

            for item in range(len(dado)//2):
                leitura.adicionarDistancia(dado.pop(0), dado.pop(0))

            info.append(leitura)
            
        logger.debug("Passando os dados: %s ", info)
        return info
    
    else:
        logger.debug("Passando os dados: %s ", info)
        return info
    
def abreArquivo(arquivo):
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

def backup(dados):
    ''' Abre o arquivo de backup e coloca ao final dele "dados".
        Caso o arquivo não exista, um arquivo vazio é criado
        e dados são salvos nele. '''

    try:
        with open(CAMINHO + '/' + ARQUIVO_BACKUP, 'a') as arquivoBackup:
            arquivoBackup.write(dados)
        logger.debug("Relizando backup")
    except:
        logger.error("Falha ao abrir o arquivo de Backup", exc_info=True)

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
