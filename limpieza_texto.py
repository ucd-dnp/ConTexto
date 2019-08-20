import itertools
import re
import unicodedata

####### Definición de funciones para limpiar el texto  #########

# Quita acentos (tildes y 'ñ'), reemplazándolos por su versión sin acento
def remover_acentos(texto):
    try:
        texto = unicode(texto, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    texto = unicodedata.normalize('NFD', texto)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(texto)

# Quita ciertas palabras y expresiones previamente indicadas
def remover_stopwords(texto, lista_palabras=[], lista_expresiones=[], ubicacion_archivo=None, separador_espacio='__'):
    # Si se pasa como argumento la ubicación de un archivo plano que contiene la lista de palabras y expresiones
    # no deseadas separadas por comas, espacios o por enters.
    if ubicacion_archivo:
        lista_palabras, lista_expresiones = cargar_stopwords(ubicacion_archivo,separador_espacio)
    # Dejar solo las palabras que no aparecen en la lista de palabras no deseadas
    texto = ' '.join([palabra for palabra in texto.split() if palabra not in set(lista_palabras)])
    # Quitar las expresiones no deseadas
    for expresion in lista_expresiones:
        texto = texto.replace(expresion,'')
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +"," ", texto)
    return texto

# Quita palabras de menos de n caracteres
def remover_palabras_cortas(texto, n_min):
    palabras =  texto.split(' ')
    return ' '.join([palabra for palabra in palabras if len(palabra) >= n_min])

# Limpieza básica del texto
def limpieza_basica(texto, quitar_numeros=True):
    # Texto a minúsculas
    texto = texto.lower()
    # Pone un espacio antes y después de cada signo de puntuación
    texto = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", texto)
    # Quita caracteres especiales del texto.
    if quitar_numeros:
        texto = re.sub(r"[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]"," ", texto)
    else:
        texto = re.sub(r"[^a-zA-ZñÑáéíóúÁÉÍÓÚ0-9 ]"," ", texto)
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +"," ", texto)
    # Quitar espacios, tabs y enters en los extremos del texto
    texto = texto.strip(' \t\n\r')
    return texto

# Limpieza básica + remover palabras de menos de n caracteres y stopwords
def limpieza_texto(texto, lista_palabras=[], lista_expresiones=[], ubicacion_archivo=None, separador_espacio='__', n_min=0, quitar_acentos=False):
    # Se verifica si se desean quitar acentos/tildes
    if quitar_acentos:
        texto = remover_acentos(texto)
    # Limpieza básica del texto
    texto = basic_clean(texto)
    # Quita palabras cortas y palabras pertenecientes a una lista específica
    texto = remover_palabras_cortas(texto, n_min)
    texto = remover_stopwords(texto,lista_palabras,lista_expresiones,ubicacion_archivo,separador_espacio)
    return texto

# Función para quitar frases o palabras repetidas separadas por un caracter
# en particular.
def quitar_repetidos(texto, sep='|'):
    lista = texto.split(sep)
    lista = set(lista)
    return ' '.join(lista)

# Función para obtener las listas de palabras y expresiones que se desean
# eliminar de un texto, a partir de un archivo plano
def cargar_stopwords(file_path, separador_espacio='__'):
    lista_palabras = []
    lista_expresiones = []
    with open(file_path, encoding='utf') as fp:
        line = fp.readline()
        while line:
            linea = line.strip().split(',')
            linea = [i.split(' ') for i in linea]
            linea = list(itertools.chain.from_iterable(linea))
            for i in linea:
                if separador_espacio in i:
                    i = re.sub(separador_espacio,' ', i)
                    lista_expresiones.append(i)
                else:
                    lista_palabras.append(i)
            line = fp.readline()
    return lista_palabras, lista_expresiones
