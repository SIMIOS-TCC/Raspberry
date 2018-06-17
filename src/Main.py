import Arquivos
import QueriesMYSQL

def Main():
    dados = pegaDados()

    #Trata os dados antes de mandar.
    #EX: timestamp e distância...
    
    #Manda queries com os dados tratados
    for leitura in dados:
        for distancia in leitura.distancias:
            #insert(distancia, [ID, timestamp, ID_distancia, valor_distancia], [leitura.ID, leitura.timestamp, distancia.ID, distancia.valor])
            logger.debug("Emitindo insert: %s", leitura)

def checaInt(string):
    '''Checa se um string representa um inteiro
        antes de passá-lo com em uma query'''
    
    try:    inteiro = int(string)
    except: return False
    return  True

def checaFloat(string):
    '''Checa se um string representa um float
        antes de passá-lo com em uma query'''
    
    try:    decimal = float(string)
    except: return False
    return  True

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

Main()
