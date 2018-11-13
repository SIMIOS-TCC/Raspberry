# -*- coding: utf-8 -*-

import logging
import serial

SEPARADORES = ["."]
SERIAL_DIRECTORY = "/dev/serial/by-id/usb-Texas_Instruments_XDS110__02.03.00.14__Embed_with_CMSIS-DAP_L5145-if00"
BAUDRATE = 115200
TIMEOUT = 3.0

ACK_SUCESSO = "y"
ACK_FALHA = "n"


def abrePort():
    try:
        port = True
        port = serial.Serial(
            port=SERIAL_DIRECTORY, baudrate=BAUDRATE, timeout=TIMEOUT)
        return port
    except(exception):
        logger.error("Erro na conexao serial: %s" %str(exception))
        return False


def lerLinhaSeparada(port):
    """ Retorna um valor recebido seguido de um separador da lista de separadores.
        O valor retornado NÃO contém o separador em questão. """
    
    valorLido = ""
    while True:
        caracterRecebido = port.read()
        if caracterRecebido in SEPARADORES:
            return valorLido
        else:
            valorLido += caracterRecebido
            logger.debug("Mensagem recebida: %s" %str(valorLido))

def enviaACK(port, resultado):
    """ Envia uma mensagem pelo por serial.
        Se o resultado for True, envia um sucesso,
        se for false, envia uma falha."""

    if (resultado):
        logger.debug("Enviando ACK_Sucesso")
        port.write(ACK_SUCESSO)
    else:
        logger.debug("Enviando ACK_Falha")
        port.write(ACK_FALHA)
        
            
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

    return logger


logger = iniciaLogger()
