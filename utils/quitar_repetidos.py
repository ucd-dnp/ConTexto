from collections import Counter
from difflib import SequenceMatcher 

# Tomada de https://www.geeksforgeeks.org/sequencematcher-in-python-for-longest-common-substring/
def longestSubstring(str1,str2): 
     # Inicializar objeto de SequenceMatcher con los dos textos 
     seqMatch = SequenceMatcher(None,str1,str2) 
     # Hallar el sub-string común de mayor longitud 
     # la salida tendra la forma de Match(a=0, b=0, size=5) 
     match = seqMatch.find_longest_match(0, len(str1), 0, len(str2)) 
     # Si se encontró un substring en común, se devuelve 
     if (match.size!=0): 
          return str1[match.a: match.a + match.size] 
     else: 
          pass

def detectar_coincidencias(text_list):
    coincidencias = []
    for i in range(len(text_list)):
        for j in range(i+1,len(text_list)):
            con = longestSubstring(text_list[i], text_list[j])
            coincidencias.append(con)
    contador = Counter(coincidencias)
    comunes = {x : contador[x] for x in contador if contador[x] >= len(text_list)}
    return [i for i in list(comunes.keys()) if len(i.split()) >= 3]

def quitar_repetidos(text_list):
    coincidencias = detectar_coincidencias(text_list)
    for con in coincidencias:
        text_list = [i.replace(con,'') for i in text_list]
    return text_list