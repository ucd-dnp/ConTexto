import re
import unicodedata
import pkg_resources
from utils.tokenizacion import tokenizar, destokenizar


def remover_acentos(texto):
    """
    Quita los acentos (tildes, diéresis, virgulilla) de un texto de entrada. \
    Esta reemplaza cada carácter con acento en el texto por su equivalente \
    sin acento.

    :param texto: Texto de entrada.
    :type texto: str
    :return: (str) Texto sin acentos después de la limpieza.
    """
    try:
        texto = unicode(texto, "utf-8")
    except NameError:
        pass
    texto = (
        unicodedata.normalize("NFD", texto)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    return str(texto)


def remover_stopwords(
    texto,
    lista_palabras=[],
    lista_expresiones=[],
    ubicacion_archivo=None,
    tokenizador=None,
):
    """
    Quita las palabras y expresiones determinadas de un texto. Esta función \
    quita del texto de entrada, palabras específicas contenidas en \
    `lista_palabras`, o expresiones de palabras contenidas en \
    `lista_expresiones`.

    :param texto: Texto al cual se le quitarán palabras y expresiones \
        contenidas en `lista_palabras` y `lista_expresiones`.
    :type texto: str
    :param lista_palabras: Lista de palabras que se desean quitar del texto. \
        Por ejemplo, la lista `['hola', 'de', 'a']` eliminará esas palabras.
    :type lista_palabras: list, opcional
    :param lista_expresiones: Lista de expresiones que se quieren quitar al \
        texto. A diferencia de `lista_palabras`, esta puede contener palabras \
        compuestas. Por ejemplo, \
        `['San juan de Dios', 'Distrito Capital, 'fuente de agua']`; esta \
        lista quitará esas palabras compuestas del texto de entrada.
    :type lista_expresiones: list, opcional
    :param ubicacion_archivo: Ruta del archivo plano que contiene la \
        lista de palabras y/o lista de palabras separadas por espacios, comas \
        o saltos de línea. En caso contrario no es necesario especificar los \
        parametros `lista_palabras` y `lista_expresiones`. \
        Valor por defecto: None.
    :type ubicacion_archivo: str, opcional
    :param tokenizador: Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una \
        instancia de la clase `TokenizadorNLTK`.
    :type tokenizador: Tokenizer, opcional
    :return: (str) Texto sin las palabras y expresiones incluidas en la \
        limpieza.
    """
    if ubicacion_archivo is not None:
        lista_palabras, lista_expresiones = cargar_stopwords(ubicacion_archivo)
    # Quitar las expresiones no deseadas
    for expresion in set(lista_expresiones):
        texto = texto.replace(expresion, " ")
    # Dejar solo las palabras que no aparecen en la lista de palabras no
    # deseadas
    tokens = tokenizar(texto, tokenizador)
    texto = destokenizar(
        [p for p in tokens if p not in set(lista_palabras)], tokenizador
    )
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +", " ", texto)
    return texto


def remover_palabras_cortas(texto, n_min):
    """
    Quita las palabras en el texto con longitud estrictamente menor a `n_min`.

    :param texto: Texto de entrada al que se quitarán las palabras de \
        longitudes menores a `n_min`.
    :type texto: str
    :param n_min: Longitud mínima de las palabras aceptadas en el texto \
         de entrada.
    :type n_min: int
    :return: (str) Texto sin las palabras de longitud menor a `n_min`.
    """
    palabras = texto.split(" ")
    return " ".join([palabra for palabra in palabras if len(palabra) >= n_min])


def limpieza_basica(texto, quitar_numeros=True, ignorar_mayus=True):
    """
    Limpieza básica del texto. Esta función realiza una limpieza básica del \
    texto de entrada, transforma todo el texto a letras minúsculas, quita \
    signos de puntuación y caracteres especiales, remueve espacios múltiples \
    dejando solo espacio sencillo y caracteres de salto de línea o \
    tabulaciones.

    :param texto: Texto de entrada al que se le aplicará la limpieza \
        básica.
    :type texto: str
    :param quitar_numeros: Indica si desea quitar los números dentro del \
        texto. Valor por defecto `True`.
    :type quitar_numeros: bool, opcional
    :param ignorar_mayus: Si `ignorar_mayus = True`, convierte el texto todo\
        a letras minúsculas, en caso contrario, deja el texto como el \
        original. Valor por defecto `True`.
    :type ignorar_mayus: bool, opcional
    :return: (str) Texto después de la limpieza básica.
    """
    # Texto a minúsculas
    if ignorar_mayus:
        texto = texto.lower()
    # Pone un espacio antes y después de cada signo de puntuación
    texto = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", texto)
    # Quita caracteres especiales del texto.
    # RegEx adaptada de https://stackoverflow.com/a/56280214
    if quitar_numeros:
        texto = re.sub(r"[^ a-zA-ZÀ-ÖØ-öø-ÿ]+", " ", texto)
    else:
        texto = re.sub(r"[^ a-zA-ZÀ-ÖØ-öø-ÿ0-9]+", " ", texto)
    # Reemplaza espacios múltiples por un solo espacio
    texto = re.sub(r" +", " ", texto)
    # Quitar espacios, tabs y enters en los extremos del texto
    texto = texto.strip(" \t\n\r")
    return texto


def limpieza_texto(
    texto,
    lista_palabras=[],
    lista_expresiones=[],
    ubicacion_archivo=None,
    n_min=0,
    quitar_numeros=True,
    quitar_acentos=False,
    ignorar_mayus=True,
    tokenizador=None,
    momento_stopwords="ambos",
):
    """
    Limpieza completa de texto. Esta función hace una limpieza exhaustiva del \
    texto de entrada. Es capaz de quitar palabras y expresiones contenidas en \
    `lista_palabras` y `lista_expresiones`, quita acentos de las palabras, \
    números y palabras de longitud menor a `n_min`.

    :param texto: Texto de entrada al que se le aplicará la limpieza.
    :type texto: str
    :param lista_palabras: Lista de palabras que se desean quitar del texto. \
        Por ejemplo, la lista `['hola', 'de', 'a']` eliminará esas palabras.
    :type lista_palabras: list, opcional
    :param lista_expresiones: Lista de expresiones que se quieren quitar al \
        texto. A diferencia de `lista_palabras`, esta puede contener palabras \
        compuestas. Por ejemplo, \
        `['San juan de Dios', 'Distrito Capital, 'fuente de agua']`; esta \
        lista quitará esas palabras compuestas del texto de entrada.
    :type lista_expresiones: list, opcional
    :param ubicacion_archivo: Ruta del archivo plano que contiene la \
        lista de palabras y/o lista de palabras separadas por espacios, comas \
        o saltos de línea. En caso contrario no es necesario especificar los \
        parametros `lista_palabras` y `lista_expresiones`. \
        Valor por defecto: None.
    :type ubicacion_archivo: str, opcional
    :param n_min: Longitud mínima de las palabras aceptadas en el texto \
         de entrada. Valor por defecto `0`.
    :type n_min: int, opcional
    :param quitar_numeros: Indica si desea quitar los números dentro del \
        texto. Valor por defecto `True`.
    :type quitar_numeros: bool, opcional
    :param quitar_acentos: Opción para determinar si se quitan acentos \
        (tildes, diéresis, virgulilla) del texto. Valor por defecto `False`.
    :type quitar_acentos: bool, opcional
    :param ignorar_mayus: Si `ignorar_mayus = True`, convierte el texto todo\
        a letras minúsculas, en caso contrario, deja el texto como el \
        original. Valor por defecto `True`.
    :type ignorar_mayus: bool, opcional
    :param tokenizador: Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una \
        instancia de la clase `TokenizadorNLTK`.
    :type tokenizador: Tokenizer, opcional
    :param momento_stopwords: Indica en que parte del proceso de limpieza de \
        texto se remueven las `stopwords`. Las opciones son hacerlo antes o \
        después de las demás operaciones de limpieza del texto, eligiendo \
        los valores `antes` o `despues`. También es posible remover \
        `stopwords` de los textos en ambos instantes al asignar el valor \
        `momento_stopwords = 'ambos'`. Valor por defecto `ambos`.
    :type momento_stopwords: {'antes', 'después', 'ambos'}, opcional
    :return: (str) Texto después de la limpieza completa.
    """
    # Estandarizar parámetro de momento_stopwords
    momento_stopwords = remover_acentos(momento_stopwords).lower()
    # Quitar palabras y expresiones no deseadas. Se hace al texto original
    # porque la palabra/expresión a remover puede tener tildes/mayúsculas
    # /signos o estar compuesta por palabras cortas
    if momento_stopwords in ("antes", "ambos"):
        texto = remover_stopwords(
            texto,
            lista_palabras,
            lista_expresiones,
            ubicacion_archivo,
            tokenizador,
        )
    # Se verifica si se desean quitar acentos/tildes
    if quitar_acentos:
        texto = remover_acentos(texto)
    # Limpieza básica del texto
    texto = limpieza_basica(texto, quitar_numeros, ignorar_mayus)
    # Quita palabras cortas y palabras pertenecientes a una lista específica
    texto = remover_palabras_cortas(texto, n_min)
    # Se quitan stopwords de nuevo, por si habían palabras que después de
    # su limpieza quedan en
    # la lista de palabras/expresiones no deseadas
    if momento_stopwords in ("despues", "ambos"):
        texto = remover_stopwords(
            texto,
            lista_palabras,
            lista_expresiones,
            ubicacion_archivo,
            tokenizador,
        )
    return texto


def limpiar_extremos(texto):
    """
    Quita los espacios presentes al inicio y al final de una cadena de texto.

    :param texto: Texto de entrada.
    :type texto: str
    :return: (str) Texto sin espacios en el inicio y en el final.
    """
    return texto.strip()


def quitar_repetidos(texto, sep="|", remover_espacios=True):
    """
    Función para quitar frases o palabras repetidas que están separadas por \
    un caracter en específico.

    :param texto: Texto de entrada.
    :type texto: str
    :param sep: Separador determinado para encontrar palabras repetidas. \
        Valor por defecto `'|'`.
    :type sep: str, opcional
    :param remover_espacios: Si `remover_espacios = True` quita los espacios \
        presentes al inicio y al final de una palabra. Valor por defecto \
        `True`.
    :type remover_espacios: bool, opcional
    :return: (str) Texto sin palabras o expresiones repetidas.
    """
    lista = texto.split(sep)
    if remover_espacios:
        lista = [limpiar_extremos(i) for i in lista]
    # Para preservar el orden de aparición. Tomado de
    # https://stackoverflow.com/a/58666031
    seen = set()
    lista = [i for i in lista if not (i in seen or seen.add(i))]
    return " ".join(lista)


def cargar_stopwords(ubicacion_archivo, encoding="utf8"):
    """
    Función para cargar las listas de palabras y expresiones que se desean \
    eliminar de un texto a partir de un archivo plano.

    :param ubicacion_archivo: Ruta del directorio o carpeta que contiene \
        los archivos planes de lista de palabras y/o lista de expresiones \
        separadas por comas, espacios o saltos de línea.
    :type ubicacion_archivo: str
    :param encoding: Codificación del archivo de texto. Valor por defecto \
        `'utf-8'`.
    :type encoding: str, opcional
    :return: (tuple) Tupla que contiene: \
        |ul|
        |li| lista_palabras (list): Lista que contiene las palabras que \
        se desean quitar en un texto. |/li|
        |li| lista_expresiones (list): Lista que contiene las expresiones \
        que se desean quitar de un texto. |/li|
        |/ul|
    """
    lista_palabras = []
    lista_expresiones = []
    with open(ubicacion_archivo, encoding=encoding) as fp:
        line = fp.readline()
        while line:
            linea = line.strip().split(",")
            for i in linea:
                i = limpiar_extremos(i)
                if len(i.split(" ")) > 1:
                    lista_expresiones.append(i)
                else:
                    lista_palabras.append(i)
            line = fp.readline()
    return lista_palabras, lista_expresiones


def lista_stopwords(lenguaje="es"):
    """
    Genera una lista de stopwords (palabras que se quieren quitar de un \
    texto). Función que genera una lista de stopwords de un idioma \
    predeterminado.

    :param lenguaje: Define el lenguaje para la generación de las \
        stopwords. Para mayor información, consultar la sección de \
        :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
        Valor por defecto `'es'`.
    :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcio
    :return: (list) Lista de palabras stopwords del idioma seleccionado.
    """
    from lenguajes import definir_lenguaje

    lenguaje = definir_lenguaje(lenguaje, False)

    from nltk.corpus import stopwords

    try:
        sw = stopwords.words(lenguaje)
    except Exception:
        import nltk

        nltk.download("stopwords")
        sw = stopwords.words(lenguaje)
    # Si se quieren en español, se intenta sacar las stopwords
    # desde la lista predfinida que viene con la librería
    if lenguaje == "spanish":
        try:
            ruta = pkg_resources.resource_filename(
                __name__, "data/listas_stopwords/sw_es.txt"
            )
            sw = cargar_stopwords(ruta, "latin-1")[0]
        except BaseException:
            pass
    # Quitar elemento vacío de la lista, si está
    if "" in sw:
        sw.remove("")
    # Devolver stopwords
    return sw


def lista_nombres(tipo="todos"):
    """
    Genera lista de nombres más comunes del español. Retorna lista con los \
    nombres más comunes, tanto para hombre y mujer del idioma español. La \
    función permite generar lista de nombres solo de mujeres o solo de \
    hombres con el parámetro `tipo`.

    :param tipo: Permite generar una lista de nombres de: solo mujeres \
        (`tipo='mujeres'`), solo nombres de hombres (`tipo='hombres'`) o \
        ambos (`tipo='todos'`). Valor por defecto `todos`.
    :type tipo: {'todos', 'mujeres', 'hombres'}, opcional
    :return: (list) Lista de nombres en español.
    """
    if tipo.lower() in ["m", "masculino", "hombre", "hombres"]:
        ruta = pkg_resources.resource_filename(
            __name__, "data/listas_stopwords/nombres_hombres.txt"
        )
        return cargar_stopwords(ruta)
    elif tipo.lower() in ["f", "femenino", "mujer", "mujeres"]:
        ruta = pkg_resources.resource_filename(
            __name__, "data/listas_stopwords/nombres_mujeres.txt"
        )
        return cargar_stopwords(ruta)
    elif tipo == "todos":
        ruta = pkg_resources.resource_filename(
            __name__, "data/listas_stopwords/nombres_ambos.txt"
        )
        lista_todos = list(cargar_stopwords(ruta))
        lista_hombres = lista_nombres("hombre")
        lista_mujeres = lista_nombres("mujer")
        for i in range(2):
            lista_todos[i] += lista_hombres[i] + lista_mujeres[i]
            lista_todos[i] = sorted(list(set(lista_todos[i])))

        return lista_todos[0], lista_todos[1]
    else:
        print(
            (
                "Por favor ingresar un tipo válido de "
                'nombres ("hombres", "mujeres" o "todos").'
            )
        )
        return [], []


def lista_apellidos():
    """
    Genera lista de apellidos más comunes del español.

    :return: (list) Lista de apellidos más comunes del español.
    """
    ruta = pkg_resources.resource_filename(
        __name__, "data/listas_stopwords/apellidos.txt"
    )
    return cargar_stopwords(ruta)


def lista_geo_colombia(tipo="todos"):
    """
    Genera lista de nombres de municipios y departamentos de Colombia.

    :param tipo: Si `tipo = 'todos'` genera una lista de nombres de \
        municipios y departamentos de Colombia. Si `tipo = 'municipios'` \
        genera nombres solo de municipios. Si `tipo = 'departamentos'` \
        genera nombres solo de departamentos. Valor por defecto `todos`.
    :type tipo: {'todos', 'municipios', 'departamentos'}, opcional
    :return: (list) Lista de nombres de municipios, departamentos o ambos.
    """
    ruta_mun = pkg_resources.resource_filename(
        __name__, "data/listas_stopwords/municipios_col.txt"
    )
    ruta_dep = pkg_resources.resource_filename(
        __name__, "data/listas_stopwords/departamentos_col.txt"
    )
    if tipo == "todos":
        palabras = sorted(
            list(
                set(
                    cargar_stopwords(ruta_mun)[0]
                    + cargar_stopwords(ruta_dep)[0]
                )
            )
        )
        expresiones = sorted(
            list(
                set(
                    cargar_stopwords(ruta_mun)[1]
                    + cargar_stopwords(ruta_dep)[1]
                )
            )
        )
        return palabras, expresiones
    elif tipo.lower() in ["municipios", "mun", "m"]:
        return cargar_stopwords(ruta_mun)
    elif tipo.lower() in ["departamentos", "dep", "d"]:
        return cargar_stopwords(ruta_dep)
    else:
        print(
            (
                "Por favor ingresar un tipo válido de lugares"
                '("municipios", "departamentos" o "todos").'
            )
        )
        return [], []
