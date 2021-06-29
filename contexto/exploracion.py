import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as cl
import networkx as nx
from networkx.convert_matrix import from_pandas_adjacency
import numpy as np
import pandas as pd
import warnings
from collections import Counter, Iterable
from wordcloud import WordCloud, ImageColorGenerator
from limpieza import limpieza_basica
from utils.tokenizacion import tokenizar, TokenizadorNLTK


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
    :param n_terminos: Cantidad de n-gramas que se incluyen en la nube. \
        Se graficarán los `n_terminos` más frecuentes en \
        el texto. Valor por defecto `100`.
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
    ubicacion_archivo=None,
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
    if ubicacion_archivo is not None:
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
    vmin=10,
    vmax=None,
    escala=700,
    n_nodos=0,
    titulo="Gráfico de co-ocurrencias",
    dim_figura=(10, 6),
    node_cmap="RdPu",
    edge_cmap="Blues",
    offset_y=0.09,
    font_color="white",
    node_font_size=12,
    label_font_size=10,
    graficar=True,
    ubicacion_archivo=None,
    devolver_grafica=False,
    seed=12,
):
    """
    Grafica una matriz de coocurrencia como un grafo no dirigido de términos.

    :param mat: Matriz de coocurrencia de términos
    :type mat: pandas.DataFrame
    :param dim_figura: Corresponden al ancho y alto de la figura en pulgadas. \
        Valor por defecto `(10, 6)`.
    :type dim_figura: (float, float), opcional
    :param vmin: Tamaño mínimo de un nodo. Valor por defecto `10`.
    :type vmin: int, opcional
    :param vmax: Tamaño máximo de un nodo. Si  `vmax = None`, se escoge el \
        número máximo de grados de un nodo. Valor por defecto `None`.
    :type vmax: int, opcional
    :param n_nodos: Indica el número o porcentaje de nodos que se quieren \
        mostrar en el gráfico. Si `n_nodos = 0`, todos los nodos son \
        selecionados. Si `n_nodos` está entre `0` y `1`, representa \
        el porcentaje de nodos que se desean graficar. Si `n_nodos > 1`, \
        reresenta el número de nodos que se desean graficar. Valor por \
        defecto `0`.
    :type n_nodos: float,int, opcional
    :param escala: Valor de escala para aumentar o disminuir el tamaño del \
        gráfico en general. Valor por defecto `700`.
    :type escala: int, opcional
    :param node_cmap: Mapa de color para generar colores de los nodos dado \
        su número de conexiones. Se aceptan todos los mapas de color \
        continuos de `Matplotlib`: \
        (https://matplotlib.org/stable/tutorials/colors/colormaps.html). \
        Valor por defecto: "RdPu".
    :type node_cmap: str, opcional
    :param edge_cmap: Mapa de color para generar colores de las conexiones \
        dado su peso. Se aceptan todos los mapas de color continuos de \
        `Matplotlib`: \
        (https://matplotlib.org/stable/tutorials/colors/colormaps.html). \
        Valor por defecto: "Blues".
    :type edge_cmap: str, opcional
    :param offset_y: Desplazamiento hacia abajo (eje y) de los textos de los \
        nodos, para evitar el traslape con los nodos. Valor por defecto `0.09`.
    :type offset_y: float, opcional
    :param font_color: Color de la letra dentro de los nodos. El color puede \
        ser un string o una tupla (rgb) de floats de 0-1. Valor por defecto \
        `'white'`.
    :type font_color: str, array of colors, opcional
    :param node_font_size: Tamaño de letra dentro del nodo. Valor por \
        defecto `12`.
    :type node_font_size: int, opcional
    :param label_font_size: Tamaño de letra de las etiquetas de los nodos. \
        Valor por defecto `10`.
    :type label_font_size: int, opcional
    :param titulo: Título del gráfico de coocurrencias. Valor por defecto \
        `"Gráfico de co-ocurencias"`.
    :type titulo: str, opcional
    :param graficar: Permite visualizar la gráfica después de ejecutar la \
        función. Valor por defecto `True`.
    :type visualizar: bool, opcional
    :param ubicacion_archivo:  Ruta donde desea exportar la gráfica como \
        archivo tipo imagen {png, jpeg, jpg, gif}. Si \
        `ubicacion_archivo = None`, la gráfica no se exporta. Valor por \
        defecto `None`.
    :type ubicacion_archivo: str, opcional
    :param devolver_grafica: Indica si se desea obtener el gráfico de \
        coocurrencias como un objeto de `Matplotlib`. \
        Valor por defecto `False`.
    :param seed: Semilla para la generación del grafo. Sirve para cambiar la \
        distribución aleatoria de aparición de los nodos. Valor por \
        defecto `12`.
    :type seed: int, opcional
    :type devolver_grafica: bool, opcional
    :return: (Matplotlib.Figure) Figura con el gráfico de coocurrencias, \
        solo si `devolver_grafica = True`.
    """
    from contexto.utils import coocurrence_plot as cp

    ax = cp.graficar_coocurencia(
        mat,
        dim_figura=dim_figura,
        vmin=vmin,
        vmax=vmax,
        n_nodos=n_nodos,
        escala=escala,
        node_cmap=node_cmap,
        edge_cmap=edge_cmap,
        offset_y=offset_y,
        font_color=font_color,
        node_font_size=node_font_size,
        label_font_size=label_font_size,
        titulo=titulo,
        visualizar=graficar,
        ubicacion_archivo=ubicacion_archivo,
        devolver_grafica=devolver_grafica,
        seed=seed,
    )

    return ax


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
    :param n_terminos: Cantidad de n-gramas que se incluyen en la gráfica. \
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
    :type eje_x: str, opcional
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
    :param devolver_grafica: Si `devolver_grafica = True`, devuelve el \
        gráfico de dispersión como objeto de `Matplotlib`. \
        Valor por defecto `False`.
    :return: (Matplotlib.Figure) Objeto de Matplotlib, solo si \
        `devolver_grafica = True`.
    """
    from utils.dispersion_plot import dispersionPlot

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
