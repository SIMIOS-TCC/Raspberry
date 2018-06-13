
DADOS = "dados.txt"

def pegaDados(arquivo):
    ''' Abre o arquivo especificado e retorna seu conteúdo,
        Caso o arquivo não exista, um arquivo vazio é criado
        e uma string vazia é retornada. '''
    
    try:
        with open('dados/' + arquivo, 'r') as arquivoDados:
            dados = arquivoDados.read()
    except (IOError, FileNotFoundError):
        with open ('dados/' + arquivo, 'w') as arquivoDados:
            dados = ''
    finally:
        return dados
    
