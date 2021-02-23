from collections import Iterable
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize.toktok import ToktokTokenizer


class TokenizadorNLTK():
    def __init__(self, tokenizador=None, destokenizador=None):
        """
        Constructor por defecto de la clase TokenizadorNLTK. Esta clase se apoya \
        en la librería NLTK para definir acciones de tokenización y detokenización \
        (operación inversa en la que se pasa de tokens a texto) de textos.

        :param tokenizador: (objeto de tokenización de NLTK) Valor por defecto: None. Objeto \
            encargado de la tokenización de textos. Si el valor es 'None', se cargará por \
            defecto una instancia de la clase *ToktokTokenizer*, de la librería NLTK.
        :param detokenizador: (objeto de detokenización de NLTK) Valor por defecto: None. Objeto \
            encargado de la detokenización de textos. Si el valor es 'None', se cargará por \
            defecto una instancia de la clase *TreebankWordDetokenizer*, de la librería NLTK.
        """
        self.establecer_tokenizador(tokenizador)
        self.establecer_destokenizador(tokenizador)

    def establecer_tokenizador(self, tokenizador):
        """
        Permite definir o cambiar el tokenizador a utilizar.

        :param tokenizador: (objeto de tokenización de NLTK). Objeto \
            encargado de la tokenización de textos. Si el valor es 'None', se cargará por \
            defecto una instancia de la clase *ToktokTokenizer*, de la librería NLTK.
        """
        if tokenizador is not None:
            self.tokenizador = tokenizador
        else:
            self.tokenizador = ToktokTokenizer()

    def establecer_destokenizador(self, destokenizador):
        """
        Permite definir o cambiar el detokenizador a utilizar.

        :param detokenizador: (objeto de detokenización de NLTK). Objeto \
            encargado de la detokenización de textos. Si el valor es 'None', se cargará por \
            defecto una instancia de la clase *TreebankWordDetokenizer*, de la librería NLTK.
        """
        if destokenizador is not None:
            self.destokenizador = destokenizador
        else:
            self.destokenizador = TreebankWordDetokenizer()

    def tokenizar(self, texto):
        """
        Realiza la función de tokenización (separar un texto en componentes sueltos, o tokens) sobre \
            uno o varios textos de entrada. 

        :param texto: (str o lista de strings). Texto o lista de textos sobre los cuales se desea \
            aplicar la tokenización.
        :return: (list) Si se ingresó un solo texto, devuelve la lista de tokens del texto. Si se \
            ingresó una lista de textos, se devuelve una lista en la que cada elemento es una lista de \
            tokens, con un elemento para cada texto de entrada.
        """
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
            print(
                'Tipo de entrada no válido. Debe ingresar un string o una lista de strings.')
            return None

    def post_destokenizacion(self, texto):
        """
        Hace algunos ajustes al texto, una vez ha pasado por la detokenización, para que \
            cumpla con las reglas de puntuación de los idiomas español e inglés. Es posible \
            que para otros idiomas sea necesario incluir ajustes adicionales. Si el texto de \
            entrada no contiene signos de puntuación (por ejemplo, si fue pasado por alguna \
            función de limpieza previamente), la salida será igual a la entrada.

        :param texto: (str). Texto que resulta de detokenizar una lista de tokens.
        :return: (str) Texto con los signos de puntuación ajustados.         
        """
        texto = texto.replace('¿ ', '¿')
        texto = texto.replace('¡ ', '¡')
        texto = texto.replace("' ", "'")
        texto = texto.replace(" .", ".")
        return texto

    def destokenizar(self, lista_tokens):
        """
        Realiza la función de detokenización (unir una lista de tokens, produciendo un texto) sobre \
            una o varias listas de tokens de entrada. 

        :param lista_tokens: (list). Lista de tokens, si es para un solo texto. Si es para varios \
        textos, se introduce una lista en la que cada elemento (uno para cada texto) es una \
        lista de tokens.
        :return: (str o lista de strings) Devuelve un solo string si se introdujo solo una lista de tokens. \
            Si se introdujeron varias listas de tokens, devuelve una lista de strings.
        """
        # Si la lista está vacía, se devuelve un string vacío
        if len(lista_tokens) < 1:
            return ''
        # Si es una sola lista de tokens se aplica el procedimiento directamente
        if isinstance(lista_tokens[0], str):
            texto = self.destokenizador.detokenize(lista_tokens)
            return self.post_destokenizacion(texto)
        # Si es una lista de listas de tokens, se aplica a cada elemento
        elif isinstance(lista_tokens[0], Iterable):
            salida = [self.post_destokenizacion(
                self.destokenizador.detokenize(i)) for i in lista_tokens]
            return salida
        else:
            print(
                'Tipo de entrada no válido. Debe ingresar una lista de tokens o una lista de listas de tokens.')
            return None


class TokenizadorEspacios():
    def tokenizar(self, texto):
        """
        Realiza la función de tokenización (separar un texto en componentes sueltos, o tokens) sobre \
            uno o varios textos de entrada. 

        :param texto: (str o lista de strings). Texto o lista de textos sobre los cuales se desea \
            aplicar la tokenización.
        :return: (list). Si se ingresó un solo texto, devuelve la lista de tokens del texto. Si se \
            ingresó una lista de textos, se devuelve una lista en la que cada elemento es una lista de \
            tokens, con un elemento para cada texto de entrada.
        """
        # Si es un string se aplica el procedimiento directamente
        if isinstance(texto, str):
            return texto.split()
        # Si es una lista o colección de strings, se aplica a cada uno
        elif isinstance(texto, Iterable):
            return [i.split() for i in texto]
        else:
            print(
                'Tipo de entrada no válido. Debe ingresar un string o una lista de strings.')
            return None

    def destokenizar(self, lista_tokens):
        """
        Realiza la función de detokenización (unir una lista de tokens, produciendo un texto) sobre \
            una o varias listas de tokens de entrada. 

        :param lista_tokens: (list). Lista de tokens, si es para un solo texto. Si es para varios \
        textos, se introduce una lista en la que cada elemento (uno para cada texto) es una \
        lista de tokens.
        :return: (str o lista de strings) Devuelve un solo string si se introdujo solo una lista de tokens. \
            Si se introdujeron varias listas de tokens, devuelve una lista de strings.
        """
        # Si la lista está vacía, se devuelve un string vacío
        if len(lista_tokens) < 1:
            return ''
        # Si es una sola lista de tokens se aplica el procedimiento directamente
        if isinstance(lista_tokens[0], str):
            return ' '.join(lista_tokens)
        # Si es una lista de listas de tokens, se aplica a cada elemento
        elif isinstance(lista_tokens[0], Iterable):
            return [' '.join(i) for i in lista_tokens]
        else:
            print(
                'Tipo de entrada no válido. Debe ingresar una lista de tokens o una lista de listas de tokens.')
            return None


def tokenizar(texto, tokenizador=None):
    """
    Función que aprovecha la clase TokenizadorNLTK para realizar la función de tokenización \
        (separar un texto en componentes sueltos, o tokens) sobre uno o varios textos de entrada.  

    :param texto: (str o lista de strings). Texto o lista de textos sobre los cuales se desea \
        aplicar la tokenización.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se cargará por defecto una instancia de la clase *TokenizadorNLTK*.
    :return: (list). Si se ingresó un solo texto, devuelve la lista de tokens del texto. Si se \
        ingresó una lista de textos, se devuelve una lista en la que cada elemento es una lista de \
        tokens, con un elemento para cada texto de entrada.
    """
    if tokenizador is None:
        tokenizador = TokenizadorNLTK()
    return tokenizador.tokenizar(texto)


def destokenizar(tokens, tokenizador=None):
    """
    Función que aprovecha la clase TokenizadorNLTK para realizar la función de detokenización \
    (unir una lista de tokens, produciendo un texto) sobre una o varias listas de tokens de entrada. 

    :param tokens: (list). Lista de tokens, si es para un solo texto. Si es para varios \
        textos, se introduce una lista en la que cada elemento (uno para cada texto) es una \
        lista de tokens.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se cargará por defecto una instancia de la clase *TokenizadorNLTK*.
    :return: (str o lista de strings) Devuelve un solo string si se introdujo solo una lista de tokens. \
        Si se introdujeron varias listas de tokens, devuelve una lista de strings.
    """
    if tokenizador is None:
        tokenizador = TokenizadorNLTK()
    return tokenizador.destokenizar(tokens)
