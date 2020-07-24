from langid.langid import LanguageIdentifier, model
from googletrans import Translator
from limpieza_texto import remover_acentos


def detectar_lenguaje(texto, devolver_proba=False):
    identificador = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    if devolver_proba:
        return identificador.classify(texto)
    else:
        return identificador.classify(texto)[0]


def traducir_texto(texto, lenguaje_destino):
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

# Función para determinar el lenguaje a partir de una entrada


def definir_lenguaje(lenguaje, simplificado=True):
    leng = None
    lenguaje = lenguaje.lower()
    lenguaje = remover_acentos(lenguaje)
    if lenguaje in dict_lenguajes.keys():
        leng = dict_lenguajes[lenguaje]
        if simplificado:
            leng = dict_lenguajes_simplificado[leng]
    return leng
