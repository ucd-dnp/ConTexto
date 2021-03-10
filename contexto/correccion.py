import json
from spellchecker import SpellChecker
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje
from utils.tokenizacion import TokenizadorNLTK

# Definir clase para el corrector ortográfico ###


class Corrector:
    def __init__(
        self, lenguaje, diccionario=None, distancia=2, tokenizador=None
    ):
        """
        Constructor por defecto de la clase Corrector. Esta clase se encarga \
        de realizar corrección ortográfica sobre textos.

        :param lenguaje: (str) Lenguaje de los textos a los que se les va a a\
            plicar corrección ortográfica. Para mayor información, consultar \
            la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        :param diccionario: (dict, list o string) Valor por defecto: None. Di\
            ccionario (o string con ubicación del archivo JSON que lo contien\
            e), o lista que permite modificar y agregar palabras. Si es una l\
            ista, contiene las palabras que serán consideradas como válidas o\
             correctas. Si es un diccionario, las llaves del diccionario son \
            las palabras que serán consideradas como válidas o correctas, y l\
            os valores del diccionario son las frecuencias de cada palabra en\
             el diccionario. Las frecuencias son utilizadas como criterio de \
            desempate, cuando una palabra incorrecta tiene más de una palabra\
             candidata para la corrección. Si se deja este parámetro como \
            None, se cargará el diccionario por defecto que trae la librería \
            `spellchecker` para el lenguaje determinado.
        :param distancia: (int) Valor por defecto: 2. Máxima distancia de Lev\
            enshtein que puede haber entre una palabra incorrecta (o no recon\
            ocida) y las palabras del diccionario para determinar si hay pala\
            bras candidatas para realizar la corrección.
        :param tokenizador: Valor por defecto: None. Objeto encargado de la t\
            okenización y detokenización de textos. Si el valor es 'None', se\
             cargará por defecto una instancia de la clase *TokenizadorNLTK*.
        """
        # Definir lenguaje del corrector ortográfico
        self.establecer_lenguaje(lenguaje)
        # Inicializar corrector
        self.iniciar_corrector(diccionario)
        self.establecer_distancia(distancia)
        self.tokenizador = (
            TokenizadorNLTK() if tokenizador is None else tokenizador
        )

    def establecer_lenguaje(self, lenguaje):
        """
        Permite definir o cambiar el lenguaje de los textos sobre los cuales \
        van a aplicarse el objeto de la clase Corrector.

        :param lenguaje: (str) Lenguaje de los textos a los que se les va a a\
            plicar corrección ortográfica. Para mayor información, consultar \
            la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_corrector(self, diccionario):
        """
        Inicializa el objeto de la clase `SpellChecker` de la librería spellc\
        hecker, para el lenguaje definido previamente, y lo asigna al atribut\
        o "corrector" del objeto de clase Corrector.

        :param diccionario: (dict, list o string) Diccionario (o string con u\
            bicación del archivo JSON que lo contiene), o lista que permite m\
            odificar y agregar palabras. Si es una lista, contiene las palabr\
            as que serán consideradas como válidas o correctas. Si es un dicc\
            ionario, las llaves del diccionario son las palabras que serán co\
            nsideradas como válidas o correctas, y los valores del diccionari\
            o son las frecuencias de cada palabra en el diccionario. Las frec\
            uencias son utilizadas como criterio de desempate, cuando una pal\
            abra incorrecta tiene más de una palabra candidata para la correc\
            ción.
        """
        self.corrector = None
        if self.lenguaje is not None:
            if isinstance(diccionario, str):
                self.corrector = SpellChecker(local_dictionary=diccionario)
            elif type(diccionario) in [dict, list]:
                self.corrector = SpellChecker(language=self.lenguaje)
                self.actualizar_diccionario(diccionario)
            else:
                self.corrector = SpellChecker(language=self.lenguaje)

    def establecer_distancia(self, distancia):
        """
        Establece la distancia máxima que utilizará el algoritmo de corrección\
         de ortografía para determinar si hay palabras candidatas para corregi\
        r una palabra incorrecta o no reconocida.

        :param distancia: (int) Valor por defecto: 2. Máxima distancia de Lev\
            enshtein que puede haber entre una palabra incorrecta (o no recon\
            ocida) y las palabras del diccionario para \
            determinar si hay palabras candidatas para realizar la corrección.
        """
        if self.corrector is not None:
            self.corrector.distance = distancia

    def actualizar_diccionario(self, diccionario):
        """
        Actualiza el diccionario que contiene las palabras válidas o reconoci\
        das disponibles para realizar la corrección ortográfica. Las palabras\
         contenidas en el argumento *diccionario* de esta función serán añadi\
        das (o sus frecuencias serán actualizadas) en el diccionario que ya e\
        xiste en el objeto de la clase Corrector.

        :param diccionario: (dict, list o string) Diccionario (o string con u\
            bicación del archivo JSON que lo contiene), o lista que permite m\
            odificar y agregar palabras. Si es una lista, contiene las palabr\
            as que serán consideradas como válidas o correctas. Si es un dicc\
            ionario, las llaves del diccionario son las palabras que serán co\
            nsideradas como válidas o correctas, y los valores del diccionari\
            o son las frecuencias de cada palabra en el diccionario. Las frec\
            uencias son utilizadas como criterio de desempate, cuando una pal\
            abra incorrecta tiene más de una palabra candidata para la correc\
            ción.
        """
        if isinstance(diccionario, str):
            diccionario = json.load(open(diccionario))
        if isinstance(diccionario, list):
            diccionario = [palabra.lower() for palabra in diccionario]
            self.corrector.word_frequency.load_words(diccionario)
        elif isinstance(diccionario, dict):
            self.quitar_palabras(list(diccionario.keys()))
            for key in diccionario.keys():
                self.corrector.word_frequency.load_words(
                    [key.lower()] * diccionario[key]
                )
        else:
            pass

    def quitar_palabras(self, palabras):
        """
        Quita del diccionario del corrector una o más palabras proporciona\
        das en el argumento *palabras*, haciendo que estas ya no sean reco\
        nocidas como palabras válidas o correctas al momento de hacer corr\
        ección ortográfica.

        :param palabras: (str o list) Palabra o lista de palabras que se dese\
            an quitar del diccionario del objeto de la clase Corrector, para \
            que no sean recnocidas como correctas al momento de hacer la corr\
            ección ortográfica.
        """
        if isinstance(palabras, str):
            palabras = [palabras]
        # Quitar de la lista palabras que no estén en el diccionario
        palabras = [p for p in palabras if self.frecuencia_palabra(p) > 0]
        if len(palabras) > 0:
            self.corrector.word_frequency.remove_words(palabras)

    def agregar_palabras(self, palabras):
        """
        Añade al diccionario del corrector una o más palabras proporcionadas \
        en el argumento *palabras*, haciendo que estas sean reconocidas como \
        palabras válidas o correctas al momento de hacer corrección ortográfi\
        ca.

        :param palabras: (str o list) Palabra o lista de palabras que se dese\
            an añadir al diccionario del objeto de la clase Corrector, para q\
            ue sean reconocidas como correctas al momento de hacer la correcc\
            ión ortográfica.
        """
        if isinstance(palabras, str):
            palabras = [palabras]
        self.actualizar_diccionario(palabras)

    def palabras_conocidas(self, texto):
        """
        A partir de un texto de entrada, devuelve un conjunto (objeto de clas\
        e *set* de Python) con las palabras del texto que se reconocen por es\
        tar presentes en el diccionario del corrector.

        :param texto: (str) Texto para el que se desean hayar las palabras co\
            nocidas.
        :return: (set) Conjunto de palabras conocidas presentes en el texto \
            de entrada.
        """
        tokens = self.tokenizador.tokenizar(texto)
        return self.corrector.known(tokens)

    def palabras_desconocidas(self, texto):
        """
        A partir de un texto de entrada, devuelve un conjunto (objeto de clas\
        e *set* de Python) con las palabras del texto que no están incluidas \
        en el diccionario del corrector y por lo tanto no se reconocen.

        :param texto: (str) Texto para el que se desean hallar las palabras d\
            esconocidas.
        :return: (set) Conjunto de palabras desconocidas presentes en el text\
            o de entrada.
        """
        tokens = self.tokenizador.tokenizar(texto)
        return self.corrector.unknown(tokens)

    def palabras_candidatas(self, palabra):
        """
        Para una palabra de entrada, retorna un conjunto de palabras que podr\
        ían ser utilizadas para corregirla. Si la palabra de entrada es corre\
        cta (está dentro del diccionario del corrector) o no tienen ninguna p\
        alabra candidata con una distancia menor o igual a la establecida en \
        el parámetro *distancia* de la clase Corrector, la función devolverá \
        la misma palabra de entrada.

        :param palabra: (str) Palabra para la que se quieren conocer palabras\
             candidatas para su corrección ortográfica.
        :return: (set) Conjunto de palabras candidatas para corregir la palab\
            ra de entrada.
        """
        return self.corrector.candidates(palabra)

    def frecuencia_palabra(self, palabra):
        """
        Para una palabra de entrada, devuelve la frecuencia de la misma, de a\
        cuerdo al diccionario del corrector. Si la palabra es desconocida (no\
         se encuentra en el diccionario), la frecuencia retornada será de \
        cero.

        :param palabra: (str) Palabra para la cual se desea conocer la frecue\
            ncia de aparición en el diccionario del corrector.
        :return: (int) Número mayor o igual a cero que indica la frecuencia d\
            e la palabra consultada en el diccionario del corrector.
        """
        return self.corrector[palabra]

    def probabilidad_palabra(self, palabra):
        """
        Para una palabra de entrada, devuelve la probabilidad de aparición de\
         la misma, entendida como su frecuencia sobre la suma de las frecuenc\
        ias de todas las palabras disponibles, de acuerdo al diccionario del \
        corrector. Si la palabra es desconocida (no se encuentra en el diccio\
        nario), la probabilidad retornada será de cero.

        :param palabra: (str) Palabra para la cual se desea conocer la probab\
            ilidad de aparición en el diccionario del corrector.
        :return: (float) Probabilidad, entre 0 y 1, de aparición de la \
            palabra.
        """
        return self.corrector.word_probability(palabra)

    def correccion_ortografia(self, texto, limpieza=False):
        """
        Realiza corrección ortográfica sobre un texto de entrada, identifican\
        do las palabras que no están en el diccionario del corrector y cambiá\
        ndolas por su candidata más frecuente o probable, siempre y cuando ha\
        ya por lo menos una palabra candidata que cumpla con la máxima distan\
        cia de Levenshtein permitida.

        :param texto: (str) Texto al cuál se desea aplicar corrección ortográ\
            fica.
        :param limpieza: (bool) {True, False} Valor por defecto: False. Argum\
            ento opcional que define si se desea hacer una limpieza básica (a\
            plicando la función `limpieza_basica` del módulo `limpieza`) al t\
            exto antes de aplicar la corrección ortográfica.
        :return: (str) Texto de entrada luego de la corrección ortográfica.
        """
        if limpieza:
            # Limpieza básica del texto para que no afecte la corrección
            texto = limpieza_basica(texto, quitar_numeros=False)
        lista_palabras = self.tokenizador.tokenizar(texto)
        desconocidas = self.corrector.unknown(lista_palabras)
        texto_corregido = [
            self.corrector.correction(p)
            if len(p) > 1 and p in desconocidas
            else p
            for p in lista_palabras
        ]
        return self.tokenizador.destokenizar(texto_corregido)


# Función que envuelve la funcionalidad básica de la clase


def corregir_texto(
    texto,
    lenguaje="es",
    corrector=None,
    diccionario=None,
    distancia=2,
    limpieza=False,
    tokenizador=None,
):
    """
    Función que aprovecha la clase Corrector para realizar corrección ortográ\
    fica sobre un texto de entrada.

    :param texto: (str) Texto al cuál se desea aplicar corrección ortográfica.
    :param lenguaje: (str) Lenguaje de los textos a los que se les va a aplic\
        ar corrección ortográfica. Para mayor información, consultar la secci\
        ón de \
        :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
    :param corrector: (Corrector) Parámetro opcional. Objeto de la clase Corr\
        ector para aplicar corrección ortográfica sobre el texto de entrada. \
        Se puede utilizar para corregir varios textos a la vez, sin necesidad\
         de inicializar una instancia de la clase Corrector en cada ocasión. \
        Esto puede representar ahorro en tiempos al momento de aplicar la fun\
        ción.
    :param diccionario: (dict, list o str) Valor por defecto: None. Diccionar\
        io (o string con ubicación del archivo JSON que lo contiene), o lista\
         que permite modificar y agregar palabras. Si es una lista, contiene \
        las palabras que serán consideradas como válidas o correctas. Si es u\
        n diccionario, las llaves del diccionario son las palabras que serán \
        consideradas como válidas o correctas, y los valores del diccionario \
        son las frecuencias de cada palabra en el diccionario. Las frecuencia\
        s son utilizadas como criterio de desempate, cuando una palabra incor\
        recta tiene más de una palabra candidata para la corrección. Si se de\
        ja este parámetro como None, se cargará el diccionario por defecto qu\
        e trae la librería `spellchecker` para el lenguaje determinado.
    :param distancia: (int) Valor por defecto: 2. Máxima distancia de Levensh\
        tein que puede haber entre una palabra incorrecta (o no reconocida) y\
         las palabras del diccionario para determinar si hay palabras candida\
        tas para realizar la corrección.
    :param limpieza: (bool) {True, False} Valor por defecto: False. Argumento\
         opcional que define si se desea hacer una limpieza básica (aplicando\
         la función `limpieza_basica` del módulo `limpieza`) al texto antes d\
        e aplicar la corrección ortográfica.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la token\
        ización y detokenización de textos. Si el valor es 'None', se cargará\
         por defecto una instancia de la clase *TokenizadorNLTK*.
    :return: (str) Texto de entrada luego de la corrección ortográfica.
    """
    if corrector is None:
        if lenguaje == "auto":
            lenguaje = detectar_lenguaje(texto)
        corrector = Corrector(lenguaje, diccionario, distancia, tokenizador)

    if corrector.corrector is None:
        print("Lenguaje no válido.")
        return None

    return corrector.correccion_ortografia(texto, limpieza)
