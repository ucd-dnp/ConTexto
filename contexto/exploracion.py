import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as cl
import networkx as nx
import numpy as np
import pandas as pd
import warnings
from collections import Counter, Iterable
from wordcloud import WordCloud, ImageColorGenerator
from limpieza import limpieza_basica
from utils.tokenizacion import tokenizar, TokenizadorNLTK
from utils.dispersion_plot import dispersionPlot


def obtener_ngramas(
    texto, n=1, devolver_lista=True, limpiar=False, tokenizador=None
):
    """
    Permite generar n-gramas a partir de un texto.

    :param texto: Texto sobre el que se calculará los n-gramas.
    :type: str
    :param n: Cantidad de elementos a tener en cuenta en la generación \
        de n-gramas. Por ejemplo, si `n = 1` se retornarán palabras, \
        y si `n = 2` se retornarán bigramas, si `n = 3` se retornarán \
        trigramas y así sucesivamente. Valor por defecto `2`.
    :type n: int
    :param devolver_lista:  Si `devolver_lista` es `True` se retorna un \
        objeto tipo lista; si el valor es `False` se retorna un objeto tipo \
        generador. Valor por defecto `True`
    :type devolver_lista: bool, opcional
    :param limpiar: Define si se desea hacer una limpieza básica (aplicando \
        la función  `limpieza_basica` del módulo `limpieza`) al texto de \
        entrada, antes de encontrar los n-gramas. Valor por defecto `False`.
    :type limpiar: bool, opcional
    :param tokenizador: Objeto encargado de la tokenización y \
        detokenización de textos. Si el valor es `None`, se cargará por \
        defecto una instancia de la clase `TokenizadorNLTK`. Valor por \
        defecto `None`.
    :type tokenizador: object, opcional
    :return: (list, generator) n-gramas generados con las características \
        especificadas.
    """
    if limpiar:
        texto = limpieza_basica(texto)
    lista = tokenizar(texto, tokenizador)
    n_gramas = (
        " ".join(lista[i : i + n])
        for i in range(len(lista))
        if i + n <= len(lista)
    )
    if devolver_lista:
        n_gramas = list(n_gramas)
    return n_gramas


def frecuencia_ngramas(texto, n_grama=1, n_max=None):
    """
    Genera un diccionario con los n-gramas y sus respectivas frecuencias de \
    ocurrencia en el texto.

    :param texto: Texto sobre el que se calculará la frecuencia de n-gramas.
    :type: str
    :param n_grama: Cantidad de elementos a tener en cuenta en la generación \
        de n-gramas. Por ejemplo, si `n_grama = 1` se retornará frecuencia de \
        palabras, si `n_grama = 2` se retornará frecuencia de bigramas, si \
        `n_grama = 3` se retornará frecuencia de trigramas y así \
        sucesivamente. Valor por defecto `2`.
    :type n: int
    :param n_max: Cantidad máxima de n-gramas a generar. Valor por defecto \
        `None`.
    :type n_max: int, opcional
    :return: (dict) diccionario de n-gramas más frecuentes.
    """
    lista = obtener_ngramas(texto, n_grama)
    cont = Counter(lista)
    if n_max is not None:
        dictu = dict(cont.most_common(n_max))
    else:
        dictu = dict(cont)
    return dictu


def nube_palabras(
    texto,
    n_grama=1,
    n_terminos=100,
    graficar=True,
    dim_figura=(10, 10),
    hor=0.6,
    titulo="Términos más frecuentes",
    ubicacion_archivo=None,
    forma=None,
    color_fondo="white",
    color_contorno="blue",
    grosor_contorno=0,
    colores_forma=False,
    semilla=1234,
    devolver_nube=False,
    mask=None,
):
    """
    Permite graficar o exportar una nube de palabras (o n-gramas) a partir de \
    un texto de entrada.

    :param texto: Texto de entrada que se desea analizar.
    :type texto: str
    :param n: Cantidad de elementos a tener en cuenta en la generación \
        de n-gramas. Por ejemplo, si `n = 1` se retornarán palabras, \
        y si `n = 2` se retornarán bigramas, si `n = 3` se retornarán \
        trigramas y así sucesivamente. Valor por defecto `2`.
    :param n_terminos:Cantidad de n-gramas que se incluyen en la nube. \
        Se graficarán los `n_terminos` más frecuentes en \
        el texto. Valor por defecto `100`
    :type n_terminos: int, opcional
    :param graficar: Permite visualizar la gráfica en el `IDE`_ que esté \
        utilizando. Valor por defecto `True`.
    :type graficar: bool, opcional
    :param dim_figura: Corresponden al tamaño (ancho y alto) de la figura. \
        Valor por defecto `(10, 10)`.
    :type dim_figura: (float, float)
    :param hor: Valor entre `0` y `1` Proporción de los términos que \
        se mostrarán de manera horizontal en la nube. Para `hor = 0` todos \
        los térmonos se mostrarán verticalmente; para `hor = 1` todos los \
        términos se mostrarán horizontalmente, y para valores intermedios \
        habrá una combinación de términos en ambas representaciones. Valor \
        por defecto `0.6`
    :type hor: float, opcional
    :param titulo: Corresponde al título de la nube de palabras. \
        Valor por defecto `"Términos más frecuentes"`.
    :type titulo: str, opcional
    :param ubicacion_archivo: Ruta donde desea exportar la gráfica como \
        archivo tipo imagen. Al nombrar el archivo se recomienda utilizar \
        la extensión `jpg`. Si `ubicacion_archivo = None`, gráfica no será \
        exportada. Valor por defecto `None`.
    :type ubicacion_archivo: str, opcional
    :param forma: Arreglo de Numpy o ubicación de archivo de imagen que \
        contenga la forma que se le desea dar a la nube de palabras. Si \
        `forma = None`, se ordenarán los términos de la nube en forma de \
        círculo. Valor por defecto `None`.
    :type forma: numpy.array, str, opcional
    :param color_fondo: Color de fondo de la nube de palabras. Se puede \
        ingresar como el nombre del color (si Python lo reconoce), código \
        hexadecimal o como una tupla con sus valores (R, G, B). Valor por \
        defecto `"white"`.
    :type color_fondo: str, tuple, opcional
    :param color_contorno: Color del contorno de la forma de la nube de \
        palabras. Se puede ingresar como el nombre del color (si Python \
        lo reconoce), código hexadecimal o como una tupla con sus valores \
        (R, G, B). Valor por defecto `"blue"`.
    :type color_contorno: str, tuple, opcional
    :param grosor_contorno: Grosor de la línea (contorno) que define la \
        forma de la nube de palabras. Si `grosor_contorno = 0`, no se \
        graficará el contorno. Valor por defecto `0`.
    :type grosor_contorno: int, opcional
    :param colores_forma: Indica si se quieren utilizar en la nube de \
        palabras los colores extraídos de la imagen o numpy array utilizada \
        para definir la forma de la nube. Valor por defecto `False`.
    :type colores_forma: bool, opcional
    :param semilla: Corresponde al estado inicial del generador. Este \
        parámetro incide en la posición y color de las palabras. En caso de \
        querer replicar la nube de palabras, se recomienda utilizar un mismo \
        valor de `semilla`. Valor por defecto `1234`.
    :type semilla: int, opcional
    :param devolver_nube: Indica si se desea obtener la nube de palabras como \
        un objeto tipo `WordCloud`. Valor por defecto `False`.
    :type devolver_nube: bool, opcional
    :return: (WordCloud) objeto  de tipo `WordCloud`, solo si \
        `devolver_nube = True`.
    """
    # Si se usa el parámetro anterior (mask) se pone la deprecation warning
    # y se asigna su valor a "forma"
    if forma is None and mask is not None:
        msj = (
            "El parámetro 'mask' ha sido reemplazado por el parámetro ",
            "'forma'. Futuras versiones de la librería no contarán con el ",
            "parámetro 'mask'.",
        )
        warnings.warn(msj, DeprecationWarning, stacklevel=2)
        forma = mask
    # Por defecto se crea una máscara circular para ordenar la nube
    if forma is None:
        x, y = np.ogrid[:600, :600]
        forma = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
        forma = 255 * forma.astype(int)
    else:
        # Si se pasó la ubicación de una imagen, se carga
        if isinstance(forma, str):
            forma = cv2.imread(forma)
        # Si se pasó una imagen a color, se conservan sus colores y se
        # convierte a escala de grises
        colores_nube = None
        if len(forma.shape) == 3:
            colores_nube = ImageColorGenerator(forma)
            forma = cv2.cvtColor(forma, cv2.COLOR_BGR2GRAY)
        # Se aplica un umbral para eliminar ruido y marcas de agua de
        # la máscara
        forma = cv2.threshold(
            forma, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )[1]
        # Si la mayoría de la imagen está en negro, se invierte la
        # imagen máscara
        if np.mean(forma) < 100:
            forma = 255 - forma
        # Operación de "closing" para rellenar huecos en la imagen máscara
        kernel = np.ones((5, 5), np.uint8)
        forma = 255 - cv2.morphologyEx(255 - forma, cv2.MORPH_CLOSE, kernel)
    # Obtener diccionario de 'n_terminos' más frecuentes con sus frecuencias
    dictu = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Crear la nube de palabras
    nube = WordCloud(
        background_color=color_fondo,
        contour_color=color_contorno,
        prefer_horizontal=hor,
        mask=forma,
        random_state=semilla,
        contour_width=grosor_contorno,
    )
    figura = nube.generate_from_frequencies(dictu)
    # Si se eligió mantener los colores de la imagen de forma, se cambian
    # los colores a la nube
    if colores_forma and colores_nube is not None:
        nube = nube.recolor(color_func=colores_nube)
    # Devolver el objeto de la nube, para graficarlo de otra manera
    if devolver_nube:
        return figura
    else:
        # Graficar y/o guardar la imagen generada
        grafica_nube(figura, dim_figura, titulo, ubicacion_archivo, graficar)


def grafica_nube(
    nube,
    dim_figura=(10, 10),
    titulo="Términos más frecuentes",
    ubicacion_archivo=None,
    graficar=True,
):
    """
    Permite graficar o guardar una nube de palabras.

    :param nube: Objeto tipo `WordCloud` correspondiente a la nube \
        de palabras.
    :type: WordCloud
    :param dim_figura: Corresponden al ancho y alto de la figura en pulgadas. \
        Valor por defecto: `(10, 10)`.
    :type dim_figura: (float, float), opcional
    :param titulo: Título de la nube de palabras. Valor por defecto: \
        `'Términos más frecuentes'`.
    :type titulo: str, opcional
    :param ubicacion_archivo: Ruta donde desea exportar la gráfica como \
        archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la \
        extensión `jpg`. Si  `ubicacion_archivo = None`, la gráfica no se \
        exporta. Valor por defecto `None`.
    :type :
    :param graficar: (bool) {True, False} Valor por defecto: True. Permite \
        visualizar la gráfica en el `IDE`_ que esté utilizando.
    """

    fig = plt.figure(figsize=dim_figura)
    plt.imshow(nube, interpolation="bilinear")
    if titulo != "":
        plt.title(titulo)
    plt.axis("off")
    if graficar:
        plt.show()
    if ubicacion_archivo is not None:
        fig.savefig(ubicacion_archivo)
    # Cerrar gráfica
    plt.close()


def par_nubes(
    texto,
    n1=1,
    n2=2,
    dim_figura=(20, 11),
    ubicacion_archivo="",
    graficar=True,
    devolver_grafica=False,
):
    """
    Permite graficar o exportar un par de nubes de palabras (una junto a \
    otra) a partir de un texto.

    :param texto:Corresponde al texto que se desea analizar.
    :type texto: str
    :param n1: Cantidad de elementos a tener en cuenta en la generación de \
        n-gramas de la nube de palabras izquierda. Valor por defecto `1`.
    :type n1: int, opcional
    :param n2: Cantidad de elementos a tener en cuenta en la generación de \
        n-gramas de la nube de palabras derecha. Valor por defecto `2`.
    :type n2: int, opcional
    :param dim_figura: (float, float) Valor por defecto: (20, 10). \
        Corresponden al ancho y alto de la figura en pulgadas.
    :param ubicacion_archivo: (str) Valor por defecto: ''. Ruta donde desea \
        exportar la gráfica como archivo tipo imagen. Al nombrar el archivo \
        se recomienda utilizar la extensión jpg. Si no se especifica una ruta,\
         la gráfica no se exporta.
    :param graficar: (bool) {True, False} Valor por defecto: True. Permite \
        visualizar la gráfica en el `IDE`_ que esté utilizando.
    :param devolver_grafica: (bool) {True, False} Valor por defecto: False. \
        Indica si se desea obtener el gráfico con el par de nubes de palabras \
        como un objeto de Matplotlib.
    :return: (objeto Figure de Matplotlib) Figura con el par de nubes de \
        palabras, solo si devolver_grafica=True.
    """

    # Obtener nubes de palabras
    nube_1 = nube_palabras(texto, n_grama=n1, hor=0.8, devolver_nube=True)
    nube_2 = nube_palabras(texto, n_grama=n2, hor=1, devolver_nube=True)

    # Graficar nubes y mostrarlas
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=dim_figura,
        gridspec_kw={"hspace": 0, "wspace": 0},
    )

    ax1.imshow(nube_1, interpolation="bilinear")
    tit = "términos" if n1 == 1 else f"n_gramas ({n1})"
    ax1.set_title(f"Nube de palabras: {tit}", size=18)

    ax2.imshow(nube_2, interpolation="bilinear")
    tit = "términos" if n2 == 1 else f"n_gramas ({n2})"
    ax2.set_title(f"Nube de palabras: {tit}", size=18)

    fig.suptitle("Términos más frecuentes", size=28, y=0.99)
    plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
    if graficar:
        plt.show()
    if ubicacion_archivo != "":
        fig.savefig(ubicacion_archivo)
    if devolver_grafica:
        return fig
    # Cerrar gráfica
    plt.close()


def matriz_coocurrencias(
    texto,
    min_frec=1,
    max_num=200,
    modo="documento",
    ventana=3,
    tri_sup=True,
    limpiar=False,
    tokenizador=None,
):
    """
    Calcula la matriz de coocurrencias de un texto.

    :param texto: Corresponde al texto (o lista de textos/documentos) que \
        se desea analizar.
    :type texto: str, list
    :param min_frec: Frecuencia mínima de aparición de palabras, si la \
        frecuencia de una palabra es menor a `min_frec`, será excluida de la \
        matriz. Valor por defecto `1`.
    :type min_frec: int, opcional
    :param max_num: Número máximo de palabras que se incluyen en la matriz \
        (se eligen las más frecuentes). Valor por defecto `200`.
    :type max_num: int, opcional
    :param modo: Corresponde al modo de análisis, con `'documento'` se \
        calcula la coocurrencia de términos sin importar la distancia entre \
        estos,  con `'ventana'` se calcula la coocurrencia de términos \
        teniendo en cuenta una distancia máxima entre estos. \
        Valor por defecto `'documento'`.
    :type modo: {'documento', 'ventana'}, opcional
    :param ventana: Tamaño de la ventana (solo cuando `modo = 'ventana'`). \
        Número de palabras anteriores o posteriores a tener en cuenta con \
        respecto al término de análisis, equivalente a calcular la \
        coocurrencia con n-gramas, siendo  `n = ventana + 1`. \
        Valor por defecto `3`.
    :type ventana: int, opcional
    :param tri_sup: Si es `True` devuelve la versión diagonal superior de la \
        matriz de coocurrencias, si es `False` devuelve la matriz completa. \
        Valor por defecto `True`.
    :type tri_sup: bool, opcional
    :param limpiar: Define si se desea hacer una limpieza básica (aplicando \
        la función `limpieza_basica` del módulo `limpieza`) al texto, antes \
        de calcular las coocurrencias. Valor por defecto `False`.
    :type limpiar: bool, opcional
    :param tokenizador: Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una \
        instancia de la clase *TokenizadorNLTK*. Valor por defecto `None`.
    :type tokenizador: Tokenizador, opcional
    :return: (pandas.DataFrame) Matriz de coocurrencias de los textos de \
        entrada.
    """
    # Generar un solo texto con todos los documentos
    if isinstance(texto, Iterable) and not isinstance(texto, str):
        texto_entero = " ".join([str(i) for i in texto])
    else:
        texto_entero = str(texto)
        texto = [texto_entero]  # Convertir variable "texto" en un iterable

    if limpiar:
        texto = [limpieza_basica(t) for t in texto]
        texto_entero = " ".join([texto])
    # Se inicializa un solo tokenizador, para ahorrar un poco de tiempo
    tok = TokenizadorNLTK() if tokenizador is None else tokenizador
    # Generar lista de palabras en todos los textos juntos
    palabras = tokenizar(texto_entero, tok)
    # Dejar solo las palabras con mayor frecuencia y/o que cumplan una
    # frecuencia mínima
    cuenta = dict(Counter(palabras).most_common(max_num))
    cuenta_filt = {k: v for k, v in cuenta.items() if v >= min_frec}
    nombres = list(set(cuenta_filt.keys()))
    # Inicializar en ceros la matriz de coocurrencias
    mat_oc = pd.DataFrame(
        np.zeros([len(nombres), len(nombres)]), columns=nombres, index=nombres
    )
    if modo == "ventana":
        for t in texto:
            palabras_t = tokenizar(t, tok)
            # Ciclo a través de las palabras para obtener las coocurrencias:
            for i, p1 in enumerate(palabras_t):
                inicio = max(0, i - ventana)
                fin = min(len(palabras), i + ventana + 1)
                for j, p2 in enumerate(palabras_t[inicio:fin]):
                    if (p2 in nombres) and (p1 in nombres):
                        if p1 != p2:
                            mat_oc[p2][p1] += 1
                        else:
                            if (inicio + j) != i:
                                mat_oc[p2][p1] += 1
    elif modo == "documento":
        for t in texto:
            cuenta_t = dict(Counter(tokenizar(t, tok)))
            for p1 in nombres:
                for p2 in nombres:
                    if p1 != p2:
                        if p1 in cuenta_t and p2 in cuenta_t:
                            mat_oc[p2][p1] += cuenta_t[p1] * cuenta_t[p2]
                    else:
                        if p1 in cuenta_t:
                            mat_oc[p2][p1] += cuenta_t[p1]

    # Ordenar filas y columnas alfabeticamente
    mat_oc.sort_index(inplace=True)
    mat_oc = mat_oc.reindex(sorted(mat_oc.columns), axis=1)
    if tri_sup:
        mat_oc = diag_superior(mat_oc)

    return mat_oc


def diag_superior(df):
    """
    Función que acepta una dataframe y devuelve la versión diagonal superior \
    de la misma.

    :param df: Matriz de entrada.
    :type df: pandas.DataFrame
    :return: (pandas.DataFrame) Matriz diagonal superior.
    """
    return pd.DataFrame(np.triu(df), index=df.index, columns=df.columns)


def graficar_coocurrencias(
    mat,
    prop_fuera=0,
    ubicacion_archivo=None,
    graficar=True,
    K=5,
    color_borde="orchid",
    color_nodo="silver",
    semilla=123,
    dim_figura=(13, 13),
    devolver_grafica=False,
    circular=False,
):
    """
    Grafica una matriz de coocurrencias de términos como un grafo no dirigido.

    :param mat: Matriz de coocurrencias que desea graficar.
    :type mat: pandas.DataFrame
    :param prop_fuera: (valor entre 0 y 100). Permite eliminar las \
        conexiones con menor peso para aclarar un poco la imagen. Si \
        `prop_fuera = 0` no se elimina ninguna conexión. Valor por defecto \
        `0`.
    :type prop_fuera: float, opcional
    :param ubicacion_archivo: Ruta donde desea exportar la gráfica como \
        archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la \
        extensión `jpg`. Si `ubicacion_archivo = None` la gráfica no se \
        exporta. Valor por defecto `None`.
    :type ubicacion_archivo: str, opcional
    :param graficar: Permite visualizar la gráfica. Valor por defecto `True`.
    :type graficar: bool, opcional
    :param K: Distancia óptima entre nodos, aumente este valor para separar \
        los nodos. Valor por defecto `5`.
    :type K: float, opcional
    :param color_borde: (str)  Corresponde al color de los bordes de la red, \
        se puede asignar el nombre de un color predefinido o el código \
        hexadecimal. Valor por defecto `'orchid'`.
    :type color_borde: str, opcional
    :param color_nodo: (str) Valor por defecto: 'silver'. Corresponde al color\
         de los nodos, se puede asignar el nombre de un color predefinido o \
        el código hexadecimal de un color.
    :param semilla: Estado inicial del generador aleatorio para establecer la \
        posición de los nodos.Valor por defecto `123`.
    :type semilla: int, opcional
    :param dim_figura: Corresponden al ancho y alto de la figura en pulgadas. \
        Valor por defecto `(13, 13)`.
    :type dim_figura: (float, float), opcional
    :param devolver_grafica: Indica si se desea obtener el gráfico de \
        coocurrencias como un objeto de `Matplotlib`. \
        Valor por defecto `False`.
    :type devolver_grafica: bool, opcional
    :return: (Matplotlib.Figure) Figura con el grafo de \
        coocurrencias, solo si `devolver_grafica = True`.
    """
    # Definir el valor máximo de la matriz y de la diagonal
    max_cooc = max(mat.max())
    max_diag = max(np.diag(mat))
    # Definir lista de conexiones (edges)
    lista_bordes = []
    for indice, fila in mat.iterrows():
        i = 0
        for col in fila:
            peso = float(col) / np.log10(max_cooc)
            lista_bordes.append((indice, mat.columns[i], peso))
            i += 1
    # Quitar de la lista conexiones con peso 0 (no hay co-ocurrencia)
    lista_bordes = [x for x in lista_bordes if x[2] > 0.0]
    # Quitar conexiones de un nodo consigo mismo
    for i in lista_bordes:
        if i[0] == i[1]:
            lista_bordes.remove(i)
    # Definir lista de vértices (nodes)
    lista_nodos = [[i, mat.loc[i, i] / np.log(max_diag)] for i in mat.columns]
    for i, nodo in enumerate(lista_nodos):
        if nodo[1] == 0.0:
            lista_nodos[i][1] += 0.1
    # Definir tamaños de nodos y bordes del grafo
    offset_y = 0.06
    escalar_nodo = 200
    escalar_borde = 0.0055
    sizes = [x[1] for x in lista_nodos]
    anchos = [x[2] for x in lista_bordes]
    # Acotar los tamaños en el percentil 99 para evitar valores demasiado altos
    anchos = np.clip(anchos, 0, np.percentile(anchos, 99))
    sizes = np.clip(sizes, 0, np.percentile(anchos, 99))
    # Modificar anchos de bordes y tamaño de nodos
    anchos = [100 * float(i) / max(anchos) for i in anchos]
    anchos = [x ** 2.35 * escalar_borde ** 2 for x in anchos]
    sizes = [30 + (escalar_nodo * float(i) / max(sizes)) for i in sizes]
    # Eliminar las conexiones con menor peso para aclarar un poco la imagen
    anchos = [
        i if i >= np.percentile(anchos, prop_fuera) else 0 for i in anchos
    ]
    # Crear grafo
    G = nx.Graph()
    for i in sorted(lista_nodos):
        G.add_node(i[0], size=1)
    G.add_weighted_edges_from(lista_bordes)
    # Crear la gráfica
    fig = plt.figure(figsize=dim_figura)
    ax = plt.axes()
    try:
        if circular:
            pos = nx.circular_layout(G)
        else:
            pos = pos = nx.spring_layout(G, iterations=300, k=K, seed=123)
    except BaseException:
        if circular:
            pos = nx.circular_layout(G)
        else:
            pos = pos = nx.spring_layout(G, iterations=300, k=K)
    # Obtener número de nodos
    n = G.number_of_nodes()
    # Número máximo de conexiones entre nodos
    max_con = max([list(G.degree())[i][1] for i in range(n)])
    # Definir los colores
    colores = [
        plt.cm.plasma(list(G.degree())[i][1] / max_con) for i in range(n)
    ]
    # Definir la cantidad de conexiones por nodos
    grados = np.array([list(G.degree())[i][1] for i in range(n)])
    # Definir la paleta de colores
    cmap = plt.get_cmap("plasma", len(grados))
    # Escribir los nombres de los nodos
    for key, value in pos.items():
        x, y = value[0] + 0, value[1] - offset_y
        plt.text(x, y, s=key, horizontalalignment="center", fontsize=10)
    for key, value in pos.items():
        xi = value[0]
        yi = value[1]
        ax.scatter(
            xi,
            yi,
            color=colores[list(G.nodes()).index(key)],
            s=350,
            edgecolors="k",
            alpha=0.7,
            cmap=cmap,
        )
    bounds = np.linspace(
        min(grados), max(grados), max(grados) - min(grados) + 1
    )
    norm = cl.BoundaryNorm(bounds, cmap.N)
    ax2 = fig.add_axes([0.90, 0.1, 0.03, 0.8])
    plt.text(
        x=1.5,
        y=-0.2,
        s="No de conecciones",
        horizontalalignment="center",
        fontsize=10,
        color="black",
        rotation=-90,
    )
    try:
        mpl.colorbar.ColorbarBase(
            ax2,
            cmap=cmap,
            norm=norm,
            spacing="proportional",
            ticks=bounds,
            boundaries=bounds,
            format="%1i",
        )
    except:
        pass
    # Hacer un bucle en la lista de aristas para obtener las coordenadas
    # x, y de los nodos conectados
    # Esos dos puntos son los extremos de la línea que se trazará.
    for i, j in enumerate(G.edges()):
        x = np.array((pos[j[0]][0], pos[j[1]][0]))
        y = np.array((pos[j[0]][1], pos[j[1]][1]))
        ax.plot(x, y, c="black", alpha=0.5, linewidth=anchos[i])
    ax.set_axis_off()
    if ubicacion_archivo is not None:
        plt.savefig(ubicacion_archivo)
    if graficar:
        plt.show()
    if devolver_grafica:
        return plt
    # Cerrar gráfica
    plt.close()


def grafica_barchart_frecuencias(
    texto,
    n_grama=1,
    dim_figura=(8, 5),
    titulo="Términos más frecuentes",
    ascendente=True,
    ubicacion_archivo=None,
    graficar=True,
    n_terminos=15,
    devolver_grafica=False,
):
    """
    Permite graficar o exportar un gráfico de barras horizontales de la \
    frecuencia de palabras o n-gramas a partir de un texto.

    :param texto: Corresponde al texto que se desea analizar.
    :type texto: str
    :param n_grama: Cantidad de elementos a tener en cuenta en la generación \
        de n-gramas. Valor por defecto `1`.
    :type n_grama: int, opcional
    :param dim_figura: Corresponden al ancho y alto de la figura en pulgadas. \
        Valor por defecto `(8, 5)`.
    :type dim_figura: (float, float), opcional
    :param titulo: Título de la nube de palabras. Valor por defecto \
        `'Términos más frecuentes'`.
    :type titulo: str, opcional
    :param ascendente: Determina si las barras de términos se muestran de \
        menos (abajo) a más (arriba) frecuentes en la gráfica. \
        Valor por defecto `True`.
    :type ascendente: bool, opcional
    :param ubicacion_archivo: Ruta donde desea exportar la gráfica como \
        archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la \
        extensión `jpg`. Si `ubicacion_archivo = None` la gráfica no se \
        exporta. Valor por defecto `None`.
    :type ubicacion_archivo: str, opcional
    :param graficar: Permite visualizar la gráfica. Valor por defecto `True`.
    :type graficar: bool, opcional
    :param n_terminos:Cantidad de n-gramas que se incluyen en la gráfica. \
        Se graficarán los `n_terminos` más frecuentes en el texto. \
        Valor por defecto `15`.
    :type n_terminos: int, opcional
    :param devolver_grafica: Indica si se desea obtener el gráfico de \
        barras como un objeto de `Matplotlib`. \
        Valor por defecto `False`.
    :type devolver_grafica: bool, opcional
    :return: (Matplotlib.Figure) Figura con el gráfico de barras, \
        solo si `devolver_grafica = True`.
    """
    dict_datos = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Ordenar datos en un dataframe
    df = pd.DataFrame.from_dict(dict_datos, orient="index")
    df = df.reset_index()
    df.columns = ["n_grama", "frecuencia"]
    df = df.sort_values(by="frecuencia", ascending=ascendente)
    # Crear gráfica
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=dim_figura)
    y_pos = np.arange(len(df["frecuencia"]))
    ax.barh(y_pos, df["frecuencia"], align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["n_grama"])
    if titulo != "":
        ax.set_title(titulo)
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel("Término")
    plt.tight_layout()
    #
    for i, v in enumerate(df["frecuencia"]):
        ax.text(v, i, v, fontsize=10, verticalalignment="center")
    # Si se dio una ubicación, se guarda ahí la figura
    if ubicacion_archivo != "":
        plt.savefig(ubicacion_archivo)
    if graficar:
        plt.show()
    if devolver_grafica:
        return fig
    # Cerrar gráfica
    plt.close()


def graficar_dispersion(
    documentos,
    palabras_clave,
    ignorar_mayus=True,
    titulo="Gráfico de dispersión de términos",
    eje_x="Distribución de términos",
    eje_y="Palabras clave",
    etiquetas=None,
    auto_etiquetas=True,
    leyenda=True,
    rotacion=30,
    dim_figura=(12, 7),
    ubicacion_archivo=None,
    graficar=True,
    marcador="|",
    tam_marcador=20,
    ancho_marcador=3,
    colores=None,
    mapa_color="nipy_spectral",
    devolver_grafica=False,
):
    """
    Permite generar un gráfico de dispersión de términos de interés a lo \
    largo de uno o varios documentos.

    :param documentos: Texto del documento o lista de textos de \
        documentos sobre los cuales se quiere analizar la dispersión de \
        términos. Si desea generar la dispersión con n-gramas, cada texto \
        debe ser representado como lista de n-gramas. 
    :type documentos: str, list
    :param palabras_clave: Lista de palabras clave, n-gramas claves \
        o término de interés\
        que se quieren encontrar en los textos de los documentos.
    :type palabras_clave: list
    :param ignorar_mayus: Si `ignorar_mayus = True`, no hace diferencia \
        si las palabras tienen mayúsculas, es decir, \
        ConTexto es igual a contexto. Valor por defecto `True`.
    :type ignorar_mayus: bool, opcional
    :param titulo: Título de la figura de dispersión de términos. Valor por \
        defecto `'Gráfico de dispersión de términos'`.
    :type titulo: str, opcional
    :param eje_x: Leyenda del eje `x` de la figura. Valor por defecto \
        `'Distribución de términos'`.
    type eje_x: str, opcional
    :param eje_y: Leyenda del eje `y` de la figura. Valor por defecto \
        `'Palabras clave'`.
    :type eje_y: str, opcional
    :param etiquetas: Lista de identificadores de los documentos analizados. \
        Esta debe ser de la misma longitud de la lista de documentos de \
        entrada. Si `etiquetas = None` y `auto_etiquetas = True`, se generan \
        etiquetas automáticas. Valor por defecto `None`.
    :type etiquetas: str, opcional
    :param auto_etiquetas: Si `etiquetas = None`, Genera etiquetas \
        automáticas para los documentos de entrada de tipo {doc1, doc2, ..., \
        docn}. Valor por defecto `True`.
    :type auto_etiquetas: bool, opcional
    :param leyenda:  Permite mostrar los identificadores de los documentos \
        al lado derecho de la gráfica. Valor por defecto `True`.
    :type leyenda: bool, opcional
    :param rotacion: Permite rotar las etiquetas de los documentos sobre el \
        eje `x` de la gráfica de dispersión. Valor por defecto `30`.
    :type rotacion: int, opcional
    :param dim_figura: Corresponden al ancho y alto de la figura en pulgadas. \
        Valor por defecto `(12, 7)`.
    :type dim_figura: (float, float), opcional
    :param ubicacion_archivo: Ruta donde desea exportar la gráfica como \
        archivo tipo imagen {png, jpeg, jpg, gif}. Si \
        `ubicacion_archivo = None`, la gráfica no se exporta. Valor por \
        defecto `None`.
    :type ubicacion_archivo: str, opcional
    :param graficar: Permite visualizar la gráfica después de ejecutar la \
        función. Valor por defecto `True`.
    :type graficar: bool, opcional
    :param marcador: Tipo de marcador utilizado por el gráfico de dispersión. \
        Se acepta los marcadores disponibles para Matplotlib \
        (https://matplotlib.org/stable/api/markers_api.html). \
        Valor por defecto `'|'`.
    :type marcador: str, opcional
    :param tam_marcador: Tamaño del marcador en el gráfico de dispersión. \
        Para un gráfico con muchas palabras clave, \
        se recomienda poner un valor menor. Valor por defecto `20`.
    :type tam_marcador: float, opcional
    :param ancho_marcador: Ancho del marcador en el gráfico de dispersión. \
        Para un gráfico con muchos documentos, se recomienda utilizar un \
            número menor. Valor por defecto `3`.
    :type ancho_marcador: float, opcional
    :param colores:  Lista de colores para identificar cada documento de \
        entrada. Si `colores = None`, se generan colores automáticos para \
        cada documento dependiendo del `'mapa_color'` seleccionado. \
        Valor por defecto `None`.
    :type colores: list, opcional
    :param mapa_color: Mapa de color para generar colores automáticos para \
        los documentos. Se aceptan todos los mapas de color continuos de \
        `Matplotlib`: \
        (https://matplotlib.org/stable/tutorials/colors/colormaps.html). \
        Valor por defecto: 'nipy_spectral'.
    :type mapa_color: str, opcional
    :param devolver_grafica:  Si `devolver_grafica = True`, devuelve el \
        gráfico de dispersión como objeto de `Matplotlib`. \
        Valor por defecto `False`.
    :return: (Matplotlib.Figure) Objeto de Matplotlib, solo si \
        `devolver_grafica = True`.
    """

    # Llamar objecto de dispersionPlot
    visualizador = dispersionPlot(
        documentos,
        palabras_clave,
        ignorar_mayus,
        titulo,
        eje_x,
        eje_y,
        etiquetas,
        auto_etiquetas,
        dim_figura,
        marcador,
        tam_marcador,
        ancho_marcador,
        colores,
        mapa_color,
        leyenda,
        rotacion,
        graficar,
        ubicacion_archivo,
        devolver_grafica,
    )

    if devolver_grafica:
        fig = visualizador.graficar()
        return fig
    else:
        visualizador.graficar()
