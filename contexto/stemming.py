import nltk.stem
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje

### Definir clase para el stemmer ###


class Stemmer():
    def __init__(self, lenguaje):
        """
        Constructor por defecto de la clase Stemmer. Esta clase se encarga \
        de hacer la operación de *stemming*, o reducción de palabras a su \
        raíz, en textos.

        :param lenguaje: (string) {'es', 'en', 'fr', 'de'}. Lenguaje de los\
            textos a los que se va a aplicar *stemming*.
        :return: (Stemmer). Objeto del tipo de la clase Stemmer
        """
        # Definir lenguaje del stemmer
        self.establecer_lenguaje(lenguaje)
        # Inicializar stemmer
        self.iniciar_stemmer()

    def establecer_lenguaje(self, lenguaje):
        """
        Permite definir o cambiar el lenguaje de los textos sobre los cuales \
            va a aplicarse el objeto de la case Stemmer.

        :param lenguaje: (string) {'es', 'en', 'fr', 'de'}. Lenguaje de los\
            textos a los que se va a aplicar stemming.
        """
        self.lenguaje = definir_lenguaje(lenguaje, simplificado=False)

    def iniciar_stemmer(self):
        """
        Inicializa el objeto de la clase `SnowballStemmer` de la librería NLTk, \
        para el lenguaje definido previamente, y lo asigna al atributo "stemmer" \
        del objeto de clase Stemmer. 
        """
        if self.lenguaje is not None:
            self.stemmer = nltk.stem.SnowballStemmer(self.lenguaje)
        else:
            self.stemmer = None

    def stemming(self, texto, limpiar=True):
        """
        Aplica *stemming* sobre un texto de entrada, y devuelve el texto \
            resultante.

        :param texto: (string). Texto al que se le desea aplicar el *stemming*. 
        :param limpiar: (bool) {True, False}. Valor por defecto: True. Argumento \
            opcional que define si se desea hacer una limpieza básica (\
            aplicando la función `limpieza_basica` del módulo `limpieza`) al \
            texto antes de aplicar el *stemming*.
        :return: (string). Texto luego de la aplicación del *stemming*.
        """
        if limpiar:
            texto = limpieza_basica(texto)
        return ' '.join([self.stemmer.stem(palabra)
                         for palabra in texto.split(" ")])


### Definir función que envuelva la funcionalidad básica de la clase ###

def stem_texto(texto, lenguaje='es', limpiar=True, stemmer=None):
    """
    Función que aprovecha la clase Stemmer para realizar *stemming*, o \
        reducción de palabras a su raíz, en un texto de entrada.
        
    :param texto: (string). Texto al que se le desea aplicar el *stemming*.
    :param lenguaje: (string) {'es', 'en', 'fr', 'de'}. Lenguaje del \
        texto al que se va a aplicar *stemming*.
    :param limpiar: (bool) {True, False}. Valor por defecto: True. Define \
        si se desea hacer una limpieza básica (aplicando la función  \
        `limpieza_basica` del módulo `limpieza`) al texto de entrada,  \
        antes de aplicar el *stemming*.
    :param stemmer: (Stemmer). Parámetro opcional. Objeto de la clase Stemmer para aplicar \
        *stemming* sobre el texto de entrada. Se puede utilizar para aplicar \
        *stemming* a varios textos a la vez, sin necesidad de inicializar una \
        instancia de la clase Stemmer en cada ocasión. Esto puede representar \
        ahorro en tiempos al momento de aplicar la función.
    :return: (string). Texto luego de la aplicación del *stemming*.
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
