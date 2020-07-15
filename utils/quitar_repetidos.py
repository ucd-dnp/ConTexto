from collections import Counter
from difflib import SequenceMatcher

# Tomada de
# https://www.geeksforgeeks.org/sequencematcher-in-python-for-longest-common-substring/


def maximo_substring(str1, str2):
    # Inicializar objeto de SequenceMatcher con los dos textos
    seqMatch = SequenceMatcher(None, str1, str2)
    # Hallar el sub-string común de mayor longitud
    # la salida tendra la forma de Match(a=0, b=0, size=5)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
    # Si se encontró un substring en común, se devuelve
    if (match.size != 0):
        return str1[match.a: match.a + match.size]
    else:
        pass

def detectar_coincidencias(lista_textos):
    coincidencias = []
    for i in range(len(lista_textos)):
        for j in range(i + 1, len(lista_textos)):
            con = maximo_substring(lista_textos[i], lista_textos[j])
            coincidencias.append(con)
    contador = Counter(coincidencias)
    comunes = {x: contador[x]
               for x in contador if contador[x] >= len(lista_textos)*0.9}
    return [i for i in comunes if i is not None and len(i.split()) >= 3]


def quitar_repetidos(lista_textos):
    coincidencias = detectar_coincidencias(lista_textos)
    for con in coincidencias:
        lista_textos = [i.replace(con, '') for i in lista_textos]
    return lista_textos
