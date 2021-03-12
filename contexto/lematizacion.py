import json
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje
from utils.tokenizacion import TokenizadorEspacios

# Definir clases para el lematizador ###


class LematizadorSpacy:
    def __init__(
        self,
        lenguaje,
        dim_modelo="md",
        dict_lemmas=None,
        maxima_longitud=None,
        tokenizador=None,
    ):
        """
        Constructor por defecto de la clase LematizadorSpacy. Esta clase se \
        encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería Spacy.

        :param lenguaje: (str) Define el lenguaje del texto a ser tratado. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        :param dim_modelo: (str) {'lg', 'md', 'sm'} Valor por defecto: 'md'. \
            Se define el tamaño del modelo. 'lg' es grande (large), 'md' es m\
            ediano (medium) y 'sm' es pequeño (small). Los modelos más grande\
            s usualmente obtienen mejores resultados, pero requieren mayor ti\
            empo de carga.
        :param dict_lemmas: (dict o str) Diccionario (o *string* con ubicació\
            n del archivo JSON que lo contiene) que permite modificar y agreg\
            ar lemas. Las llaves del diccionario son las palabras completas y\
             los valores del diccionario son los lemas escogidos para cada pa\
            labra.
        :param maxima_longitud: (int) Valor por defecto: None. Parámetro opci\
            onal que permite establecer la máxima longitud (número de caracte\
            res) que acepta el lematizador en un texto de entrada. Si este va\
            lor se deja en None, se utilizará la máxima longitud que trae Spa\
            cy por defecto (1 millón de caracteres).
        :param tokenizador: Valor por defecto: None. Objeto encargado de la d\
            etokenización de textos después de lematizar. Si el valor es \
            'None', se cargará por defecto una instancia de la clase \
            *TokenizadorEspacios*.
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

        :param lenguaje: (str) Define el lenguaje del texto a ser tratado. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, dim_modelo, maxima_longitud):
        """
        Inicia el lematizador con el tamaño del modelo de lematización basado\
         en en los tamaños de la librería Spacy. Los modelos más grandes usua\
        lmente obtienen mejores resultados, pero requieren mayor tiempo de ca\
        rga.

        :param dim_modelo: (str) {'lg', 'md', 'sm'} Valor por defecto: 'md'. \
            Se define el tamaño del modelo. 'lg' es grande (large), 'md' es m\
            ediano (medium) y 'sm' es pequeño (small).
        :param maxima_longitud: (int) Parámetro opcional que permite establec\
            er la máxima longitud (número de caracteres) que acepta el vector\
            izador en un texto de entrada. Si este valor se deja en None, se \
            utilizará la máxima longitud que trae Spacy por defecto (1 millón\
             de caracteres).
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
        Define lemas asociados a palabras escogidas por el usuario. Estos nue\
        vos lemas serán adicionados al diccionario de lemas del lematizador.

        :param dict_lemmas: (dict) Diccionario que permite modificar y agregar\
             lemas. Las llaves del diccionario son las palabras completas y l\
            os valores del diccionario son los lemas escogidos para cada pala\
            bra.
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
        Se lleva a cabo el proceso de lematización del texto, el cual puede \
        ser limpiado antes de la lematización.

        :param texto: (str) El texto que se desea lematizar.
        :param limpiar: (bool) {True, False} Valor por defecto: True. Especif\
            ica si se desea hacer una limpieza básica del texto antes de la \
            lematización.
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
        lenguaje,
        modelo_lemas="",
        dict_lemmas=None,
        archivo_salida="",
        tokenizador=None,
    ):
        """
        Constructor por defecto de la clase LematizadorStanza. Esta clase se \
        encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería Stanza.

        :param lenguaje: (str) Define el lenguaje del texto a ser tratado. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        :param modelo_lemas: (str) Valor por defecto: None. Especifica la ruta\
             de un modelo de lemas personalizado. En caso de ser vacío, se ut\
            iliza el modelo genérico de lemas de Stanza.
        :param dict_lemmas: (dict o str) Diccionario (o *string* con ubicación\
             del archivo JSON que lo contiene) que permite modificar y agregar\
             lemas. Las llaves del diccionario son las palabras completas y l\
            os valores del diccionario son los lemas escogidos para cada pala\
            bra.
        :param archivo_salida: (str) Valor por defecto: ''. Especifica la ruta\
             del archivo de salida del modelo de lemas modificado. En caso de \
            ser vacío, el resultado de la lematizacción se guarda en un archiv\
            o temporal que eventualmente será borrado.
        :param tokenizador: Valor por defecto: None. Objeto encargado de la d\
            etokenización de textos después de lematizar. Si el valor es \
            'None', se cargará por defecto una instancia de la clase \
            *TokenizadorEspacios*.
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

        :param lenguaje: (str) Define el lenguaje del texto a ser tratado. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, modelo_lemas):
        """
        Inicia el lematizador de Stanza y permite ingresar la ruta de un mode\
        lo de lematización personalizado. En caso de no especificar la ruta \
        se utilizará el modelo que trae Stanza por defecto para el lenguaje \
        seleccionado.

        :param modelo_lemas: (str) Valor por defecto: None. Especifica la ruta\
             de un modelo de lemas personalizado. En caso de ser vacío, se uti\
            liza el modelo que trae Stanza por defecto para el lenguaje selecc\
            ionado.
        """
        from utils.stanza_funcs import stanza_pipeline

        self.lematizador = None
        if self.lenguaje is not None:
            self.lematizador = stanza_pipeline(
                self.lenguaje, modelo_lemas=modelo_lemas
            )

    def modificar_lemmas(
        self, dict_lemmas, archivo_entrada="", archivo_salida="", gpu=False
    ):
        """
        Permite modificar o añadir nuevos lemas al modelo original de lematiz\
        ación. Adicionalmente, permite ingresar un modelo personalizado desde \
        una ruta específica.

        :param dict_lemmas: (dict) Diccionario que permite modificar y agregar\
             lemas. Las llaves del diccionario son las palabras completas \
            y el valor el lema escogido para cada palabra.
        :param archivo_entrada: (str) Valor por defecto: ''. En caso de ser va\
            cío, se escoge un modelo de lematización genérico. De lo contrario\
            , se especifica la ruta del modelo de lematización personalizado a\
             ser utilizado.
        :param archivo_salida: (str) Valor por defecto: ''. Especifica la ruta\
             del archivo de salida del modelo de lemas modificado. En caso de \
            ser vacío, el modelo modificado de lematizacción se guarda en un \
            archivo temporal que eventualmente será borrado.
        :param gpu: (bool) {True, False} Valor por defecto: False. Se escoge \
            si correr el proceso de lematización con GPU (True) o CPU (False)
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
        Se lleva a cabo el proceso de lematización del texto, el cual puede \
        ser limpiado antes de la lematización.

        :param texto: (str) El texto que se desea lematizar.
        :param limpiar: (bool) {True, False} Valor por defecto: True. Específ\
            ica si se desea hacer una limpieza básica del texto antes de la \
            lematización.
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
    modelo_lemas="",
    archivo_salida="",
    maxima_longitud=None,
    tokenizador=None,
):
    """
    Función que retorna un texto lematizado por la librería Spacy o Stanza. \
    Permite escoger el idioma de lematización, si hacer limpieza del texto, \
    modificar los modelos de lematizaciones originales y guardar los modelos \
    modificados.

    :param texto: (str) Texto de entrada a ser lematizado.
    :param lenguaje: (str) Valor por defecto: 'es'. Define el lenguaje del \
        texto a ser tratado. Para mayor información, consultar la sección de \
        :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
    :param libreria: (str) {'spacy', 'stanza'} Valor por defecto: 'spacy'. \
        Se define la librería de Python de lematización para ser utilizada en \
        el texto. Las opciones son las librerías Spacy y Stanza.
    :param limpiar: (bool) {True, False} Valor por defecto: True. Especifica \
        si se desea hacer una limpieza básica del texto antes de la lematiza\
        ción.
    :param lematizador: Valor por defecto: None. Parámetro opcional. Objeto \
        de la clase LematizadorSpacy o LematizadorStanzapara aplicar lematiz\
        ación sobre el texto de entrada. Se puede utilizar para aplicar lema\
        tización a varios textos a la vez, sin necesidad de inicializar un \
        lematizador en cada ocasión. Esto puede representar ahorro en tiempos \
        al momento de aplicar la función.
    :param dict_lemmas: (dict) Diccionario que permite modificar y agregar \
        lemas. Las llaves del diccionario son las palabras completas y los \
        valores del diccionario son los lemas escogidos para cada palabra.
    :param dim_modelo: (str) {'lg', 'md', 'sm'} Valor por defecto: 'md'. \
        Se define el tamaño del modelo. 'lg' es grande (large), 'md' es medi\
        ano (medium) y 'sm' es pequeño (small). Aplica únicamente para el \
        lematizador Spacy.
    :param modelo_lemas: (str) Valor por defecto: None. Especifica la ruta \
        de un modelo de lemas personalizado. En caso de ser vacío, se utiliza \
        el modelo genérico de lemas de Stanza. Aplica únicamente para la \
        lematización con Stanza.
    :param archivo_salida: (str) Valor por defecto: ''. Especifica la ruta \
        del archivo de salida del modelo de lemas modificado. En caso de ser \
        vacío, el resultado de la lematizacción se guarda en un archivo \
        temporal que eventualmente será borrado. Aplica únicamente para la \
        lematización con Stanza.
    :param maxima_longitud: (int) Valor por defecto: None. Parámetro opcional \
        que permite establecer la máxima longitud (número de caracteres) que \
        acepta el LematizadorSpacy en un texto de entrada. Si este valor se \
        deja en None, se utilizará la máxima longitud que trae Spacy por defe\
        cto (1 millón de caracteres). Aplica únicamente para la lematización \
        con Spacy.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la detok\
        enización de textos después de lematizar. Si el valor es 'None', se ca\
        rgará por defecto una instancia de la clase *TokenizadorEspacios*.
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
