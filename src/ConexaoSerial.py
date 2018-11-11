# -*- coding: utf-8 -*-

import serial

SEPARADORES = ["."]
SERIAL_DIRECTORY = "/dev/serial/by-id/usb-Texas_Instruments_XDS110__02.03.00.14__Embed_with_CMSIS-DAP_L5145-if03"
BAUDRATE = 115200
TIMEOUT = 3.0


def abrePort():
    try:
        port = True
        port = serial.Serial(
            port=SERIAL_DIRECTORY, baudrate=BAUDRATE, timeout=TIMEOUT)
        return port
    except:
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
