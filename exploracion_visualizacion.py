import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from collections import Counter, Iterable
from wordcloud import WordCloud

# Función para generar n-gramas a partir de un texto


def obtener_ngramas(texto, n=1, devolver_lista=True):
    lista = texto.split(' ')
    n_gramas = (' '.join(lista[i:i + n])
                for i in range(len(lista)) if i + n <= len(lista))
    if devolver_lista:
        n_gramas = list(n_gramas)
    return n_gramas


def frecuencia_ngramas(texto, n_grama=1, n_max=None):
    lista = obtener_ngramas(texto, n_grama)
    cont = Counter(lista)
    if n_max is not None:
        dictu = dict(cont.most_common(n_max))
    else:
        dictu = dict(cont)
    return dictu

# Función para crear y graficar/guardar una nube de palabras


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

# Función para graficar o guardar una nube de palabras


def grafica_nube(
        nube,
        dim_figura=(10, 10),
        titulo='Términos más frecuentes',
        ubicacion_archivo='',
        graficar=True):
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

# Grafica un par de nubes de palabras, una junto a otra


def par_nubes(texto, n1=1, n2=2, dim_figura=(20, 11), ubicacion_archivo='', graficar=True):
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
    # Cerrar gráfica
    plt.close()

# Función que calcula matriz de co-ocurrencias de un texto


def matriz_coocurrencias(
        texto,
        min_frec=1,
        max_num=200,
        modo='documento',
        ventana=3,
        tri_sup=True):
    """
    texto: Un solo texto o un conjunto de documentos
    min_frec: Mínima frecuencia de aparición de palabras
    max_num: Máximo número de palabras a dejar en la matriz (se cogen las más frecuentes)
    ventana: Tamaño de la ventana (solo se usa cuando modo='ventana')
    modo: Modo de análisis (documento o ventana)
    """
    # Generar un solo texto con todos los documentos
    if isinstance(texto, Iterable) and not isinstance(texto, str):
        texto_entero = ' '.join([str(i) for i in texto])
    else:
        texto_entero = str(texto)
        texto = [texto_entero]  # Convertir variable "texto" en un iterable
    # Generar lista de palabras en todos los textos juntos
    palabras = texto_entero.split()
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
            palabras_t = t.split()
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
            cuenta_t = dict(Counter(t.split()))
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

# Función que acepta una data frame y devuelve la versión diagonal
# superior de la misma


def diag_superior(df):
    return pd.DataFrame(np.triu(df), index=df.index, columns=df.columns)

# Función que grafica la matriz de co-ocurrencias como un grafo no dirigido


def graficar_coocurrencias(
    mat,
    tipo=None,
    prop_fuera=0,
    ubicacion_archivo='',
    graficar=True,
    K=5,
    color_borde='orchid',
    color_nodo='silver',
    semilla=123,
    dim_figura=(13, 13)):
    # Detectar tipo de matriz de co-ocurrencias
    if tipo is None:
        tipo = 'ventana' if mat.sum().sum() == np.sum(np.triu(mat)) else 'documento'
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
        plt.savefig(ubicacion_archivo)  # save as png
    if graficar:
        plt.show()
    # Cerrar gráfica
    plt.close()

# los datos corresponden a un string para analizar


def grafica_barchart_frecuencias(
        texto,
        n_grama=1,
        figsize=(8, 5),
        titulo='',
        ascendente=True,
        ubicacion_archivo='',
        graficar=True,
        n_terminos=15):

    dict_datos = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Ordenar datos en un dataframe
    df = pd.DataFrame.from_dict(dict_datos, orient='index')
    df = df.reset_index()
    df.columns = ['n_grama', 'frecuencia']
    df = df.sort_values(by='frecuencia', ascending=ascendente)
    # Crear gráfica
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=figsize)
    y_pos = np.arange(n_terminos)
    ax.barh(y_pos, df['frecuencia'], align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['n_grama'])
    if titulo != '':
        ax.set_title(titulo)
    ax.set_xlabel('Frecuencia')
    ax.set_ylabel('Término')
    plt.tight_layout()

    for i, v in enumerate(df['frecuencia']):
        ax.text(v, i, v, fontsize=10, verticalalignment="center")

    if ubicacion_archivo != '':
        plt.savefig(ubicacion_archivo)  # save as png
    if graficar:
        plt.show()
    # Cerrar gráfica
    plt.close()
