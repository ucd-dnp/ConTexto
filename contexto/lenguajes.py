from langid.langid import LanguageIdentifier, model
from googletrans import Translator
from limpieza import remover_acentos


def detectar_lenguaje(texto, devolver_proba=False):
    """ Identifica el lenguaje en el que está escrito el texto de entrada.   

    :param texto: (str) Corresponde al texto que se desea analizar. 
    :param devolver_proba: (bool) {True, False} Valor por defecto: False. \ 
        Indica si se retorna el porcentaje de confiabilidad del \ 
        lenguaje identificado.
    :return: (str) Texto del lenguaje identificado siguiendo el estandar \ 
        `ISO 639-1 <https://es.wikipedia.org/wiki/ISO_639-1>`_. \ 
        Si devolver_proba es True retorna una tupla.
    """
    identificador = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    if devolver_proba:
        return identificador.classify(texto)
    else:
        return identificador.classify(texto)[0]


def traducir_texto(texto, lenguaje_destino):
    """ Permite hacer traducciones a un texto de interés.

    .. note::
        Es importante tener en cuenta los siguientes aspectos al utilizar la función **traducir_texto**:

        * La función utiliza la librería googletrans, que hace uso de la API de Google Translate. Por lo tanto, se requiere tener una conexión a internet para su funcionamiento.        
        * El límite máximo de caracteres en un solo texto es de 15.000.
        * Debido a las limitaciones de la versión web del traductor de Google, el uso de la API no garantiza que la librería funcione correctamente en todo momento.
        * Si desea utilizar una API estable, se recomienda el uso de la `API de traducción oficial de Google <https://cloud.google.com/translate/docs>`_.
        * Si recibe un error HTTP 5xx, probablemente se deba a que Google ha bloqueado su dirección IP.
        * Para mayor información puede consultar la `documentación de la librería googletrans <https://py-googletrans.readthedocs.io/en/latest/>`_.

    :param texto: (str) Corresponde al texto que se desea traducir. 
    :param lenguaje_destino: (str)  Indica el lenguaje al que desea \ 
        traducir el texto. Para mayor información, consultar la \ 
        sección de :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.        
    :return: (str) Texto traducido.
    """
    traductor = Translator()
    # Adecuar el lenguaje de destino al formato de la API
    lenguaje_destino = dict_lenguajes[lenguaje_destino]
    lenguaje_destino = dict_lenguajes_simplificado[lenguaje_destino]
    salida = traductor.translate(texto, dest=lenguaje_destino)
    if isinstance(texto, str):
        return salida.text
    else:
        return [i.text for i in salida]


# Diccionario para distintas representaciones de idiomas
# Por ahora se acota a español, inglés, alemán y francés
dict_lenguajes = {
    'es': 'spanish',
    'espanol': 'spanish',
    'esp': 'spanish',
    'spanish': 'spanish',
    'sp': 'spanish',
    'spa': 'spanish',
    'en': 'english',
    'eng': 'english',
    'english': 'english',
    'ingles': 'english',
    'ing': 'english',
    'ge': 'german',
    'de': 'german',
    'deu': 'german',
    'german': 'german',
    'aleman': 'german',
    'al': 'german',
    'ale': 'german',
    'fr': 'french',
    'fra': 'french',
    'fre': 'french',
    'french': 'french',
    'frances': 'french',
}

# Diccionario para dejar la representación en dos letras de cada idioma
dict_lenguajes_simplificado = {
    'spanish': 'es',
    'english': 'en',
    'french': 'fr',
    'german': 'de'
}

# Diccionario para traducir el lenguaje a la forma aceptada por Tesseract
dict_tesseract = {
    'spanish': 'spa',
    'english': 'eng',
    'french': 'fra',
    'german': 'deu'
}


def definir_lenguaje(lenguaje, simplificado=True):
    """ Función auxiliar - permite determinar el lenguaje a partir de una entrada.

    :param lenguaje: (str) Corresponde al nombre del lenguaje a definir.
    :param simplificado: (bool) {True, False} Valor por defecto: True. \ 
        Indica si se utiliza el dictionario de dict_lenguajes o \ 
        dict_lenguajes_simplificado.
    :return: (str) Texto correspondiente al lenguaje identificado.
    """
    leng = None
    lenguaje = lenguaje.lower()
    lenguaje = remover_acentos(lenguaje)
    if lenguaje in dict_lenguajes.keys():
        leng = dict_lenguajes[lenguaje]
        if simplificado:
            leng = dict_lenguajes_simplificado[leng]
    return leng


def lenguaje_tesseract(lenguaje):
    """ Función auxiliar - Para un lenguaje de entrada, busca su equivalente en Tesseract.

    :param lenguaje: (str) Corresponde al nombre del lenguaje a definir.
    :return: (str) Texto correspondiente al lenguaje identificado, de acuerdo a lo aceptado por \
        Tesseract.
    """
    leng = None
    lenguaje = lenguaje.lower()
    lenguaje = remover_acentos(lenguaje)
    if lenguaje in dict_lenguajes.keys():
        leng = dict_lenguajes[lenguaje]
        leng = dict_tesseract[leng]
    return leng
