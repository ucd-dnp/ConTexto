import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

# Función para generar n-gramas a partir de un texto
def obtener_ngramas(texto, n=1, devolver_lista=True):
    lista = texto.split(' ')
    n_gramas = (' '.join(lista[i:i+n]) for i in range(len(lista)) if i + n <= len(lista))
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
def nube_palabras(texto, n_grama=1, n_terminos=100, plot=True, figsize=(10,10), hor=0.6,
                  titulo='Términos más frecuentes',archivo='',mask=None, semilla=1234):
    # Obtener diccionario de 'n_terminos' más frecuentes con sus frecuencias
    dictu = frecuencia_ngramas(texto, n_grama, n_terminos)
    # Crear máscara (circular) para ordenar la nube
    if mask is None:
        x, y = np.ogrid[:600, :600]
        mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
        mask = 255 * mask.astype(int)
    wordcl = WordCloud(background_color = 'white',prefer_horizontal=hor, mask=mask,random_state=semilla)
    figura = wordcl.generate_from_frequencies(dictu)
    # Graficar y/o guardar la imagen generada
    grafica_nube(figura, figsize, titulo, archivo, plot)

# Función para graficar o guardar una nube de palabras
def grafica_nube(nube, figsize=(10,10), titulo='Términos más frecuentes', archivo='', plot=True):
    fig = plt.figure(figsize=figsize)
    if titulo != '':
        plt.title(titulo)
    plt.axis("off")
    if plot:
        plt.imshow(nube, interpolation='bilinear')
        plt.show()
    if archivo != '':
        fig.savefig(archivo)
    # Cerrar gráfica
    plt.close()
    
# Función que calcula matriz de co-ocurrencias de un texto
def matriz_coocurrencias(texto, min_freq=1, max_num=100, modo='documento', ventana=3, triu=True):
    """
    min_freq: Mínima frecuencia de aparición de palabras
    max_num: Máximo número de palabras a dejar en la matriz (se cogen las más frecuentes)
    ventana: Tamaño de la ventana (solo se usa cuando modo='ventana')
    modo: Modo de análisis (documento o ventana)
    """
    # Generar lista de palabras
    palabras = texto.split()
    # Dejar solo las palabras con mayor frecuencia y/o que cumplan una frecuencia mínima
    cuenta = dict(Counter(palabras).most_common(max_num))
    cuenta_filt = {k: v for k, v in cuenta.items() if v >= min_freq}
    names = list(cuenta_filt.keys())
    # Inicializar en ceros la matriz de co-ocurrencias
    mat_oc = pd.DataFrame(np.zeros([len(names),len(names)]),columns=names, index=names)
    # Ciclo a través de las palabras para obtener las co-ocurrencias:
    for i, palabra in enumerate(palabras):
        if modo == 'ventana':
            inicio = max(0, i - ventana)
            fin = min(len(palabras), i + ventana + 1)
            for j, item in enumerate(palabras[inicio:fin]):
                if (item in mat_oc.columns) and (palabra in mat_oc.columns):
                    if palabra != item:
                        mat_oc[item][palabra] += 1
                    else:
                        if (inicio + j) != i:
                            mat_oc[item][palabra] += 1
        else:
            if palabra not in names:
                continue
            for item in names:
                if palabra != item:
                    mat_oc[item][palabra] = cuenta_filt[palabra] * cuenta_filt[item]
                else:
                    if mat_oc[item][palabra] == 0: 
                        mat_oc[item][palabra] = cuenta_filt[palabra]
    # Ordenar filas y columnas alfabeticamente
    mat_oc.sort_index(inplace=True)
    mat_oc = mat_oc.reindex(sorted(mat_oc.columns), axis=1)
    if triu:
        mat_oc = diag_superior(mat_oc)

    return mat_oc

# Función que acepta una data frame y devuelve la versión diagonal superior de la misma
def diag_superior(df):
    return pd.DataFrame(np.triu(df), index=df.index, columns=df.columns)

# Función que grafica la matriz de co-ocurrencias como un grafo no dirigido
def graficar_coocurrencias(mat, tipo=None, prop_fuera=0, archivo='', plot=True, K=5,
                           col_borde='orchid', col_nodo='silver', semilla=123, figsize=(13,13)):
    # Detectar tipo de matriz de co-ocurrencias
    if tipo is None:
        tipo = 'ventana' if any(np.diag(mat) == 0) else 'documento'
    # Definir el valor máximo de la matriz y de la diagonal
    max_cooc = max(mat.max())
    max_diag = max(np.diag(mat))
    # Definir lista de conexiones (edges)
    edge_list = []
    for index, row in mat.iterrows():
        i = 0
        for col in row:
            weight = float(col)/np.log10(max_cooc)
            edge_list.append((index, mat.columns[i], weight))
            i += 1
    # Quitar de la lista conexiones con peso 0 (no hay co-ocurrencia)
    edge_list = [x for x in edge_list if x[2] > 0.0]
    # Quitar conexiones de un nodo consigo mismo
    for i in edge_list:
        if i[0] == i[1]:
            edge_list.remove(i)
    # Definir lista de vértices (nodes)
    node_list = [[i,mat.loc[i,i] / np.log(max_diag)] for i in mat.columns]
    for i, node in enumerate(node_list):
        if node[1] == 0.0:
            node_list[i][1] += 0.1
    # Definir tamaños de nodos y bordes del grafo
    offset_y = 0.06
    node_scalar = 200
    edge_scalar = 0.0055
    sizes = [x[1] for x in node_list]
    widths = [x[2] for x in edge_list]
    # Acotar los tamaños en el percentil 99 para evitar valores demasiado altos
    widths = np.clip(widths, 0, np.percentile(widths,99))
    sizes = np.clip(sizes, 0, np.percentile(widths,99))
    # Modificar anchos de bordes y tamaño de nodos
    widths = [100 * float(i)/max(widths) for i in widths] 
    widths = [x**2.35 * edge_scalar**2 for x in widths]
    sizes = [30 + (node_scalar * float(i)/max(sizes)) for i in sizes] 
    # Eliminar las conexiones con menor peso para aclarar un poco la imagen
    widths = [i if i >= np.percentile(widths,prop_fuera) else 0 for i in widths]
    # Crear grafo
    G = nx.Graph()
    for i in sorted(node_list):
        G.add_node(i[0], size = 1)
    G.add_weighted_edges_from(edge_list)
    # Crear la gráfica
    plt.subplots(figsize=figsize)
    try:
        pos = nx.spring_layout(G, iterations=300, k=K, seed=semilla)
    except:
        pos = nx.spring_layout(G, iterations=300, k=K)
    nx.draw(G, pos, with_labels=False, node_size=sizes, width=widths, edge_color=col_borde,
            node_color=col_nodo)
    # Escribir los nombres de los nodos
    for key, value in pos.items():
        x, y = value[0] + 0, value[1] - offset_y
        plt.text(x, y, s=key, horizontalalignment='center', fontsize=10)
    plt.axis('off')
    if archivo != '':
        plt.savefig(archivo) # save as png
    if plot:
        plt.show()
    # Cerrar gráfica
    plt.close()