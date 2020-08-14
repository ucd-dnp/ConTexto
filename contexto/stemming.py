import nltk.stem
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje

### Definir clase para el stemmer ###


class Stemmer():
    def __init__(self, lenguaje):
        """

        :param lenguaje:
        """
        # Definir lenguaje del stemmer
        self.establecer_lenguaje(lenguaje)
        # Inicializar stemmer
        self.iniciar_stemmer()

    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje:
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje, simplificado=False)

    def iniciar_stemmer(self):
        """

        :return:
        """
        if self.lenguaje is not None:
            self.stemmer = nltk.stem.SnowballStemmer(self.lenguaje)
        else:
            self.stemmer = None

    def stemming(self, texto, limpiar=True):
        """

        :param texto:
        :param limpiar:
        :return:
        """
        if limpiar:
            texto = limpieza_basica(texto)
        return ' '.join([self.stemmer.stem(palabra)
                         for palabra in texto.split(" ")])


### Definir función que envuelva la funcionalidad básica de la clase ###

def stem_texto(texto, lenguaje='es', limpiar=True, stemmer=None):
    """

    :param texto:
    :param lenguaje:
    :param limpiar:
    :param stemmer:
    :return:
    """
    # Si no se provee un stemmer, este debe ser inicializado
    if stemmer is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        stemmer = Stemmer(lenguaje)

    if stemmer.stemmer is None:
        print('Lenguaje no válido.')
        return None

    return stemmer.stemming(texto, limpiar)
