# -*- coding: utf-8 -*-
import MySQLdb
import logging
CAMINHO = 'arquivos/'

#Valores default
HOST = "192.168.0.8"
USER = "user"                   # Usuario do banco de dados cadastrado para um certo IP local.
PASSWORD = "user123"            # Senha deste mesmo usuario cadastrado.
DB = "simios_db"                # Banco de dados ao qual querremos conectar.
PORT = 3306                     # Porta TCP (valor default: 3306)

def criar(tabela, colunas=[]):
    ''' Funcao para criar uma tabela dentro do banco de dados conectado.
        Ela toma o nome da nova tabela em string como parametro e tambem
        as colunas e suas propriedades como uma lista desta forma:
            [[coluna1, propriedade], [coluna2, propriedade]] '''
    
    query = "CREATE TABLE `" + DB + "`.`" + tabela + "` ("      #Acessa a tabela desejada

    for coluna in colunas:                                      #Percorre a lista de colunas que se 
        query += "`" + coluna[0] + "` " + coluna[1] + " ,"      #   deseja criar, separadas por virgula.
        
    query += "PRIMARY KEY (`" + colunas[0][0] + "`)"            #Define a primary key como a primeira coluna passada por default (REVISAR).
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

    query = "INSERT INTO `" + DB + "`.`" + tabela + "` ("       #Acessa a tabela desejada

    for coluna in colunas[:-1]:                                 #Percorre a lista de colunas nas quais se
        query += coluna + ","                                   #   deseja inserir, separadas por virgula.
    query += colunas[-1] + ")"                                  #   Exceto a ultima, que acaba com ")".
        
    query += "VALUES "
    for linha in valores[:-1]:                                  #Percorre cada linha nova que se deseja inserir
        query += "("
        for valor in linha[:-1]:                                #Percorre os valores que se deseja inserir em
            query += '"' + valor + '"' + ","                    #   cada coluna, separados por virgula cada um.
        query += '"' + linha[-1] + '"' + "),"                   #   Exceto o ultimo, que acaba com "),".
    query += "("
    for valor in valores[-1][:-1]:                              #Encerra com os valores da ultima linha a serem
        query += '"' + valor + '"' + ","                        #   inseridos, que precisam acabar com ");".
    query += '"' + valores[-1][-1] + '"' + ");"
    
    executar(query)

def ler(tabela, colunas) :
    ''' Funcao para ler valores de uma tabela dentro do banco de dados conectado.
        Ela toma o nome da nova tabela em string como parametro e tambem
        as colunas e as colunas que devem ser lidas desta forma:
            [coluna1, caluna2] '''

    query = "SELECT "

    for coluna in colunas[:-1]:                                 #Seleciona as colunas da lista
        query += "`" + coluna + "`, "
    query += "`" + colunas[-1] + "` "

    query += "FROM `" + DB + "`.`" + tabela + "`;"              #Acessa a tabela desejada

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
    
    conexao = conectar()                                        #Realiza a conexao ao banco de dados. Retona None se falhou.
    
    if conexao is not None:                                     #Caso a conexao tenha sido um sucesso...
        cursor = conexao.cursor()                               #Inicializa o cursor do banco

        logger.debug("Executando a query: %s", query)           #Para fins de debug
        
        try:
            cursor.execute(query)                               #Tenta executar a query passada
            conexao.commit()                                    #Se ha sucesso, confirma as mudancas
            
            for linha in cursor.fetchall():                     #Caso haja informacao que o cursor foi buscar
                print (linha)                                   #   inprime ela na tela.
                
            logger.debug("Tudo OK")       #Para fins de debug
            
        except MySQLdb.Error, erro:                             #Caso haja algum problema com a execucao
            logger.error("Erro na execução da Query: %s ", query, exc_info=True)
            conexao.rollback()                                  #   desfazemos-la e verificamos o erro.
            
        finally:
            cursor.close()                                      # Importante sempre fechar a conexao e o cursor
            conexao.close()                                     #   ao finalizar uma transacao.
    else:
        pass

def conectar(host=HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT):
    ''' Funcao para se conectar ao banco de dados.
        Gerencia os erros da conexao.
        Retorna None se falhou. '''
    
    try:
        conexao = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port)
        return conexao                                          #A conexao so e realizada quando for necessario.
    
    except MySQLdb.Error, erro:
        logger.error("Erro na conexão com o Banco de Dados", exc_info=True)
        return None

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
