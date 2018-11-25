# -*- coding: utf-8 -*-

import MySQLdb
import ConfigParser
import logging

CAMINHO = 'arquivos/'
ARQUIVO_LOGGER = 'registro.log'
ARQUIVO_CONFIG = 'config.ini'

SECAO_CONFIG = 'ConfiguracaoConexao'

# Valores default
HOST = "192.168.0.14"
# Usuario do banco de dados cadastrado para um certo IP local.
USER = "user"
PASSWORD = "user123"            # Senha deste mesmo usuario cadastrado.
DB = "simios_db"                # Banco de dados ao qual querremos conectar.
PORT = 3306                     # Porta TCP (valor default: 3306)

SIMIO_DISTANCE = "simio_distance"
AP_ID = "ap_id"
SIMIO_ID = "simio_id"
DISTANCE = "distance"
TIMESTAMP = "timestamp"


def criar(tabela, colunas=[]):
    ''' Funcao para criar uma tabela dentro do banco de dados conectado.
        Ela toma o nome da nova tabela em string como parametro e tambem
        as colunas e suas propriedades como uma lista desta forma:
            [[coluna1, propriedade], [coluna2, propriedade]] '''

    query = "CREATE TABLE `" + DB + "`.`" + \
        tabela + "` ("  # Acessa a tabela desejada

    for coluna in colunas:  # Percorre a lista de colunas que se
        # deseja criar, separadas por virgula.
        query += "`" + coluna[0] + "` " + coluna[1] + " ,"

    # Define a primary key como a primeira coluna passada por default (REVISAR).
    query += "PRIMARY KEY (`" + colunas[0][0] + "`)"
    query += ");"

    executar(query)


def inserir(tabela, colunas=[], valores=[]):
    ''' Funcao para inserir linhas em uma tabela dentro do banco de dados conectado.
        Ela toma o nome da tabela em string como parametro e tambem
        as colunas nas quais deve se inserir os valores desta forma:
            [coluna1, caluna2]
        e os valores para inserir nestas colunas desta forma:
            [[valor1Coluna1, valor1Coluna2], [valor2Coluna1, valor2Coluna2]]
        ATENCAO: Nao e verificado nada. tomas cuidado com strings! (revisar)'''

    query = "INSERT INTO `" + DB + "`.`" + \
        tabela + "` ("  # Acessa a tabela desejada

    for coluna in colunas[:-1]:  # Percorre a lista de colunas nas quais se
        query += coluna + ","  # deseja inserir, separadas por virgula.
    query += colunas[-1] + ")"  # Exceto a ultima, que acaba com ")".

    query += "VALUES "
    for linha in valores[:-1]:  # Percorre cada linha nova que se deseja inserir
        query += "("
        for valor in linha[:-1]:  # Percorre os valores que se deseja inserir em
            # cada coluna, separados por virgula cada um.
            query += '"' + valor + '"' + ","
        # Exceto o ultimo, que acaba com "),".
        query += '"' + linha[-1] + '"' + "),"
    query += "("
    for valor in valores[-1][:-1]:  # Encerra com os valores da ultima linha a serem
        # inseridos, que precisam acabar com ");".
        query += '"' + valor + '"' + ","
    query += '"' + valores[-1][-1] + '"' + ");"

    return(executar(query))


def inserirDistancia(ap_id, simio_id, distance, dateTime):
    ''' Funcao para inserir uma linha contendo a distancia entre um ponto de acesso e um simio.
        Deve ser dado o id do simio, do ponto de acesso (ap) e a distancia entre ambos.'''

    query = "INSERT INTO `" + DB + "`.`" + SIMIO_DISTANCE + "` ("

    query += AP_ID + ","
    query += SIMIO_ID + ","
    query += DISTANCE + ","
    query += TIMESTAMP + ")"

    query += "VALUES "
    query += "("
    query += '"' + ap_id + '"' + ","
    query += '"' + simio_id + '"' + ","
    query += '"' + distance + '"' + ","
    query += '"' + dateTime + '"' + ")"

    return(executar(query))


def ler(tabela, colunas):
    ''' Funcao para ler valores de uma tabela dentro do banco de dados conectado.
        Ela toma o nome da nova tabela em string como parametro e tambem
        as colunas e as colunas que devem ser lidas desta forma:
            [coluna1, caluna2] '''

    query = "SELECT "

    for coluna in colunas[:-1]:  # Seleciona as colunas da lista
        query += "`" + coluna + "`, "
    query += "`" + colunas[-1] + "` "

    query += "FROM `" + DB + "`.`" + tabela + "`;"  # Acessa a tabela desejada

    executar(query)


def deletar(tabela):
    ''' Funcao para deletar uma tabela do banco de dados conectado.
        Toma o nome da tbela a se deletar em string como parametro.'''

    query = "DROP TABLE " + tabela

    executar(query)


def executar(query):
    ''' Funcao para enviar o comando de execucao para o banco de dados conectado.
        Deve-se passar a query que se deseja execuar. Todos os erros do banco de dados sao
        pegos aqui. Os erros de conexao sao tratados na funcao conexao. '''

    # Realiza a conexao ao banco de dados. Retona None se falhou.
    conexao = conectar()

    status = False

    if conexao is not None:  # Caso a conexao tenha sido um sucesso...
        cursor = conexao.cursor()  # Inicializa o cursor do banco

        logger.debug("Executando a query: %s", query)  # Para fins de debug

        try:
            cursor.execute(query)  # Tenta executar a query passada
            conexao.commit()  # Se ha sucesso, confirma as mudancas

            for linha in cursor.fetchall():  # Caso haja informacao que o cursor foi buscar
                print(linha)  # inprime ela na tela.

            logger.debug("Tudo OK")  # Para fins de debug.

            status = True

        except MySQLdb.Error, erro:  # Caso haja algum problema com a execucao
            logger.error("Erro na execução da Query: %s ", query, exc_info=True)
            conexao.rollback()  # desfazemos-la e verificamos o erro.

            status = False

        finally:
            # Importante sempre fechar a conexao e o cursor
            cursor.close()
            conexao.close()  # ao finalizar uma transacao.

    else:
        status = False

    return status


def conectar(host=HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT):
    ''' Funcao para se conectar ao banco de dados.
        Gerencia os erros da conexao.
        Retorna None se falhou. '''

    try:
        conexao = MySQLdb.connect(
            host=host, user=user, passwd=passwd, db=db, port=port)
        return conexao  # A conexao so e realizada quando for necessario.

    except MySQLdb.Error, erro:
        logger.error("Erro na conexão com o Banco de Dados", exc_info=True)
        return None


def iniciaConfig():
    Config = ''

    status = False

    try:
        Config = ConfigParser.ConfigParser()
        Config.read(CAMINHO + '/' + ARQUIVO_CONFIG)

        mapaConfig = mapearConfiguracao(Config, SECAO_CONFIG)

        if mapaConfig:
            HOST = mapaConfig['HOST']
            # Usuario do banco de dados cadastrado para um certo IP local.
            USER = mapaConfig['USER']
            # Senha deste mesmo usuario cadastrado.
            PASSWORD = mapaConfig['PASSWORD']
            # Banco de dados ao qual querremos conectar.
            DB = mapaConfig['DB']
            PORT = mapaConfig['PORT']     # Porta TCP (valor default: 3306).

        else:
            pass  # Os valores default serão usados.

        status = True

    except:
        logger.error(
            "Não foi possível encontrar o arquivo de configuração.", exc_info=True)
        status = False

    finally:
        return (status)


def mapearConfiguracao(Config, secao):
    dict1 = {}
    opcoes = Config.options(secao)
    for opcao in opcoes:
        try:
            dict1[opcao] = Config.get(section, opcao)
            if dict1[opcao] == -1:
                logger.debug("Opção pulada: %s", opcao)
        except:
            logger.error(
                "Não foi possível atribuir as opçoes de configuração.", exc_info=True)
            dict1[option] = None
    return dict1


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
    handler = logging.FileHandler(CAMINHO + '/' + ARQUIVO_LOGGER)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


config = iniciaConfig()
logger = iniciaLogger()
