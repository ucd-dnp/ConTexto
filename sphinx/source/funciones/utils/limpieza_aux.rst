Limpieza aux
============

Las funciones de esta sección se encargan de encontrar caracteres con ciertas características dentro de los textos, como números o letras repetidos, números o letras consecutivos y coincidencias de textos. También permite la eliminación de caracteres no deseados por el usuario, según varios criterios de selección.


.. function:: substrings_en_comun( str1, str2, longitud_min=10 )
    
    Encuentra los *substrings*, o cadena de caracteres internas, que tienen en común \
    dos textos de entrada y cumplen con una longitud mínima.

    :param str1: (str) Primer texto de insumo.
    :param str2: (str) Segundo texto de insumo.
    :param longitud_min: (int) Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los dos textos de entrada, para ser considerada.
    :return: (list) Lista de *substrings* o cadenas de caracteres en común que cumplan \
        con el requisito de longitud mínima. Si no hay ningúna cadena de caracteres que cumpla \
        esta condición, se devuelve una lista vacía. 


.. function:: detectar_coincidencias(lista_textos, prop=0.5, n_min=2, longitud_min=10)

    Detecta y devuelve *substrings*, o cadenas de caracteres, que se repiten a lo \
    largo de una lista de textos y que cumplan hasta tres condiciones, ajustadas \
    por el usuario:

        * Que aparezcan en por lo menos una proporción determinada de todos los textos.
        * Que tengan por lo menos un número determinado de palabras.
        * Que tengan un número de caracteres mayor o igual a una longitud mínima establecida.

    :param lista_textos: (list) Lista de textos sobre los cuales se desea buscar coincidencias.
    :param prop: (float) Valor por defecto: 0.5. Número entre 0 y 1 que determina la proporción \
        mínima de la lista de textos en los que debe estar presente una cadena de caracteres para \
        ser considerada. Por ejemplo, si prop=0.8, un *substring* debe estar en por lo menos el 80% \
        de los textos de lista_textos, para ser devuelto.
    :param n_min: (int) Valor por defecto: 2. Número mínimo de palabras que debe tener una \
        coincidencia entre los textos de entrada, para ser considerada.
    :param longitud_min: (int) Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los textos de entrada, para ser considerada.        
    :return: (list) Lista de coincidencias encontradas entre los textos de entrada, que cumplan \
        con las condiciones con los valores establecidos por el usuario. Si no hay ningúna cadena \
        de caracteres que cumpla estas condiciones, se devuelve una lista vacía. 


.. function:: quitar_coincidenias(lista_textos, prop=0.5, n_min=2, longitud_min=10)
    
    Detecta y remueve *substrings*, o cadenas de caracteres, que se repiten a lo \
    largo de una lista de textos y que cumplan hasta tres condiciones, ajustadas \
    por el usuario:

        * Que aparezcan en por lo menos una proporción determinada de todos los textos.
        * Que tengan por lo menos un número determinado de palabras.
        * Que tengan un número de caracteres mayor o igual a una longitud mínima establecida.

        Cada coincidencia encontrada entre la lista de textos es reemplazada de los textos de \
        entrada por un espacio en blanco.

    :param lista_textos: (list) Lista de textos sobre los cuales se desea buscar coincidencias.
    :param prop: (float) Valor por defecto: 0.5. Número entre 0 y 1 que determina la proporción \
        mínima de la lista de textos en los que debe estar presente una cadena de caracteres para \
        ser considerada. Por ejemplo, si prop=0.8, un *substring* debe estar en por lo menos el 80% \
        de los textos de lista_textos, para ser devuelto.
    :param n_min: (int) Valor por defecto: 2. Número mínimo de palabras que debe tener una \
        coincidencia entre los textos de entrada, para ser considerada.
    :param longitud_min: (int) Cantidad mínima de caracteres que debe tener una coincidencia \
        entre los textos de entrada, para ser considerada.        
    :return: (list) Lista de textos de entrada, luego de remover todas las coincidencias \
        encontradas que cumplan con las condiciones con los valores establecidos por el usuario. 


.. function:: caracteres_repetidos(palabra, n, limpiar_palabra=True)
    
    Determina si en una palabra de entrada se repiten caracteres (letras o números) de forma \
    seguida por lo menos un número de veces determinado por el usuario. Por ejemplo, si \
    n=3 y palabra='animaaal', la función arrojara positivo, porque el carácter 'a' aparece \
    3 veces de forma seguida.

    :param palabra: (str) Palabra que se quiere analizar.
    :param n: (int) Número mínimo de veces seguidas que debe aparecer un carácter para \
        que la función arroje positivo.
    :param limpiar_palabra: (bool) {True, False} Valor por defecto: True. Argumento opcional que permite pasar a minúsculas \
        y quitar acentos (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se \
        deja como False, las letras con acentos no serán contabilizadas en la búsqueda de caracteres repetidos, y \
        pueden haber inconsistencias entre letras en mayúscula y minúscula. Por ejemplo, las palabras "animaáal" o \
        "animaAal" no contabilizarán caracteres repetidos seguidos.         
    :return: (bool) Devuelve True si se cumple la condición de caracteres consecutivos repetidos, \
        y False en caso contrario. 


.. function:: caracteres_consecutivos(palabra, n, limpiar_palabra=True)

    Determina si en una palabra de entrada hay caracteres (letras o números) consecutivos, uno junto al \
    otro, por lo menos un número de veces determinado por el usuario. Por ejemplo, si n=4 y palabra=\
    '1234555', la función va a arrojar positivo, porque hay cinco caracteres consecutivos \
    (del 1 al 5) que aparecen uno junto al otro.

    :param palabra: (str) Palabra que se quiere analizar.
    :param n: (int) Número mínimo de caracteres consecutivos que deben aparecer juntos en la palabra \
        que la función arroje positivo.
    :param limpiar_palabra: (bool) {True, False} Valor por defecto: True. Permite pasar a minúsculas \
        y quitar acentos (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se \
        deja como False, las letras con acentos no serán contabilizadas en la búsqueda de caracteres consecutivos, y \
        pueden haber inconsistencias entre letras en mayúscula y minúscula. Por ejemplo, las palabras 'àbcdë' o \
        'ABcde' solo contabilizarán 3 caracteres consecutivos seguidos. 
    :return: (bool) Devuelve True si se cumple la condición de caracteres consecutivos seguidos, \
        y False en caso contrario. 


.. function:: consonantes_consecutivas(palabra, n, incluir_y=True, limpiar_palabra=True)
    
    Determina si en una palabra de entrada hay consonantes (letras distintas a vocales) seguidas, una \
    junto a la otra, por lo menos un número de veces determinado por el usuario. Por ejemplo, si n=4 \
    y palabra='Abstracto', la función va a arrojar positivo, porque hay cuatro consonantes seguidas \
    ('bstr') en la palabra.

    :param palabra: (str) Palabra que se quiere analizar.
    :param n: (int) Número mínimo de consonantes que deben aparecer seguidas en la palabra \
        que la función arroje positivo.
    :param incluir_y: (bool) {True, False} Valor por defecto: True. Argumento opcional para determinar si la letra. \
        'Y' debe ser considerada como vocal. Si incluir_y=False, la letra 'Y' será considerada consonante.
    :param limpiar_palabra: (bool) {True, False} Valor por defecto: True. Argumento opcional que permite quitar acentos \
        (tildes, diéresis, virgulilla) a la palabra antes de analizarla. Si este parámetro se deja como False, \
        las consonantes con acentos como 'ç' o 'ñ' no serán contabilizadas en la búsqueda de consonantes seguidas.
    :return: (bool) Devuelve True si se cumple la condición de consonantes seguidas, y \
        False en caso contrario. 


.. function:: quitar_palabras_atipicas(texto, n_repetidas=None, n_consecutivas=None, n_consonantes=True, \
                             incluir_y=True, limpiar_palabras=True, tokenizador=None)

    Para un texto de entrada, busca y elimina palabras que cumplan una o varias de las siguientes condiciones, \
    ajustadas por el usuario:

        * Si se repiten caracteres (letras o números) de forma seguida por lo menos un número de veces determinado.
        * Si hay caracteres (letras o números) consecutivos, uno junto al otro, por lo menos un número de veces determinado.
        * Si hay consonantes (letras distintas a vocales) seguidas, una junto a la otra, por lo menos un número de veces determinado.

    Al final, devuelve el texto de entrada sin las palabras identificadas.

    :param texto: (str) Texto al que se desean quitar palabras potencialmente problemáticas.
    :param n_repetidas: (int) Valor por defecto: None. Número mínimo de veces seguidas que se debe repetir \
        un caracter en una palabra para que cumpla este criterio. Si n_repetidas=None, la función no identificará \
        palabras con caracteres repetidos. Si n_repetidas=0, el valor de n_repetidas se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param n_consecutivas: (int) Valor por defecto: None. Número mínimo de caracteres consecutivos que deben \
        aparecer juntos en una palabra para que cumpla este criterio. Si n_consecutivas=None, la función no identificará \
        palabras con caracteres consecutivos. Si n_consecutivas=0, el valor de n_consecutivas se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param n_consonantes: (int) Valor por defecto: None. Número mínimo de consonantes que deben aparecer \
        seguidas en una palabra que cumpla este criterio. Si n_consonantes=None, la función no identificará \
        palabras con consonantes seguidas. Si n_consonantes=0, el valor de n_consonantes se definirá en función \
        de la longitud de cada palabra, de acuerdo a unas reglas preestablecidas.
    :param incluir_y: (bool) {True, False} Valor por defecto: True. Argumento opcional para determinar si la letra. \
        "Y" debe ser considerada como vocal, al buscar palabras con consonantes seguidas. Si incluir_y=False, \
        la letra "Y" será considerada consonante.
    :param limpiar_palabras: (bool) {True, False} Valor por defecto: True. Argumento opcional que permite quitar acentos \
        (tildes, diéresis, virgulilla) y pasar a minúsculas las palabras del texto antes de revisar las \
        condiciones definidas por el usuario.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se cargará por defecto una instancia de la clase *TokenizadorNLTK*.
    :return: (str) Devuelve el texto de entrada sin las palabras que hayan sido identificadas de acuerdo a los \
        criterios especificados por el usuario. 


..
   comentario: la siguiente instrucción genera un error al usar autodoc porque el script \
   utils/limpieza:aux.py tiene un import por fuera de la carpeta, python no genera un error \
   pero sphinx arroja un warning y termina la lectura del archivo, por eso tocó incluir el \
   docstring acá.

    .. automodule:: utils.limpieza_aux
       :members: substrings_en_comun
       :undoc-members:
       :show-inheritance:
       :exclude-members: 

