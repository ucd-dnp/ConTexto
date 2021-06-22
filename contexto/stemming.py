import nltk.stem
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje
from utils.tokenizacion import TokenizadorNLTK

# Definir clase para el stemmer ###


class Stemmer:
    def __init__(self, lenguaje="es", tokenizador=None):
        """
        Constructor por defecto de la clase `Stemmer`. Esta clase se encarga \
        de hacer la operación de *stemming*, o reducción de palabras a su \
        raíz, en textos.

        :param lenguaje: Lenguaje de los textos a los que se va a aplicar \
            *stemming*. Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
            Valor por defecto `'es'`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        :param tokenizador: Objeto encargado de la tokenización y \
            detokenización de textos. Si el valor es 'None', se utilizará \
            por defecto una instancia de la clase `TokenizadorNLTK`.
        :type tokenizador: Tokenizer, opcional
        :return: (Stemmer) Objeto del tipo de la clase `Stemmer`.
        """
        # Definir lenguaje del stemmer
        self.establecer_lenguaje(lenguaje)
        # Inicializar stemmer
        self.iniciar_stemmer()
        # Para tokenizar los textos antes de aplicar el stemming
        self.tokenizador = (
            TokenizadorNLTK() if tokenizador is None else tokenizador
        )

    def establecer_lenguaje(self, lenguaje):
        """
        Permite definir o cambiar el lenguaje de los textos sobre los cuales \
        va a aplicarse el objeto de la case Stemmer.

        :param lenguaje: Lenguaje de los textos a los que se va a aplicar \
            *stemming*. Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
        :type lenguaje: {'es', 'en', 'fr', 'ge'}
        """
        self.lenguaje = definir_lenguaje(lenguaje, simplificado=False)

    def iniciar_stemmer(self):
        """
        Inicializa el objeto de la clase `SnowballStemmer` de la librería \
        `NLTk`, para el lenguaje definido previamente, y lo asigna al \
        atributo "stemmer" del objeto de clase `Stemmer`.
        """
        if self.lenguaje is not None:
            self.stemmer = nltk.stem.SnowballStemmer(self.lenguaje)
        else:
            self.stemmer = None

    def stemming(self, texto, limpiar=False):
        """
        Aplica *stemming* sobre un texto de entrada, y devuelve el texto \
        resultante.

        :param texto: Texto al que se desea aplicar el *stemming*.
        :type texto: str
        :param limpiar: Define si se desea hacer una limpieza básica \
            (aplicando la función `limpieza_basica` del módulo \
            `limpieza`) al texto antes de aplicar el *stemming*. \
            Valor por defecto `False`.
        :type limpiar: bool, opcional
        :return: (str) Texto luego de la aplicación del *stemming*.
        """
        if limpiar:
            texto = limpieza_basica(texto)
        tokens = self.tokenizador.tokenizar(texto)
        salida = [self.stemmer.stem(p) for p in tokens]
        return self.tokenizador.destokenizar(salida)


# Definir función que envuelva la funcionalidad básica de la clase ###


def stem_texto(texto, lenguaje="es", limpiar=False, stemmer=None):
    """
    Función que aprovecha la clase `Stemmer` para realizar *stemming*, o \
    reducción de palabras a su raíz, en un texto de entrada.

    :param texto: Texto al que se desea aplicar el *stemming*.
    :type texto: str
    :param lenguaje: Lenguaje de los textos a los que se va a aplicar \
        *stemming*. Para mayor información, consultar la sección de \
        :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
        Valor por defecto `'es'`.
    :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
    :param limpiar: Define si se desea hacer una limpieza básica \
        (aplicando la función `limpieza_basica` del módulo \
        `limpieza`) al texto antes de aplicar el *stemming*. \
        Valor por defecto `False`.
    :type limpiar: bool, opcional
    :param stemmer: Objeto de la clase `Stemmer` para aplicar *stemming* \
        sobre el texto de entrada. \
        Se puede utilizar para aplicar *stemming* a varios textos a la \
        vez, sin necesidad de inicializar una instancia de la clase *Stemmer* \
        en cada ocasión. Esto puede representar ahorro en tiempos al momento \
        de aplicar la función. Valor por defecto `None`.
    :type stemmer: Stemmer, opcional
    :return: (str) Texto luego de la aplicación del *stemming*.
    """
    # Si no se provee un stemmer, este debe ser inicializado
    if stemmer is None:
        if lenguaje == "auto":
            lenguaje = detectar_lenguaje(texto)
        stemmer = Stemmer(lenguaje)

    if stemmer.stemmer is None:
        print("Lenguaje no válido.")
        return None

    return stemmer.stemming(texto, limpiar)
