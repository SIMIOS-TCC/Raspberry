# Projeto de TCC - SIMIOS - Módulo Controlador

Contém os arquivos para a operação do Raspberry Pi. Tem como objetvo principal fazer a intermediação da comunicação entre as placas Sensor Tagdos módulos de target, pontos de acesso e central, e o banco de dados.

## Arquivos principais

* Main.py
* Arquivos.py
* Classes.py
* ConexaoSerial.py
* DB connect.py
* QueriesMYSQL.py
* conexaoSensortag.py

## Descrição de cada arquivo

### Main.py

Esta é a aplicação principal. 

Ela é responsável por fazer toda a leitura dos dados enviados via UART pelas placas sensortag, e por isso tem toda a configuração de parâmetros lidos, abertura de porta e leitura. Assim que é feita a leitura, a mensagem é processada para que suas informações sejam armazenadas no banco de dados de maneira adequada: há verificação se há campos faltando, tipo de dado (int ou float, por exemplo), correção de timestamp, dentre outros. Feito este processamento, é feita a escrita no banco. 

Suas funções principais são:

* loopConexao(): basicamente fica esperando uma porta serial ser conectada. Quando uma porta é detectada, ela é retornada pela função;
* loopleitura(portSerial): dada a porta serial obtida por loopConexao() (portSerial), esta função é responsável por ler as mensagens passadas através desta porta. Ela retorna em "mensagemSerial" a leitura realizada e a armazena em um logger. Ela continua fazendo isso até que não haja mais leituras para serem realizadas (tempo relacionado à temporização de envio dos módulos targets presentes nos macacos, que não ficam enviando dados o tempo inteiro para economizar bateria);
* instanciaLeitura(mensagemSerial, portSerial): dada uma mensagem lida e a porta, esta função faz a separação da mensagem de acordo com o caractere separador definido. Cada campo da mensagem se refere a um parâmetro, como id do macaco, timestamp, horário e data, RSSI, entre outros. 
* iniciaLogger(): inicia a logger a ser utilizado pela aplicação.

Há ainda funções para depuração da mensagem e verificação de seu formato, como isCamposMalFormatados(mensagem), isInt(string), isFloat(string), timeStampCorrigido(deltaTimeStamp), dentre outras.


### Arquivos.py

### Classes.py

### ConexaoSerial.py

### DB connect.py

### QueriesMYSQL.py

### conexaoSensortag.py

http://software-dl.ti.com/ccs/esd/CCSv8/CCS_8_1_0/exports/CCS8.1.0.00011_web_linux-x64.tar.gz

http://www.ti.com/tool/download/SIMPLELINK-CC13X0-SDK
