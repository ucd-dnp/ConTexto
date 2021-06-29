import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
import warnings


# Definir lista de vértices (nodes)
def normalize_size(size, vmin=10, vmax=40, scale=700):
    """
    Normaliza el tamaño del nodo para ser graficado

    :param size: Tamaño del nodo
    :type size: float
    :param vmin: Tamaño minimo del nodo, por defecto `10`.
    :type vmin: int, opcional
    :param vmax: Tamaño máximo del nodo, por defecto `40`.
    :type vmax: int, opcional
    :param scale: Escala de tamaño para los nodos, por defecto `700`.
    :type scale: int, opcional
    :return: (float) Retorna el tamaño del nodo, normalizado entre \
        `vmin*scale` y `vmax*scale`.
    """
    return int((size / vmax) * scale + vmin)


def graficar_coocurencia(
    mat,
    vmin=10,
    vmax=None,
    escala=700,
    n_nodos=0,
    titulo="Gráfico de Coocurrencias",
    dim_figura=(10, 6),
    node_cmap="RdPu",
    edge_cmap="Blues",
    offset_y=0.08,
    font_color="white",
    node_font_size=12,
    label_font_size=10,
    visualizar=True,
    ubicacion_archivo=None,
    devolver_grafica=False,
    seed=12,
):
    # Objeto del grafo
    G = nx.Graph()

    # Mapas de colores
    node_cmap = cm.get_cmap(node_cmap)
    edge_cmap = cm.get_cmap(edge_cmap)

    # máximo valor de la matriz
    max_cooc = max(mat.max())

    # calculando los bordes del grafo
    for indice, fila in mat.iterrows():
        for i, col in enumerate(fila):
            peso = float(col) / np.log10(max_cooc)
            if peso > 0 and (indice != mat.columns[i]):
                G.add_edge(indice, mat.columns[i], weight=round(peso, 1))

    # Eliminar nodos por criterio Numero o porcentaje
    if n_nodos > 0 and n_nodos <= 1:
        orden = sorted(list(G.degree), key=lambda kv: kv[1])[::-1]
        n = int(len(orden) * n_nodos)
        for no in orden[n:]:
            G.remove_node(no[0])
    elif n_nodos > 1:
        if n_nodos > len(G):
            warnings.warn(
                "n_nodos sobrepasa el número de nodos totales. "
                "Se tomarán todos los nodos del grafo."
            )
        else:
            orden = sorted(list(G.degree), key=lambda kv: kv[1])[::-1]
            for no in orden[n_nodos:]:
                G.remove_node(no[0])

    # Máximo grado de conexiones
    if vmax is None:
        vmax = max(list(dict(G.degree).values()))

    # Normalzizar el tamaño de los nodos
    node_size = [
        normalize_size(g, vmin=vmin, vmax=vmax, scale=escala)
        for g in list(dict(G.degree).values())
    ]
    # Valor máximo de las conexiones
    vmax = max(list(nx.get_edge_attributes(G, "weight").values()))
    # Normalizando el peso de las conexiones
    w_edges = [
        w / vmax for w in list(nx.get_edge_attributes(G, "weight").values())
    ]

    # posicion de los nodos
    pos = nx.spring_layout(G, seed=seed)

    # objeto fig de matplotlib
    fig, ax = plt.subplots(figsize=dim_figura)

    # gráficar nodos
    nodes = nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_size,
        node_color=list(dict(G.degree).values()),
        cmap=node_cmap,
    )
    # Colores para las conexiones
    edge_colors = [edge_cmap(c) for c in w_edges]

    # graficar conexiones entre nodos
    edges = []
    for e in range(G.number_of_edges()):
        edges.append(
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[list(G.edges())[e]],
                edge_color=edge_colors[e],
                width=1.2,
            )
        )

    # Cambiar el plano en el grafico para traslape de conexiones
    for e in range(G.number_of_edges()):
        edges[e].set_zorder(int(w_edges[e] * G.number_of_edges()))

    # Poner los nodos por encima de las conexiones
    nodes.set_zorder(G.number_of_edges() + 1)

    # Ubicando textos y grados de los nodos
    for key, value in pos.items():
        x, y = value[0] + 0, value[1] - offset_y
        plt.text(
            x,
            y,
            s=key,
            horizontalalignment="center",
            fontsize=label_font_size,
            zorder=G.number_of_edges() + 1,
        )
        plt.text(
            x,
            y - 0.015 + offset_y,
            s=G.degree[key],
            horizontalalignment="center",
            fontsize=node_font_size,
            color=font_color,
            zorder=G.number_of_edges() + 1,
        )

    # Ubicando colorbar del gráfico
    plt.colorbar(
        nodes,
        label="Número de conexiones",
        orientation="vertical",
        shrink=0.4,
    )

    ax.set_title(titulo, {"fontsize": 15, "fontweight": 700})
    plt.axis("off")
    if visualizar:
        plt.show()

    if ubicacion_archivo is not None:
        plt.savefig(
            ubicacion_archivo,
            bbox_inches="tight",
            transparent=False,
            facecolor="w",
            dpi=300,
        )

    if not visualizar and ubicacion_archivo is None:
        warnings.warn("Por favor fije una ruta para guardar la imagen")

    if devolver_grafica:
        return fig

    return ax
