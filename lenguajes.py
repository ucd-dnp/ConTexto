from langid.langid import LanguageIdentifier, model
from googletrans import Translator

def detectar_lenguaje(texto, devolver_proba=False):
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    if devolver_proba:
        return identifier.classify(texto)
    else:
        return identifier.classify(texto)[0]

def traducir_texto(texto,lenguaje_destino):
    traductor = Translator()
    out = traductor.translate(texto, dest=lenguaje_destino)
    if type(texto) == str:
        return out.text
    else:
        return [i.text for i in out]

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