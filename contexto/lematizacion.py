import json
import spacy
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje

### Definir clases para el lematizador ###


class LematizadorSpacy():
    def __init__(self, lenguaje, dict_lemmas=None, dim_modelo='md'):
        """
        Constructor por defecto de la clase LematizadorSpacy. Esta clase se \
        encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería Spacy

        :param lenguaje: (string). {'es', 'en', 'fr', 'de'}  Se define el 
            lenguaje del texto a ser tratado. Los lenguajes posibles son español \
            ('es'), inglés ('en'), francés ('fr') y alemán ('de')
        :param dict_lemmas: (dict). Diccionario que permite modificar y \ 
            agregar lemas. Las llaves del diccionario son las palabras completas \
            y el valor el lema escogido para cada palabra
        :param dim_modelo: (string) {'lg', 'md', 'sm'}. Se define el tamaño \ 
            del modelo. 'lg' es grande (large), 'md' es mediano (medium) y 'sm' es \
            pequeño (small). Los modelos más grandes obtienen mejores predicciones \
            pero requieren mayor tiempo de carga
        :return: objeto del tipo de la clase LematizadorSpacy

        """

        # Definir lenguaje del lematizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar lematizador
        self.iniciar_lematizador(dim_modelo)
        # Si se introdujo un diccionario personalizado, se utiliza
        if isinstance(dict_lemmas, dict):
            self.modificar_lemmas(dict_lemmas)
        # Si es la ubicación del archivo, primero se carga
        elif isinstance(dict_lemmas, str):
            try:
                dict_lemmas = json.load(open(dict_lemmas))
                self.modificar_lemmas(dict_lemmas)
            except BaseException:
                print('No se pudo cargar el diccionario de lemas')

    def establecer_lenguaje(self, lenguaje):
        """ Define el lenguaje del texto a ser tratado por las funciones de \
            lematización

        :param lenguaje: (string). {'es', 'en', 'fr', 'de'}  Se define el 
            lenguaje del texto a ser tratado. Los lenguajes posibles son español \
            ('es'), inglés ('en'), francés ('fr') y alemán ('de')

        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, dim_modelo):
        """ Define el tamaño del modelo de lematización. Se basa en los tamaños \
            de la librería Spacy. Los modelos más grandes obtienen mejores predicciones \
            pero requieren mayor tiempo de carga

        :param dim_modelo: (string) {'lg', 'md', 'sm'}. Se define el tamaño \ 
            del modelo. 'lg' es grande (large), 'md' es mediano (medium) y 'sm' es \
            pequeño (small). 
        :return:
        """
        self.lematizador = None
        if self.lenguaje is not None:
            from utils.spacy_funcs import cargar_modelo
            self.lematizador = cargar_modelo(dim_modelo, self.lenguaje)

    def modificar_lemmas(self, dict_lemmas):
        """ Define lemas asociados a palabras escogidas por el usuario. Estos nuevos \
            lemas serán adicionados al diccionario de lemas que ya incluyen los \
            modelos de Spacy

        :param dict_lemmas: (dict). Diccionario que permite modificar y \ 
            agregar lemas. Las llaves del diccionario son las palabras completas \
            y el valor el lema escogido para cada palabra
        :return:
        """
        # Definir función auxiliar
        def cambiar_propiedades_lemma(doc):
            for token in doc:
                if(token.text in dict_lemmas):
                    token.lemma_ = dict_lemmas[token.text]
            return doc
        # Aplicar la función para modificar el lematizador
        if (self.lematizador is not None) and (self.lematizador != -1):
            self.lematizador.add_pipe(cambiar_propiedades_lemma, first=True)

    def lematizar(self, texto, limpiar=True):
        """ Se lleva a cabo el proceso de lematización del texto, el cual puede \
            ser limpiado antes de la lematización

        :param texto: (string). El texto que se desea lematizar
        :param limpiar: (bool) {True, False}. Valor por defecto: True. Especifica \
            si se desea hacer una limpieza básica del texto antes de la lematización
        :return:
        """
        if limpiar:
            texto = limpieza_basica(texto)
        return ' '.join([token.lemma_ for token in self.lematizador(texto)])

# Implementación alternativa, utilizando stanza


class LematizadorStanza():
    def __init__(
            self,
            lenguaje,
            modelo_lemas='',
            dict_lemmas=None,
            archivo_salida=''):

        """
        Constructor por defecto de la clase LematizadorStanza. Esta clase se \
        encarga de manejar todas las funciones asociadas a la lematización \
        del texto con la librería Stanza

        :param lenguaje: (string). {'es', 'en', 'fr', 'de'}  Se define el 
            lenguaje del texto a ser tratado. Los lenguajes posibles son español \
            ('es'), inglés ('en'), francés ('fr') y alemán ('de')
        :param modelo_lemas:
        :param dict_lemmas: (dict). Diccionario que permite modificar y \ 
            agregar lemas. Las llaves del diccionario son las palabras completas \
            y el valor el lema escogido para cada palabra
        :param archivo_salida:

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
                print('No se pudo cargar el diccionario de lemas')

    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje: (string). {'es', 'en', 'fr', 'de'}  Se define el 
            lenguaje del texto a ser tratado. Los lenguajes posibles son español \
            ('es'), inglés ('en'), francés ('fr') y alemán ('de')
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_lematizador(self, modelo_lemas):
        """

        :param modelo_lemas:
        :return:
        """
        from utils.stanza_funcs import stanza_pipeline
        self.lematizador = None
        if self.lenguaje is not None:
            self.lematizador = stanza_pipeline(
                self.lenguaje, modelo_lemas=modelo_lemas)

    def modificar_lemmas(
            self,
            dict_lemmas,
            archivo_entrada='',
            archivo_salida='',
            gpu=False):
        """

        :param dict_lemmas: (dict). Diccionario que permite modificar y \ 
            agregar lemas. Las llaves del diccionario son las palabras completas \
            y el valor el lema escogido para cada palabra
        :param archivo_entrada:
        :param archivo_salida:
        :param gpu:
        :return:
        """
        from utils.stanza_funcs import modificar_modelo
        self.lematizador = modificar_modelo(
            self.lematizador,
            'lemma',
            dict_lemmas,
            archivo_entrada,
            archivo_salida,
            gpu)

    def lematizar(self, texto, limpiar=True):
        """ Se lleva a cabo el proceso de lematización del texto, el cual puede \
            ser limpiado antes de la lematización
        :param texto: (string). El texto que se desea lematizar
        :param limpiar: (bool) {True, False}. Valor por defecto: True. Especifica \
            si se desea hacer una limpieza básica del texto antes de la lematización
        :return:
        """
        if limpiar:
            texto = limpieza_basica(texto)
        doc = self.lematizador(texto)
        # Extraer los lemas de cada palabra, de cada frase, y juntarlos
        return ' '.join([w.lemma for s in doc.sentences for w in s.words])


### Definir función que envuelva la funcionalidad básica de las clases ###

def lematizar_texto(
        texto,
        lenguaje='es',
        libreria='spacy',
        limpiar=True,
        lematizador=None,
        dict_lemmas=None,
        dim_modelo='md',
        modelo_lemas='',
        archivo_salida=''):
    """

    :param texto: (string). Texto de entrada a ser lematizado
    :param lenguaje: (string). {'es', 'en', 'fr', 'de'}  Se define el 
        lenguaje del texto a ser tratado. Los lenguajes posibles son español \
        ('es'), inglés ('en'), francés ('fr') y alemán ('de')
    :param libreria: (string). {'spacy', 'stanza'}. Valor por defecto: 'spacy' \
        Se define la librería de Python de lematización para ser utilziada en '
        el texto. Las opciones son las librerías Spacy y Stanza
    :param limpiar: (bool) {True, False}. Valor por defecto: True. Especifica \
        si se desea hacer una limpieza básica del texto antes de la lematización
    :param lematizador: 
    :param dict_lemmas: (dict). Diccionario que permite modificar y \ 
        agregar lemas. Las llaves del diccionario son las palabras completas \
        y el valor el lema escogido para cada palabra
    :param dim_modelo: (string) {'lg', 'md', 'sm'}. Se define el tamaño \ 
        del modelo. 'lg' es grande (large), 'md' es mediano (medium) y 'sm' es \
        pequeño (small). Aplica para el lematizador Spacy
    :param modelo_lemas:
    :param archivo_salida:
    :return:
    """
    # Si no se provee un lematizador, este debe ser inicializado
    if lematizador is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        if libreria.lower() == 'spacy':
            lematizador = LematizadorSpacy(lenguaje, dict_lemmas, dim_modelo)
        elif libreria.lower() == 'stanza':
            lematizador = LematizadorStanza(
                lenguaje, modelo_lemas, dict_lemmas, archivo_salida)
        else:
            print(
                'Por favor escoja una librería válida para el lematizador (Spacy o Stanza)')
            return None
    # Si el lenguaje no se reconoce, se envía mensaje
    if lematizador.lematizador is None:
        print('Lenguaje no válido.')
        return None
    # Devolver la lematización del texto
    return lematizador.lematizar(texto, limpiar)
