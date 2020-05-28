import itertools
import re
import unicodedata
import pkg_resources
from lenguajes import dict_lenguajes

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
def remover_stopwords(texto, lista_palabras=[], lista_expresiones=[], ubicacion_archivo=None):
    # Si se pasa como argumento la ubicación de un archivo plano que contiene la lista de palabras y expresiones
    # no deseadas separadas por comas, espacios o por enters.
    if ubicacion_archivo:
        lista_palabras, lista_expresiones = cargar_stopwords(ubicacion_archivo)
    # Quitar las expresiones no deseadas
    for expresion in set(lista_expresiones):
        texto = texto.replace(expresion,' ')
    # Dejar solo las palabras que no aparecen en la lista de palabras no deseadas
    texto = ' '.join([palabra for palabra in texto.split() if palabra not in set(lista_palabras)])
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
def limpieza_texto(texto, lista_palabras=[], lista_expresiones=[], ubicacion_archivo=None, n_min=0, quitar_numeros=True, quitar_acentos=False):
    # Quitar palabras y expresiones no deseadas. Se hace al texto original porque la palabra/expresión
    # a remover puede tener tildes/mayúsculas/signos o estar compuesta por palabras cortas
    texto = remover_stopwords(texto,lista_palabras,lista_expresiones,ubicacion_archivo)
    # Se verifica si se desean quitar acentos/tildes
    if quitar_acentos:
        texto = remover_acentos(texto)
    # Limpieza básica del texto
    texto = limpieza_basica(texto, quitar_numeros)
    # Quita palabras cortas y palabras pertenecientes a una lista específica
    texto = remover_palabras_cortas(texto, n_min)
    # Se hace esto de nuevo, por si habían palabras que después de su limpieza quedan en 
    # la lista de palabras/expresiones no deseadas
    texto = remover_stopwords(texto,lista_palabras,lista_expresiones,ubicacion_archivo)    
    return texto

# Función para quitar frases o palabras repetidas separadas por un caracter
# en particular.
def quitar_repetidos(texto, sep='|'):
    lista = texto.split(sep)
    lista = set(lista)
    return ' '.join(lista)

# Función para quitar el espacio al inicio y al final de un string
def limpiar_extremos(texto):
    return texto[::-1].rstrip()[::-1].rstrip()

# Función para obtener las listas de palabras y expresiones que se desean
# eliminar de un texto, a partir de un archivo plano
def cargar_stopwords(file_path):
    lista_palabras = []
    lista_expresiones = []
    with open(file_path, encoding='utf8') as fp:
        line = fp.readline()
        while line:
            linea = line.strip().split(',')
            # linea = [i.split(' ') for i in linea]
            # linea = list(itertools.chain.from_iterable(linea))
            for i in linea:
                i = limpiar_extremos(i)
                if len(i.split(' ')) > 1:
                    lista_expresiones.append(i)
                else:
                    lista_palabras.append(i)
            line = fp.readline()
    return lista_palabras, lista_expresiones


# Función para cargar lista general predefinida de stopwords
def lista_stopwords(lenguaje='es'):
    lenguaje = dict_lenguajes[remover_acentos(lenguaje)]
    if lenguaje == 'spanish':
        try:
            ruta = pkg_resources.resource_filename(__name__, 'data/listas_stopwords/sw_es.txt')
            sw = cargar_stopwords(ruta)[0]
        except:
            from nltk.corpus import stopwords
            sw = stopwords.words(lenguaje)
        else:
            from nltk.corpus import stopwords
            sw = stopwords.words(lenguaje)
    return sw

# Función para cargar lista general de stopwords
def lista_nombres(tipo='todos'):
    if tipo == 'todos':
        ruta = pkg_resources.resource_filename(__name__, 'data/listas_stopwords/nombres.txt')
    elif tipo.lower() in ['m','masculino','hombre','hombres']:
        ruta = pkg_resources.resource_filename(__name__, 'data/listas_stopwords/nombres_hombres.txt')
    elif tipo.lower() in ['f','femenino','mujer','mujeres']:
        ruta = pkg_resources.resource_filename(__name__, 'data/listas_stopwords/nombres_mujeres.txt')
    else:
        return [], []
    return cargar_stopwords(ruta)

def lista_apellidos():
    ruta =  pkg_resources.resource_filename(__name__, 'data/listas_stopwords/apellidos.txt')
    return cargar_stopwords(ruta)

def lista_geo_colombia(tipo='todos'):
    ruta_mun =  pkg_resources.resource_filename(__name__, 'data/listas_stopwords/municipios_col.txt')
    ruta_dep =  pkg_resources.resource_filename(__name__, 'data/listas_stopwords/departamentos_col.txt')
    if tipo == 'todos':
        palabras = list(set(cargar_stopwords(ruta_mun)[0] + cargar_stopwords(ruta_dep)[0]))
        expresiones = list(set(cargar_stopwords(ruta_mun)[1] + cargar_stopwords(ruta_dep)[1]))
        return palabras, expresiones
    elif tipo.lower() in ['municipios', 'mun', 'm']:
        return cargar_stopwords(ruta_mun)
    elif tipo.lower() in ['departamentos', 'dep', 'd']:
        return cargar_stopwords(ruta_dep)
    else:
        return [], []
