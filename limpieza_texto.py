import re
import unicodedata

####### Definición de funciones para limpiar el texto  #########

# Quita palabras de 2 letras o menos
def remove_shortW(words):
    return [word for word in words if len(word) > 2]

# Quita acentos (tildes y 'ñ'), reemplazándolos por su versión sin acento
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

# Quita ciertas palabras previamente indicadas de la lista de palabras
def remove_sw(words,sw_list):
    return [word for word in words if word not in sw_list]

# Limpieza básica del texto
def basic_clean(text):
# Texto a minúsculas
    text = text.lower()
# Pone un espacio antes y después de cada signo de puntuación
    text = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", text)
# Quita caracteres especiales de las palabras. Solo deja pasar letras y espacio
    text = re.sub(r"[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]","", text)
# Reemplaza espacios múltiples por un solo espacio
    text = re.sub(r" +"," ", text)
# Quitar espacios, tabs y enters en los extremos del texto
    text = text.strip(' \t\n\r')
    
    return text

# Limpieza básica + remover palabras de menos de 3 caracteres y stopwords
def clean_text(text,sw_list = []):
# Limpieza básica del texto
    text = basic_clean(text)
# Vuelve el texto en una lista de palabras
    lista = text.split()
# Quita palabras cortas y palabras pertenecientes a una lista específica
    lista = remove_shortW(lista)
    lista = remove_sw(lista,sw_list)
    text = ' '.join(lista)
    return text



def remove_shortW(words):
    return [word for word in words if len(word) > 2]

# Quita ciertas palabras previamente indicadas de la lista de palabras
def remove_sw(words,sw_list):
    return [word for word in words if word not in sw_list]

def basic_clean(text):
# Texto a minúsculas
    text = text.lower()
# Pone un espacio antes y después de cada signo de puntuación
    text = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", text)
# Quita caracteres especiales de las palabras. Solo deja pasar letras y espacio
    text = re.sub(r"[^a-zA-ZñÑáéíóúÁÉÍÓÚ ]","", text)
# Reemplaza espacios múltiples por un solo espacio
    text = re.sub(r" +"," ", text)
# Quitar espacios, tabs y enters en los extremos del texto
    text = text.strip(' \t\n\r')
    
    return text

def clean_text(text,sw_list = []):
# Limpieza básica del texto
    text = basic_clean(text)
# Vuelve el texto en una lista de palabras
    lista = text.split()
# Quita palabras cortas y palabras pertenecientes a una lista específica
    lista = remove_shortW(lista)
    lista = remove_sw(lista,sw_list)
    
    text = ' '.join(lista)
    return text

#%% Manipulación de texto

# Función para quitar frases repetidas separadas por '|'.
def quitar_repetidos(text):
    lista = text.split('|')
    lista = pd.unique(lista)
    return ' '.join(lista)

# Función que tiene un texto de entrada y lo devuelve lematizado

# tagger = treetaggerwrapper.TreeTagger(TAGLANG='es')

# def lemmatize_text(text):
#     words_lst = text.split()
#     a = treetaggerwrapper.make_tags(tagger.tag_text(words_lst))
#     words_lst = [item[2] for item in a]
#     return ' '.join(words_lst)