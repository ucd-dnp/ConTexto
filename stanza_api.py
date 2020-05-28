import stanza
from lenguajes import detectar_lenguaje
from lenguajes import dict_lenguajes, dict_lenguajes_simplificado
from limpieza_texto import remover_acentos

idioma = 'español'
idioma = remover_acentos(idioma)
idioma = dict_lenguajes_simplificado[dict_lenguajes[idioma]]

nlp = stanza.Pipeline('en')

stanza.download('en')