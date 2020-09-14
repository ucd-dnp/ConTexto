import re
from collections import Counter
from difflib import SequenceMatcher
from tokenizacion import TokenizadorNLTK
from ..limpieza import remover_acentos

def substrings_en_comun(str1, str2, longitud_min=10):
    """
    Encuentra los *substrings*, o cadena de caracteres internas, que tienen en común \
        dos textos de entrada y cumplen con una longitud mínima.

    :param str1: (str). Primer texto de insumo.
    :param str2: (str). Segundo texto de insumo.
    :param longitud_min: (int). Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los dos textos de entrada, para ser considerada.
    :return: (list). Lista de *substrings* o cadenas de caracteres en común que cumplan \
        con el requisito de longitud mínima. Si no hay ningúna cadena de caracteres que cumpla \
        esta condición, se devuelve una lista vacía. 
    """    
    # Inicializar objeto de SequenceMatcher con los dos textos
    seqMatch = SequenceMatcher(None, str1, str2)
    # Hallar el sub-string común de mayor longitud
    # Cada elemento tiene la forma de Match(a=0, b=0, size=5)
    coincidencias = seqMatch.get_matching_blocks()
    # Se filtran solo las coincidencias que cumplan la longitud mínima
    coincidencias = [i for i in coincidencias if i.size >= longitud_min]
    # Se devuelve la lista de strings con las coincidencias
    return [str1[i.a: i.a + i.size] for i in coincidencias]

def detectar_coincidencias(lista_textos, prop=0.5, n_min=2, longitud_min=10):
    """
    Detecta y devuelve *substrings*, o cadenas de caracteres, que se repiten a lo \
        largo de una lista de textos y que cumplan hasta tres condiciones, ajustadas \
        por el usuario:

        * Que aparezcan en por lo menos una proporción determinada de todos los textos.
        * Que tengan por lo menos un número determinado de palabras.
        * Que tengan un número de caracteres mayor o igual a una longitud mínima establecida.

    :param lista_textos: (list). Lista de textos sobre los cuales se desea buscar coincidencias.
    :param prop: (float). Valor por defecto: 0.5. Número entre 0 y 1 que determina la proporción \
        mínima de la lista de textos en los que debe estar presente una cadena de caracteres para \
        ser considerada. Por ejemplo, si prop=0.8, un *substring* debe estar en por lo menos el 80% \
        de los textos de lista_textos, para ser devuelto.
    :param n_min: (int). Valor por defecto: 2. Número mínimo de palabras que debe tener una \
        coincidencia entre los textos de entrada, para ser considerada.
    :param longitud_min: (int). Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los textos de entrada, para ser considerada.        
    :return: (list). Lista de coincidencias encontradas entre los textos de entrada, que cumplan \
        con las condiciones con los valores establecidos por el usuario. Si no hay ningúna cadena \
        de caracteres que cumpla estas condiciones, se devuelve una lista vacía. 
    """        
    # Lista general de coincidencias entre los textos (que cumplan con longitud_min)
    coincidencias = []
    for i in range(len(lista_textos)):
        for j in range(i+1, len(lista_textos)):
            con = substrings_en_comun(lista_textos[i], lista_textos[j], longitud_min)
            coincidencias += con
    # Cantidad de veces que aparece cada coincidencia
    contador = Counter(coincidencias)
    # Se filtran las coincidencias que aparezcan en una proporción de los textos menor a prop
    comunes = {x: contador[x]
               for x in contador if contador[x] >= len(lista_textos) * prop}
    # Se devuelven las coincidencias que tengan igual o más palabras que n_min
    return [i for i in comunes if i is not None and len(i.split()) >= n_min]

def quitar_coincidenias(lista_textos, prop=0.5, n_min=2, longitud_min=10):
    """
    Detecta y remueve *substrings*, o cadenas de caracteres, que se repiten a lo \
        largo de una lista de textos y que cumplan hasta tres condiciones, ajustadas \
        por el usuario:

        * Que aparezcan en por lo menos una proporción determinada de todos los textos.
        * Que tengan por lo menos un número determinado de palabras.
        * Que tengan un número de caracteres mayor o igual a una longitud mínima establecida.
        
        Cada coincidencia encontrada entre la lista de textos es reemplazada de los textos de \
        entrada por un espacio en blanco.
    :param lista_textos: (list). Lista de textos sobre los cuales se desea buscar coincidencias.
    :param prop: (float). Valor por defecto: 0.5. Número entre 0 y 1 que determina la proporción \
        mínima de la lista de textos en los que debe estar presente una cadena de caracteres para \
        ser considerada. Por ejemplo, si prop=0.8, un *substring* debe estar en por lo menos el 80% \
        de los textos de lista_textos, para ser devuelto.
    :param n_min: (int). Valor por defecto: 2. Número mínimo de palabras que debe tener una \
        coincidencia entre los textos de entrada, para ser considerada.
    :param longitud_min: (int). Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los textos de entrada, para ser considerada.        
    :return: (list). Lista de textos de entrada, luego de remover todas las coincidencias \
        encontradas que cumplan con las condiciones con los valores establecidos por el usuario. 
    """     
    coincidencias = detectar_coincidencias(lista_textos, prop, n_min, longitud_min)
    for con in coincidencias:
        lista_textos = [i.replace(con, ' ') for i in lista_textos]
    return lista_textos

# Establece los criterios (de repetidos y consecutivos) 
# dependiendo de la longitud de la palabra de entrada.
dict_condiciones = {
    1: 0,
    2: 2,
    3: 2,
    4: 3
}

## Funciones basadas en expresiones regulares
def caracteres_repetidos(palabra, n, limpiar_palabra=True):
    """
    Determina si en una palabra de entrada se repiten caracteres (letras o números) de forma \
        seguida por lo menos un número de veces determinado por el usuario. Por ejemplo, si \
        n=3 y palabra="animaaal", la función arrojara positivo, porque el carácter "a" aparece \
        3 veces de forma seguida.

    :param palabra: (str). Palabra que se quiere analizar.
    :param n: (int). Número mínimo de veces seguidas que debe aparecer un carácter para \
        que la función arroje positivo.
    :param limpiar_palabra: (bool). Valor por defecto: True. Argumento opcional que permite pasar a minúsculas \
        y quitar acentos (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se \
        deja como False, las letras con acentos no serán contabilizadas en la búsqueda de caracteres repetidos, y \
        pueden haber inconsistencias entre letras en mayúscula y minúscula. Por ejemplo, las palabras "animaáal" o \
        "animaAal" no contabilizarán caracteres repetidos seguidos.         
    :return: (bool). Devuelve True si se cumple la condición de caracteres consecutivos repetidos, \
        y False en caso contrario. 
    """
    if limpiar_palabra:
        palabra = remover_acentos(palabra).lower()      
    cond_repetido = "([a-zA-Z0-9])" + "\\1" * (n - 1)
    return bool(re.search(cond_repetido, palabra))

def caracteres_consecutivos(palabra, n, limpiar_palabra=True):
    """
    Determina si en una palabra de entrada hay caracteres (letras o números) consecutivos, uno junto al \
        otro, por lo menos un número de veces determinado por el usuario. Por ejemplo, si n=4 y palabra=\
        "1234555", la función va a arrojar positivo, porque hay cinco caracteres consecutivos \
        (del 1 al 5) que aparecen uno junto al otro.

    :param palabra: (str). Palabra que se quiere analizar.
    :param n: (int). Número mínimo de caracteres consecutivos que deben aparecer juntos en la palabra \
        que la función arroje positivo.
    :param limpiar_palabra: (bool). Valor por defecto: True. Argumento opcional que permite pasar a minúsculas \
        y quitar acentos (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se \
        deja como False, las letras con acentos no serán contabilizadas en la búsqueda de caracteres consecutivos, y \
        pueden haber inconsistencias entre letras en mayúscula y minúscula. Por ejemplo, las palabras "àbcdë" o \
        "ABcde" solo contabilizarán 3 caracteres consecutivos seguidos. 
    :return: (bool). Devuelve True si se cumple la condición de caracteres consecutivos seguidos, \
        y False en caso contrario. 
    """        
    if limpiar_palabra:
        palabra = remover_acentos(palabra).lower()       
    cond_consecutivo = f"(?:(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){{{n-1},}}\d|(?:a(?=b)|b(?=c)|c(?=d)|d(?=e)|e(?=f)|f(?=g)|g(?=h)|h(?=i)|i(?=j)|j(?=k)|k(?=l)|l(?=m)|m(?=n)|n(?=o)|o(?=p)|p(?=q)|q(?=r)|r(?=s)|s(?=t)|t(?=u)|u(?=v)|v(?=w)|w(?=x)|x(?=y)|y(?=z)){{{n-1},}})"
    return bool(re.search(cond_consecutivo, palabra))

def consonantes_consecutivas(palabra, n, incluir_y=True, limpiar_palabra=True):
    """
    Determina si en una palabra de entrada hay consonantes (letras distintas a vocales) seguidas, una \
        junto a la otra, por lo menos un número de veces determinado por el usuario. Por ejemplo, si n=4 \
        y palabra="Abstracto", la función va a arrojar positivo, porque hay cuatro consonantes seguidas \
        ("bstr") en la palabra.

    :param palabra: (str). Palabra que se quiere analizar.
    :param n: (int). Número mínimo de consonantes que deben aparecer seguidas en la palabra \
        que la función arroje positivo.
    :param incluir_y: (bool). Valor por defecto: True. Argumento opcional para determinar si la letra. \
        "Y" debe ser considerada como vocal. Si incluir_y=False, la letra "Y" será considerada consonante.
    :param limpiar_palabra: (bool). Valor por defecto: True. Argumento opcional que permite quitar acentos \
        (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se deja como False, \
        las consonantes con acentos como "ç" o "ñ" no serán contabilizadas en la búsqueda de consonantes seguidas.
    :return: (bool). Devuelve True si se cumple la condición de consonantes seguidas, y \
        False en caso contrario. 
    """         
    if limpiar_palabra:
        palabra = remover_acentos(palabra)
    # Decidir si se cuenta la "y" como vocal
    if incluir_y:
        cond_consonantes = f'(?:(?![aeiouy])[a-z]){{{n},}}'
    else:
        cond_consonantes = f'(?:(?![aeiou])[a-z]){{{n},}}'
    # Devolver condicion
    return bool(re.search(cond_consonantes, palabra.lower()))

# Función para quitar de un texto las palabras que cumplan los criterios de caracteres
# repetidos y/o consecutivos
def quitar_palabras_atipicas(texto, n_repetidas=None, n_consecutivas=None, n_consonantes=True, 
                            incluir_y=True, limpiar_palabras=True, tokenizador=None):
    """
    Para un texto de entrada, busca y elimina palabras que cumplan una o varias de las siguientes condiciones, \
        ajustadas por el usuario:

    * Si se repiten caracteres (letras o números) de forma seguida por lo menos un número de veces determinado.
    * Si hay caracteres (letras o números) consecutivos, uno junto al otro, por lo menos un número de veces determinado.
    * Si hay consonantes (letras distintas a vocales) seguidas, una junto a la otra, por lo menos un número de veces \
        determinado.

    Al final, devuelve el texto de entrada sin las palabras identificadas.
    :param texto: (str). Texto al que se desean quitar palabras potencialmente problemáticas.
    :param n_repetidas: (int). Valor por defecto: None. Número mínimo de veces seguidas que se debe repetir \
        un caracter en una palabra para que cumpla este criterio. Si n_repetidas=None, la función no identificará \
        palabras con caracteres repetidos. Si n_repetidas=0, el valor de n_repetidas se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param n_consecutivas: (int). Valor por defecto: None. Número mínimo de caracteres consecutivos que deben \
        aparecer juntos en una palabra para que cumpla este criterio. Si n_consecutivas=None, la función no identificará \
        palabras con caracteres consecutivos. Si n_consecutivas=0, el valor de n_consecutivas se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param n_consonantes: (int). Valor por defecto: None. Número mínimo de consonantes que deben aparecer \
        seguidas en una palabra que cumpla este criterio. Si n_consonantes=None, la función no identificará \
        palabras con consonantes seguidas. Si n_consonantes=0, el valor de n_consonantes se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param incluir_y: (bool). Valor por defecto: True. Argumento opcional para determinar si la letra. \
        "Y" debe ser considerada como vocal, al buscar palabras con consonantes seguidas. Si incluir_y=False, \
        la letra "Y" será considerada consonante.
    :param limpiar_palabras: (bool). Valor por defecto: True. Argumento opcional que permite quitar acentos \
        (tildes, diéresis, virgulilla) y pasar a minúsculas las palabras del texto antes de revisar las \
        condiciones definidas por el usuario.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se cargará por defecto una instancia de la clase *TokenizadorNLTK*.
    :return: (str). Devuelve el texto de entrada sin las palabras que hayan sido identificadas de acuerdo a los \
        criterios especificados por el usuario. 
    """                   
    if tokenizador is None:
        tokenizador = TokenizadorNLTK()
    # Guardar tokens del texto original para devolver las palabras originales al final
    palabras_orig = tokenizador.tokenizar(texto)
    # Si se eligió limpiar el texto, se quitan acentos y se pasa todo a minúsculas
    if limpiar_palabras:
        texto = remover_acentos(texto).lower() 
    # Se parte el texto en palabras y se inicializa la lista de salida
    palabras = tokenizador.tokenizar(texto)    
    salida = []
    for i, p in enumerate(palabras):
        # Longitud de la palabra
        l = len(p)
        # Valor por reglas "duras", por si se necesita
        n = dict_condiciones[l] if l in dict_condiciones else 4
        # Ajustar valores mínimos, si aplica
        n_repetidas = n if n_repetidas==0 else n_repetidas 
        n_consecutivas = n if n_consecutivas==0 else n_consecutivas
        n_consonantes = n if n_consonantes==0 else n_consonantes
        # Se inicializan las dos condiciones, y si está indicado en los
        # parámetros, se calculan
        cond1 = cond2 = cond3 = False
        if n_repetidas is not None:
            cond1 = caracteres_repetidos(p, n_repetidas, False)
        if n_consecutivas is not None:
            cond2 = caracteres_consecutivos(p, n_consecutivas, False)
        if n_consonantes is not None:
            cond3 = consonantes_consecutivas(p, n_consonantes, incluir_y, False)
        # La palabra solo se incluye en la salida si no cumple ninguna condición
        if not any([cond1, cond2, cond3]):
            salida.append(palabras_orig[i])
    # Se pasa a texto la lista de salida, y se retorna
    return tokenizador.destokenizar(salida)
