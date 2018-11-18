# -*- coding: utf-8 -*-

from Classes import PortTest
import serial

SEPARADORES = ["."]

SERIAL_DIRECTORY = "/dev/serial/by-id/usb-Texas_Instruments_XDS110__02.03.00.14__Embed_with_CMSIS-DAP_L5145-if00"
BAUDRATE = 115200
TIMEOUT = 3.0

ACK_SUCESSO = "y"
ACK_FALHA = "n"


def abrePort():
    logger.info("Conectando-se com o port:")
    logger.info("\t No Endereço: %s" % str(SERIAL_DIRECTORY))
    logger.info("\t Com Baudrate: %s" % str(BAUDRATE))
    logger.info("\t E Timeout: %s" % str(TIMEOUT))

    try:
        #port = PortTest()
        port = serial.Serial(port=SERIAL_DIRECTORY,
                             baudrate=BAUDRATE, timeout=TIMEOUT)
        logger.debug("Sucesso na conexao com o port")
        return port
    except(exception):
        logger.error("Erro na conexao serial: %s" % str(exception))
        return False


def lerLinhaSeparada(port):
    """ Retorna um valor recebido seguido de um separador da lista de separadores.
        O valor retornado NÃO contém o separador em questão. """

    valorLido = ""
    while True:
        caracterRecebido = port.read()
        if caracterRecebido in SEPARADORES:
            logger.debug("Mensagem recebida: %s" % str(valorLido))
            return valorLido
        elif caracterRecebido == '' or caracterRecebido == None:
            return None
        else:
            valorLido += caracterRecebido


def enviaACK(port, resultado):
    """ Envia uma mensagem pelo por serial.
        Se o resultado for True, envia um sucesso,
        se for false, envia uma falha."""

    if (resultado == True):
        logger.debug("Enviando ACK_Sucesso")
        port.write(ACK_SUCESSO)
    else:
        logger.debug("Enviando ACK_Falha")
        port.write(ACK_FALHA)
