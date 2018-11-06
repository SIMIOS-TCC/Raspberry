import serial

port = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__02.03.00.14__Embed_with_CMSIS-DAP_L5145-if03", baudrate=115200, timeout=3.0)

while True:
    port.write("s")
    rcv = port.read(10)
    print "Valor lido: ", rcv
