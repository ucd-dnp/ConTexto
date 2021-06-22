import json
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje
from utils.tokenizacion import TokenizadorEspacios

# Definir clases para el lematizador ###


class LematizadorSpacy:
    def __init__(
        self,
        lenguaje="es",
        dim_modelo="md",
        dict_lemmas=None,
        maxima_longitud=None,
        tokenizador=None,
    ):
        """
        Constructor por defecto de la clase `LematizadorSpacy`. Esta clase se \
        encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería `Spacy`.

        :param lenguaje: Define el lenguaje del texto que se desea \
            analizar. Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
            Valor por defecto `'es'`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        :param dim_modelo: Tamaño del modelo. 'lg' es grande (large), 'md' es \
            mediano (medium) y 'sm' es pequeño (small). Los modelos más \
            grandes usualmente obtienen mejores resultados, pero requieren \
            mayor tiempo de carga. Valor por defecto `'md'`.
        :type dim_modelo: {'lg', 'md', 'sm'}, opcional
        :param dict_lemmas: Diccionario (o *string* con \
            ubicación del archivo JSON que lo contiene) que permite modificar \
            y agregar lemas. Las llaves del diccionario son las palabras \
            completas y los valores del diccionario son los lemas escogidos \
            para cada palabra. Valor por defecto `None`.
        :type dict_lemmas: dict, str, opcional
        :param maxima_longitud: Establecer la máxima longitud (número de \
            caracteres) que acepta el lematizador en un texto de entrada. Si \
            `maxima_longitud = None`, se utilizará la máxima longitud que \
            trae Spacy por defecto (1 millón de caracteres). \
            Valor por defecto `None`.
        :type maxima_longitud: int, opcional
        :param tokenizador: Valor por defecto: None. Objeto encargado de la \
            detokenización de textos después de lematizar. Si el valor es \
            'None', se cargará por defecto una instancia de la clase \
            *TokenizadorEspacios*.
        :param tokenizador: Objeto encargado de la tokenización y \
            detokenización de textos después de lematizar. Si el valor es \
            `None`, se cargará por defecto una instancia de la clase \
            `TokenizadorEspacios`. Valor por defecto `None`.
        :type tokenizador: object, opcional
        """
        # Definir lenguaje del lematizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar lematizador
        self.iniciar_lematizador(dim_modelo, maxima_longitud)
        # Si se introdujo un diccionario personalizado, se utiliza
        if isinstance(dict_lemmas, dict):
            self.modificar_lemmas(dict_lemmas)
        # Si es la ubicación del archivo, primero se carga
        elif isinstance(dict_lemmas, str):
            try:
                dict_lemmas = json.load(open(dict_lemmas))
                self.modificar_lemmas(dict_lemmas)
            except BaseException:
                print("No se pudo cargar el diccionario de lemas")
        self.tokenizador = (
            TokenizadorEspacios() if tokenizador is None else tokenizador
        )

    def establecer_lenguaje(self, lenguaje):
        """
        Define el lenguaje del lematizador.

        :param lenguaje: Define el lenguaje del Lematizador. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
            Valor por defecto `'es'`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, dim_modelo, maxima_longitud):
        """
        Inicia el lematizador con el tamaño del modelo de lematización basado \
        en en los tamaños de la librería `Spacy`. Los modelos más grandes \
        usualmente obtienen mejores resultados, pero requieren mayor tiempo \
        de carga.

        :param dim_modelo: Tamaño del modelo. 'lg' es grande (large), 'md' es \
            mediano (medium) y 'sm' es pequeño (small). Los modelos más \
            grandes usualmente obtienen mejores resultados, pero requieren \
            mayor tiempo de carga. Valor por defecto `'md'`.
        :type dim_modelo: {'lg', 'md', 'sm'}, opcional
        :param maxima_longitud: Establecer la máxima longitud (número de \
            caracteres) que acepta el lematizador en un texto de entrada. Si \
            `maxima_longitud = None`, se utilizará la máxima longitud que \
            trae Spacy por defecto (1 millón de caracteres). \
            Valor por defecto `None`.
        :type maxima_longitud: int, opcional
        """
        self.lematizador = None
        if self.lenguaje is not None:
            from utils.spacy_funcs import cargar_modelo

            self.lematizador = cargar_modelo(
                dim_modelo, self.lenguaje, maxima_longitud
            )
            # Se añade este proceso para poder deshabilitar el parser.
            # Tomado de https://bit.ly/38uMzC6
            self.lematizador.add_pipe(
                self.lematizador.create_pipe("sentencizer")
            )

    def modificar_lemmas(self, dict_lemmas):
        """
        Define lemas asociados a palabras escogidas por el usuario. Estos \
        nuevos lemas serán adicionados al diccionario de lemas del \
        lematizador.

        :param dict_lemmas: Diccionario que permite modificar \
            y agregar lemas. Las llaves del diccionario son las palabras \
            completas y los valores del diccionario son los lemas escogidos \
            para cada palabra.
        :type dict_lemmas: dict, opcional
        """
        # Definir función auxiliar
        def cambiar_propiedades_lemma(doc):
            for token in doc:
                if token.text in dict_lemmas:
                    token.lemma_ = dict_lemmas[token.text]
            return doc

        # Aplicar la función para modificar el lematizador
        if (self.lematizador is not None) and (self.lematizador != -1):
            self.lematizador.add_pipe(cambiar_propiedades_lemma, first=True)

    def lematizar(self, texto, limpiar=True):
        """
        Lematización de texto.

        :param texto: El texto que se desea lematizar.
        :type text: str
        :param limpiar: Especifica si se desea hacer una limpieza básica del \
            texto antes de la lematización. Valor por defecto `True`.
        :type limpiar: bool, opcional
        :return: (str) Retorna el texto lematizado.
        """
        if limpiar:
            texto = limpieza_basica(texto)
        lemas = self.lematizador(texto, disable=["ner", "parser"])
        return self.tokenizador.destokenizar([token.lemma_ for token in lemas])


# Implementación alternativa, utilizando stanza


class LematizadorStanza:
    def __init__(
        self,
        lenguaje="es",
        modelo_lemas=None,
        dict_lemmas=None,
        archivo_salida=None,
        tokenizador=None,
    ):
        """
        Constructor por defecto de la clase `LematizadorStanza`. Esta clase \
        se encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería `Stanza`.

        :param lenguaje: Define el lenguaje del Lematizador. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
            Valor por defecto `'es'`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        :param modelo_lemas: Especifica la ruta de un modelo de lemas \
            personalizado. Si `modelo_lemas = None`, utiliza el modelo \
            genérico de lemas de `Stanza`. Valor por defecto `None`.
        :type modelo_lemas: str, opcional
        :param dict_lemmas: Diccionario (o *string* con \
            ubicación del archivo JSON que lo contiene) que permite modificar \
            y agregar lemas. Las llaves del diccionario son las palabras \
            completas y los valores del diccionario son los lemas escogidos \
            para cada palabra. Valor por defecto `None`.
        :type dict_lemmas: dict, str, opcional
        :param archivo_salida:Especifica la ruta del archivo de salida del \
            modelo de lemas modificado. Si `archivo_salida = None`, el \
            resultado de la lematizacción se guarda en un archivo temporal \
            que eventualmente será borrado.
        :type archivo_salida: str, opcional
        :param tokenizador: Objeto encargado de la tokenización y \
            detokenización de textos después de lematizar. Si el valor es \
            `None`, se cargará por defecto una instancia de la clase \
            `TokenizadorEspacios`. Valor por defecto `None`.
        :type tokenizador: object, opcional
        """
        # Definir lenguaje del lematizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar lematizador
        self.iniciar_lematizador(modelo_lemas)
        # Si se introdujo un diccionario personalizado, se utiliza
        if isinstance(dict_lemmas, dict):
            self.modificar_lemmas(dict_lemmas, modelo_lemas, archivo_salida)
        # Si es la ubicación del archivo, primero se carga
        elif isinstance(dict_lemmas, str):
            try:
                dict_lemmas = json.load(open(dict_lemmas))
                self.modificar_lemmas(dict_lemmas)
            except BaseException:
                print("No se pudo cargar el diccionario de lemas")
        self.tokenizador = (
            TokenizadorEspacios() if tokenizador is None else tokenizador
        )

    def establecer_lenguaje(self, lenguaje):
        """
        Define el lenguaje del lematizador.

        :param lenguaje: Define el lenguaje del Lematizador. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, modelo_lemas):
        """
        Inicia el lematizador de `Stanza` y permite ingresar la ruta de un \
        modelo de lematización personalizado. En caso de no especificar la \
        ruta se utilizará el modelo que trae `Stanza` por defecto para el \
        lenguaje seleccionado.

        :param modelo_lemas: Especifica la ruta de un modelo de lemas \
            personalizado. Si `modelo_lemas = None`, utiliza el modelo \
            genérico de lemas de `Stanza`.
        :type modelo_lemas: str, opcional
        """
        from utils.stanza_funcs import stanza_pipeline

        self.lematizador = None
        if self.lenguaje is not None:
            self.lematizador = stanza_pipeline(
                self.lenguaje, modelo_lemas=modelo_lemas
            )

    def modificar_lemmas(
        self, dict_lemmas, archivo_entrada=None, archivo_salida=None, gpu=False
    ):
        """
        Permite modificar o añadir nuevos lemas al modelo original de \
        lematización. Adicionalmente, permite ingresar un modelo \
        personalizado desde una ruta específica.

        :param dict_lemmas: Diccionario que permite modificar \
            y agregar lemas. Las llaves del diccionario son las palabras \
            completas y los valores del diccionario son los lemas escogidos \
            para cada palabra.
        :type dict_lemmas: dict
        :param archivo_entrada: Si `archivo_entrada = None`, se escoge un \
            modelo de lematización genérico. De lo contrario, especifica la \
            ruta del modelo de lematización personalizado que se quiere \
            utilizar. Valor por defecto `None`.
        :type archivo_entrada: str, opcional
        :param archivo_salida:Especifica la ruta del archivo de salida del \
            modelo de lemas modificado. Si `archivo_salida = None`, el \
            resultado de la lematizacción se guarda en un archivo temporal \
            que eventualmente será borrado.
        :type archivo_salida: str, opcional
        :param gpu: Correr el proceso de la lematización en la GPU (solo si \
            si tiene GPU). Valor por defecto `False`.
        :type gpu: bool, opcional
        """
        from utils.stanza_funcs import modificar_modelo

        self.lematizador = modificar_modelo(
            self.lematizador,
            "lemma",
            dict_lemmas,
            archivo_entrada,
            archivo_salida,
            gpu,
        )

    def lematizar(self, texto, limpiar=True):
        """
        Lematización de texto.

        :param texto: El texto que se desea lematizar.
        :type text: str
        :param limpiar: Especifica si se desea hacer una limpieza básica del \
            texto antes de la lematización. Valor por defecto `True`.
        :type limpiar: bool, opcional
        :return: (str) Retorna el texto lematizado.
        """
        if limpiar:
            texto = limpieza_basica(texto)
        doc = self.lematizador(texto)
        # Extraer los lemas de cada palabra, de cada frase, y juntarlos
        return self.tokenizador.destokenizar(
            [w.lemma for s in doc.sentences for w in s.words]
        )


# Definir función que envuelva la funcionalidad básica de las clases ###


def lematizar_texto(
    texto,
    lenguaje="es",
    libreria="spacy",
    limpiar=True,
    lematizador=None,
    dict_lemmas=None,
    dim_modelo="md",
    modelo_lemas=None,
    archivo_salida=None,
    maxima_longitud=None,
    tokenizador=None,
):
    """
    Función que retorna un texto lematizado por la librería `Spacy` o \
    `Stanza`. \
    Permite escoger el idioma de lematización, si hacer limpieza del texto, \
    modificar los modelos de lematizaciones originales y guardar los modelos \
    modificados.

    :param texto: Texto de entrada a ser lematizado.
    :type texto: str
    :param lenguaje: Define el lenguaje del Lematizador. \
        Para mayor información, consultar la sección de \
        :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
        Valor por defecto `'es'`.
    :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
    :param libreria: Se define la librería de lematización para ser utilizada \
        en el texto. Las opciones son las librerías `spacy` o `stanza`.
        Valor por defecto `spacy`.
    :type libreria: {'spacy', 'stanza'}
    :param limpiar: Si `limpiar = True` se hace una limpieza básica de texto \
        antes del proceso de lematización. Valor por defecto `True`.
    :type limpiar: bool, opcional
    :param lematizador:  Objeto de la clase `LematizadorSpacy` o \
        `LematizadorStanza` para el proceso de lematización sobre el texto \
        de entrada. Se puede utilizar para lematización a varios textos a la \
        vez, sin necesidad de inicializar un lematizador en cada ocasión. \
        Esto puede representar ahorro en tiempos al momento de aplicar la \
        función. Valor por defecto `None`.
    :type lematizador: {LematizadorStanza, LematizadorSpacy}, opcional
    :param dict_lemmas: Diccionario que permite modificar \
            y agregar lemas. Las llaves del diccionario son las palabras \
            completas y los valores del diccionario son los lemas escogidos \
            para cada palabra.
    :type dict_lemmas: dict
    :param dim_modelo: Tamaño del modelo. 'lg' es grande (large), 'md' es \
            mediano (medium) y 'sm' es pequeño (small). Los modelos más \
            grandes usualmente obtienen mejores resultados, pero requieren \
            mayor tiempo de carga. Aplica unicamente para `LematizadorSpacy`. \
            Valor por defecto `'md'`.
    :type dim_modelo: {'lg', 'md', 'sm'}, opcional.
    :param modelo_lemas: Especifica la ruta de un modelo de lemas \
        personalizado. Si `modelo_lemas = None`, utiliza el modelo \
        genérico de lemas de `Stanza`. Aplica únicamente para la \
        lematización con Stanza.
    :type modelo_lemas: str, opcional
    :param archivo_salida: Especifica la ruta del archivo de salida del \
        modelo de lemas modificado. Si `archivo_salida = None`, el \
        resultado de la lematizacción se guarda en un archivo temporal \
        que eventualmente será borrado. Aplica únicamente para la \
        lematización con Stanza.
    :type archivo_salida: str, opcional
    :param maxima_longitud: Establecer la máxima longitud (número de \
        caracteres) que acepta el lematizador en un texto de entrada. Si \
        `maxima_longitud = None`, se utilizará la máxima longitud que \
        trae `Spacy` por defecto (1 millón de caracteres). Aplica únicamente \
        para la lematización con Spacy. Valor por defecto `None`.
    :type maxima_longitud: int, opcional
    :param tokenizador: Objeto encargado de la tokenización y \
        detokenización de textos después de lematizar. Si el valor es \
        `None`, se cargará por defecto una instancia de la clase \
        `TokenizadorEspacios`. Valor por defecto `None`.
    :type tokenizador: object, opcional
    :return: (str) Texto lematizado.
    """
    # Si no se provee un lematizador, este debe ser inicializado
    if lematizador is None:
        if lenguaje == "auto":
            lenguaje = detectar_lenguaje(texto)
        if libreria.lower() == "spacy":
            lematizador = LematizadorSpacy(
                lenguaje, dim_modelo, dict_lemmas, maxima_longitud, tokenizador
            )
        elif libreria.lower() == "stanza":
            lematizador = LematizadorStanza(
                lenguaje,
                modelo_lemas,
                dict_lemmas,
                archivo_salida,
                tokenizador,
            )
        else:
            print(
                (
                    "Por favor escoja una librería válida "
                    "para el lematizador (Spacy o Stanza)"
                )
            )
            return None
    # Si el lenguaje no se reconoce, se envía mensaje
    if lematizador.lematizador is None:
        print("Lenguaje no válido.")
        return None
    # Devolver la lematización del texto
    return lematizador.lematizar(texto, limpiar)
