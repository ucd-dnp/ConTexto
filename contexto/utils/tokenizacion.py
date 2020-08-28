from collections import Iterable
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize.toktok import ToktokTokenizer

class TokenizadorNLTK():
    def __init__(self, tokenizador=None, destokenizador=None):
        self.establecer_tokenizador(tokenizador)
        self.establecer_destokenizador(tokenizador)
        
    def establecer_tokenizador(self, tokenizador):
        if tokenizador is not None:
            self.tokenizador = tokenizador
        else:
            self.tokenizador = ToktokTokenizer()

    def establecer_destokenizador(self, destokenizador):
        if destokenizador is not None:
            self.destokenizador = destokenizador
        else:
            self.destokenizador = TreebankWordDetokenizer()

    def tokenizar(self, texto):
        # Si es un string se aplica el procedimiento directamente
        if isinstance(texto, str):
            # Se separa el punto para que se coja como un token por separado
            texto = texto.replace(".", " .")
            return self.tokenizador.tokenize(texto)
        # Si es una lista o colección de strings, se aplica a cada uno
        elif isinstance(texto, Iterable):
            texto = [i.replace(".", " .") for i in texto]
            return self.tokenizador.tokenize_sents(texto)
        else:
            print('Tipo de entrada no válido. Debe ingresar un string o una lista de strings.')
            return None

    def post_destokenizacion(self, texto):
        texto = texto.replace('¿ ', '¿')
        texto = texto.replace('¡ ', '¡')
        texto = texto.replace("' ", "'")
        return texto
    
    def destokenizar(self, lista_tokens):
        # Si es una sola lista de tokens se aplica el procedimiento directamente
        if isinstance(lista_tokens[0], str):
            texto = self.destokenizador.detokenize(lista_tokens)
            return self.post_destokenizacion(texto)
        # Si es una lista de listas de tokens, se aplica a cada elemento
        elif isinstance(lista_tokens[0], Iterable):
            salida = [self.post_destokenizacion(self.destokenizador.detokenize(i)) for i in lista_tokens]
            return salida
        else:
            print('Tipo de entrada no válido. Debe ingresar una lista de tokens o una lista de listas de tokens.')
            return None

def tokenizar(texto, tokenizador=None):
    if tokenizador is None:
        tokenizador = TokenizadorNLTK()
    return tokenizador.tokenizar(texto)

def destokenizar(tokens, tokenizador=None):
    if tokenizador is None:
        tokenizador = TokenizadorNLTK()
    return tokenizador.destokenizar(tokens)