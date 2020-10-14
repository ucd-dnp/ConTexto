import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from collections import Counter, Iterable
from wordcloud import WordCloud
from limpieza import limpieza_basica
from utils.tokenizacion import tokenizar, TokenizadorNLTK, TokenizadorEspacios


def obtener_ngramas(texto, n=1, devolver_lista=True, limpiar=False, tokenizador=None):
    """ Permite generar n-gramas a partir de un texto.

    :param texto: (str) Corresponde al texto que se desea analizar.
    :param n: (int) Cantidad de elementos a tener en cuenta en la generación de n-gramas. Por ejemplo, si n=1 se retornarán palabras, y si n=2 se retornarán bigramas.
    :param devolver_lista: (bool) {True, False} valor por defecto: True. Si el valor es True se retorna un objeto tipo lista; si el valor es False se retorna un objeto tipo generador.
    :param limpiar: (bool) {True, False}. Valor por defecto: False. Define \
        si se desea hacer una limpieza básica (aplicando la función  \
        `limpieza_basica` del módulo `limpieza`) al texto de entrada, antes de encontrar los n-gramas.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una instancia de la clase *TokenizadorNLTK*.        
    :return: n-gramas generados con las características especificadas.
    """
    if limpiar:
        texto = limpieza_basica(texto)
    lista = tokenizar(texto, tokenizador)
    n_gramas = (' '.join(lista[i:i + n])
                for i in range(len(lista)) if i + n <= len(lista))
    if devolver_lista:
        n_gramas = list(n_gramas)
    return n_gramas


def frecuencia_ngramas(texto, n_grama=1, n_max=None):
    """ Genera un diccionario con los n-gramas y sus respectivas frecuencias de ocurrencia en el texto.

    :param texto: (str) Corresponde al texto que se desea analizar.
    :param n_grama: (int) valor por defecto: 1. Cantidad de elementos a tener en cuenta en la generación de n-gramas.
    :param n_max: (int) valor por defecto: None. Cantidad máxima de n-gramas a generar.
    :return: diccionario de n-gramas más frecuentes.
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
        titulo='Términos más frecuentes',
        ubicacion_archivo='',
        mask=None,
        semilla=1234,
        devolver_nube=False):
    """ Permite graficar o exportar una nube de palabras (n-gramas) a partir de un texto.

    :param texto: (str) Corresponde al texto que se desea analizar.
    :param n_grama: (int) valor por defecto: 1. Cantidad de elementos a tener en cuenta en la generación de n-gramas.
    :param n_terminos: (int) valor por defecto: 100. Cantidad de n-gramas a graficar.
    :param graficar: (bool) {True, False} valor por defecto: True. Permite visualizar la gráfica en el `IDE`_ que esté utilizando.
    :param dim_figura: (float, float) valor por defecto: (10, 10). Corresponden al ancho y alto de la figura en pulgadas.
    :param hor: (float) (valor de 0 a 1). Corresponde a la orientación de las palabras en el gráfico, siendo 0 una distribución vertical, 1 una distribución horizontal y una distribución mixta a cualquier valor entre 0 y 1.
    :param titulo: (str) valor por defecto: 'Términos más frecuentes'. Corresponde al título de la nube de palabras.
    :param ubicacion_archivo: (str) valor por defecto: vacío. Ruta donde desea exportar la gráfica como archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la extensión jpg. Si no se especifica una ruta, la gráfica no se exporta.
    :param mask: (array) o None, valor por defecto: None. Correspondiente a la máscara base donde se dibujan las palabras, por defecto se utiliza una máscara circular.
    :param semilla: (int) valor por defecto: 1234. Corresponde al estado inicial del generador, este incide en la posición y color de las palabras. En caso de querer replicar la nube de palabras, se recomienda utilizar un mismo valor de semilla.
    :param devolver_nube: (bool) {True, False} valor por defecto: False. Indica si desea obtener la nube de palabras como un objeto tipo WordCloud.
    :return: objeto tipo WordCloud, solo si devolver_nube=True.
    """

    # Obtener diccionario de 'n_terminos' más frecuentes con sus frecuencias
    dictu = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Por defecto se crea una máscara circular para ordenar la nube
    if mask is None:
        x, y = np.ogrid[:600, :600]
        mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
        mask = 255 * mask.astype(int)
    nube = WordCloud(background_color='white',
                       prefer_horizontal=hor, mask=mask, random_state=semilla)
    figura = nube.generate_from_frequencies(dictu)
    # Devolver el objeto de la nube, para graficarlo de otra manera
    if devolver_nube:
        return figura
    else:
        # Graficar y/o guardar la imagen generada
        grafica_nube(figura, dim_figura, titulo, ubicacion_archivo, graficar)


def grafica_nube(
        nube,
        dim_figura=(10, 10),
        titulo='Términos más frecuentes',
        ubicacion_archivo='',
        graficar=True):
    """ Permite graficar o guardar una nube de palabras.

    :param nube: (WordCloud) Objeto tipo WordCloud correspondiente a la nube de palabras.
    :param dim_figura: (float, float) valor por defecto: (10, 10). Corresponden al ancho y alto de la figura en pulgadas.
    :param titulo: (str) valor por defecto: 'Términos más frecuentes'. Corresponde al título de la nube de palabras.
    :param ubicacion_archivo: (str) valor por defecto: ''. Ruta donde desea exportar la gráfica como archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la extensión jpg. Si no se especifica una ruta, la gráfica no se exporta.
    :param graficar: (bool) {True, False} valor por defecto: True. Permite visualizar la gráfica en el `IDE`_ que esté utilizando.
    """

    fig = plt.figure(figsize=dim_figura)
    plt.imshow(nube, interpolation='bilinear')
    if titulo != '':
        plt.title(titulo)
    plt.axis("off")
    if graficar:
        plt.show()
    if ubicacion_archivo != '':
        fig.savefig(ubicacion_archivo)
    # Cerrar gráfica
    plt.close()


def par_nubes(texto, n1=1, n2=2, dim_figura=(20, 11), ubicacion_archivo='', 
            graficar=True, devolver_grafica=False):
    """ Permite graficar o exportar un par de nubes de palabras (una junto a otra) a partir de un texto.

    :param texto: (str) Corresponde al texto que se desea analizar.
    :param n1: (int) valor por defecto: 1. Cantidad de elementos a tener en cuenta en la generación de n-gramas de la nube de palabras izquierda.
    :param n2: (int) valor por defecto: 2. Cantidad de elementos a tener en cuenta en la generación de n-gramas de la nube de palabras derecha.
    :param dim_figura: (float, float) valor por defecto: (20, 10). Corresponden al ancho y alto de la figura en pulgadas.
    :param ubicacion_archivo: (str) valor por defecto: ''. Ruta donde desea exportar la gráfica como archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la extensión jpg. Si no se especifica una ruta, la gráfica no se exporta.
    :param graficar: (bool) {True, False} valor por defecto: True. Permite visualizar la gráfica en el `IDE`_ que esté utilizando.
    :param devolver_grafica: (bool) {True, False} valor por defecto: False. Indica si se desea obtener \
        el gráfico con el par de nubes de palabras como un objeto de Matplotlib.
    :return: Figura (objeto Figure de Matplotlib) con el par de nubes de palabras, solo si devolver_grafica=True.    
    """

    # Obtener nubes de palabras
    nube_1 = nube_palabras(texto, n_grama=n1, hor=0.8, devolver_nube=True)
    nube_2 = nube_palabras(texto, n_grama=n2, hor=1, devolver_nube=True)

    # Graficar nubes y mostrarlas
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=dim_figura, 
                                    gridspec_kw={'hspace': 0, 'wspace': 0})

    ax1.imshow(nube_1, interpolation='bilinear')
    tit = 'términos' if n1 == 1 else f"n_gramas ({n1})"
    ax1.set_title(f'Nube de palabras: {tit}', size=18)

    ax2.imshow(nube_2, interpolation='bilinear')
    tit = 'términos' if n2 == 1 else f"n_gramas ({n2})"
    ax2.set_title(f'Nube de palabras: {tit}', size=18)

    fig.suptitle('Términos más frecuentes', size=28, y=0.99)
    plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
    if graficar:
        plt.show()
    if ubicacion_archivo != '':
        fig.savefig(ubicacion_archivo)
    if devolver_grafica:
        return fig
    # Cerrar gráfica
    plt.close()


def matriz_coocurrencias(
        texto,
        min_frec=1,
        max_num=200,
        modo='documento', 
        ventana=3,
        tri_sup=True,
        limpiar=False,
        tokenizador=None):
    """ Calcula la matriz de co-ocurrencias de un texto.

    :param texto: (str o list) Corresponde al texto (o lista de textos/documentos) que se desea analizar.
    :param min_frec: (int) valor por defecto: 1. Frecuencia mínima de aparición de palabras, si la frecuencia de una palabra es menor a min_frec, dicha palabra es excluida de la matriz.
    :param max_num: (int) valor por defecto: 200. Número máximo de palabras a dejar en la matriz (se eligen las más frecuentes).
    :param modo: (str) {'documento', 'ventana'} valor por defecto: 'documento'. Corresponde al modo de análisis, con 'documento' se calcula la co-ocurrencia de términos sin importar la distancia entre estos,  con 'ventana' se calcula la co-ocurrencia de términos teniendo en cuenta una distancia máxima entre estos.
    :param ventana: (int) valor por defecto: 3. Tamaño de la ventana (solo se usa cuando modo='ventana'). Número de palabras anteriores o posteriores a tener en cuenta con respecto al término de análisis, equivalente a calcular la co-ocurrencia con n-gramas, siendo n=ventana+1.
    :param tri_sup: (bool) {True, False} valor por defecto: True. Si el valor es True devuelve la versión diagonal superior de la matriz de co-ocurrencias, si es False devuelve la matriz completa.
    :param limpiar: (bool) {True, False}. Valor por defecto: False. Define \
        si se desea hacer una limpieza básica (aplicando la función `limpieza_basica` \
        del módulo `limpieza`) al texto de entrada, antes de calcular las co-ocurrencias.
    :param tokenizador: Valor por defecto: None. Objeto encargado de la tokenización y detokenización \
        de textos. Si el valor es 'None', se utilizará por defecto una instancia de la clase *TokenizadorNLTK*.        
    :return: dataframe de pandas con las co-ocurrencias de los textos de entrada.
    """
    # Generar un solo texto con todos los documentos
    if isinstance(texto, Iterable) and not isinstance(texto, str):
        texto_entero = ' '.join([str(i) for i in texto])
    else:
        texto_entero = str(texto)
        texto = [texto_entero]  # Convertir variable "texto" en un iterable
    
    if limpiar:
        texto = [limpieza_basica(t) for t in texto]
        texto_entero = ' '.join([texto])
    # Se inicializa un solo tokenizador, para ahorrar un poco de tiempo
    tok = TokenizadorNLTK() if tokenizador is None else tokenizador
    # Generar lista de palabras en todos los textos juntos
    palabras = tokenizar(texto_entero, tok)
    # Dejar solo las palabras con mayor frecuencia y/o que cumplan una
    # frecuencia mínima
    cuenta = dict(Counter(palabras).most_common(max_num))
    cuenta_filt = {k: v for k, v in cuenta.items() if v >= min_frec}
    nombres = list(set(cuenta_filt.keys()))
    # Inicializar en ceros la matriz de co-ocurrencias
    mat_oc = pd.DataFrame(
        np.zeros([len(nombres), len(nombres)]), columns=nombres, index=nombres)
    if modo == 'ventana':
        for t in texto:
            palabras_t = tokenizar(t, tok)
            # Ciclo a través de las palabras para obtener las co-ocurrencias:
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
    elif modo == 'documento':
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
    """ Función que acepta una dataframe y devuelve la versión diagonal superior de la misma.

    :param df: (dataframe) dataset de insumo.
    :return: dataframe transformado.
    """
    return pd.DataFrame(np.triu(df), index=df.index, columns=df.columns)


def graficar_coocurrencias(
    mat,
    prop_fuera=0,
    ubicacion_archivo='',
    graficar=True,
    K=5,
    color_borde='orchid',
    color_nodo='silver',
    semilla=123,
    dim_figura=(13, 13)):
    """ Grafica una matriz de co-ocurrencias de términos como un grafo no dirigido.

    :param mat: (dataframe) Matriz de co-ocurrencias que desea graficar.
    :param prop_fuera: (float) (valor entre 0 y 100). Permite eliminar las conexiones con menor peso para aclarar un poco la imagen.
    :param ubicacion_archivo: (str) valor por defecto: ''. Ruta donde desea exportar la gráfica como archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la extensión jpg. Si no se especifica una ruta, la gráfica no se exporta.
    :param graficar: (bool) {True, False} valor por defecto: True. Permite visualizar la gráfica en el `IDE`_ que esté utilizando.
    :param K: (float) valor por defecto: 5. Distancia óptima entre nodos, aumente este valor para separar los nodos. 
    :param color_borde: (str) valor por defecto: 'orchid'. Corresponde al color de los bordes de la red, se puede asignar el nombre de un color predefinido o el código hexadecimal de un color.
    :param color_nodo: (str) valor por defecto: 'silver'. Corresponde al color de los nodos, se puede asignar el nombre de un color predefinido o el código hexadecimal de un color.
    :param semilla: (int) valor por defecto: 123. Estado inicial del generador aleatorio para establecer la posición de los nodos.
    :param dim_figura: (float, float) valor por defecto: (13, 13). Corresponden al ancho y alto de la figura en pulgadas.    
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
    anchos = [x**2.35 * escalar_borde**2 for x in anchos]
    sizes = [30 + (escalar_nodo * float(i) / max(sizes)) for i in sizes]
    # Eliminar las conexiones con menor peso para aclarar un poco la imagen
    anchos = [i if i >= np.percentile(
        anchos, prop_fuera) else 0 for i in anchos]
    # Crear grafo
    G = nx.Graph()
    for i in sorted(lista_nodos):
        G.add_node(i[0], size=1)
    G.add_weighted_edges_from(lista_bordes)
    # Crear la gráfica
    plt.subplots(figsize=dim_figura)
    try:
        pos = nx.spring_layout(G, iterations=300, k=K, seed=semilla)
    except BaseException:
        pos = nx.spring_layout(G, iterations=300, k=K)
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=sizes,
        width=anchos,
        edge_color=color_borde,
        node_color=color_nodo)
    # Escribir los nombres de los nodos
    for key, value in pos.items():
        x, y = value[0] + 0, value[1] - offset_y
        plt.text(x, y, s=key, horizontalalignment='center', fontsize=10)
    plt.axis('off')
    if ubicacion_archivo != '':
        plt.savefig(ubicacion_archivo)
    if graficar:
        plt.show()
    # Cerrar gráfica
    plt.close()


def grafica_barchart_frecuencias(
        texto,
        n_grama=1,
        dim_figura=(8, 5),
        titulo='Términos más frecuentes',
        ascendente=True,
        ubicacion_archivo='',
        graficar=True,
        n_terminos=15,
        devolver_grafica=False):
    """ Permite graficar o exportar un gráfico de barras horizontales de la frecuencia de palabras (n-gramas) a partir de un texto.

    :param texto: (str) Corresponde al texto que se desea analizar.
    :param n_grama: (int) valor por defecto: 1. Cantidad de elementos a tener en cuenta en la generación de n-gramas.
    :param dim_figura: (float, float) valor por defecto: (8, 5). Corresponden al ancho y alto de la figura en pulgadas.
    :param titulo: (str) valor por defecto: 'Términos más frecuentes'. Corresponde al título de la nube de palabras.
    :param ascendente: (bool) {True, False} valor por defecto: True. Determina si las barras de términos se muestran de menos (abajo) a más (arriba) frecuentes en la gráfica.
    :param ubicacion_archivo: (str) valor por defecto: vacío (''). Ruta donde desea exportar la gráfica como archivo tipo imagen. Al nombrar el archivo se recomienda utilizar la extensión jpg. Si no se especifica una ruta, la gráfica no se exporta.
    :param graficar: (bool) {True, False} valor por defecto: True. Permite visualizar la gráfica en el `IDE`_ que esté utilizando.
    :param n_terminos: (int) valor por defecto: 15. Cantidad de n-gramas a graficar.
    :param devolver_grafica: (bool) {True, False} valor por defecto: False. Indica si se desea obtener \
        el gráfico de barras como un objeto de Matplotlib.
    :return: Figura (objeto Figure de Matplotlib) con el gráfico de barras, solo si devolver_grafica=True.    
    """
    dict_datos = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Ordenar datos en un dataframe
    df = pd.DataFrame.from_dict(dict_datos, orient='index')
    df = df.reset_index()
    df.columns = ['n_grama', 'frecuencia']
    df = df.sort_values(by='frecuencia', ascending=ascendente)
    # Crear gráfica
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=dim_figura)    
    y_pos = np.arange(len(df['frecuencia']))
    ax.barh(y_pos, df['frecuencia'], align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['n_grama'])
    if titulo != '':
        ax.set_title(titulo)
    ax.set_xlabel('Frecuencia')
    ax.set_ylabel('Término')
    plt.tight_layout()
    #
    for i, v in enumerate(df['frecuencia']):
        ax.text(v, i, v, fontsize=10, verticalalignment="center")
    # Si se dio una ubicación, se guarda ahí la figura
    if ubicacion_archivo != '':
        plt.savefig(ubicacion_archivo)
    if graficar:
        plt.show()
    if devolver_grafica:
        return fig
    # Cerrar gráfica
    plt.close()
