from langid.langid import LanguageIdentifier, model
from googletrans import Translator
from limpieza import remover_acentos


def detectar_lenguaje(texto, devolver_proba=False):
    """ Identifica el idioma en el que está escrito el texto de entrada.

    :param texto: (str) Corresponde al texto que se desea analizar. 
    :param devolver_proba: (bool) {True, False}, valor por defecto: False. Indica si se retorna el porcentaje de confiabilidad del lenguaje identificado.
    :return: string del idioma identificado siguiendo el estandar `ISO 639-1 <https://es.wikipedia.org/wiki/ISO_639-1>`_. Si devolver_proba es True retorna una tupla.
    """
    identificador = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    if devolver_proba:
        return identificador.classify(texto)
    else:
        return identificador.classify(texto)[0]


def traducir_texto(texto, lenguaje_destino):
    """ Permite hacer traducciones a un texto de interés.

    :param texto: (str) Corresponde al texto que se desea traducir. 
    :param lenguaje_destino: (str) {'es', 'en', 'de', 'fr'}. Indica el idioma al que desea traducir el texto, soporta Español(es), Inglés(en), Alemán(de) y Francés(fr).
    :return: string del texto traducido.
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


def definir_lenguaje(lenguaje, simplificado=True):
    """ Función auxiliar - permite determinar el lenguaje a partir de una entrada.

    :param lenguaje: (str) Corresponde al nombre del lenguaje a definir.
    :param simplificado: (bool) {True, False}, valor por defecto: True. Indica si se utiliza el dictionario de dict_lenguajes o dict_lenguajes_simplificado.
    :return: string correspondiente al lenguaje identificado.
    """
    leng = None
    lenguaje = lenguaje.lower()
    lenguaje = remover_acentos(lenguaje)
    if lenguaje in dict_lenguajes.keys():
        leng = dict_lenguajes[lenguaje]
        if simplificado:
            leng = dict_lenguajes_simplificado[leng]
    return leng
