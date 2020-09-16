import os
import sys

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.limpieza import limpieza_texto, lista_stopwords
from contexto.vectorizacion import *
from contexto.utils.auxiliares import verificar_crear_dir

import matplotlib.pyplot as plt
from sklearn.datasets import fetch_20newsgroups
from sklearn.cluster import KMeans
from sklearn import manifold, decomposition, discriminant_analysis

# Temas que en principio son bastante diferentes entre sí, por lo que deberían
# ser más fáciles de agrupar
grupo_1 = ['comp.graphics', 'rec.sport.baseball', 'sci.med', 'talk.politics.guns']

# Temas mucho más similares entre sí
grupo_2 = ['soc.religion.christian', 'alt.atheism', 'talk.religion.misc', 'talk.politics.mideast']

# Vectorizadores a considerar
vectorizadores = ['bow', 'tfidf', 'hash', 'doc2vec', 'word2vec', 'word2vec_conocidas']

# Función para graficar los puntos
def embedding_plot(X, y, title, num_grupo, norm, nombres, dir_out='out/caso_uso_vectores/'): 
    num_cats = len(np.unique(y))
    # Hasta 8 diferentes categorías
    colores = ['black', 'blue', 'yellow', 'red', 'green', 'orange', 'brown', 'purple']
    color_dict = {i:colores[i] for i in range(num_cats)}
    label_dict = {i:nombres[i] for i in range(num_cats)}
    fig, ax = plt.subplots(figsize=(10,10))
    for g in range(num_cats):
        ix = np.where(y == g)
        ax.scatter(X[ix,0], X[ix,1], c=color_dict[g], label=label_dict[g])
    # Convenciones
    plt.legend(loc="lower right", title="Clases")
    plt.xticks([]), plt.yticks([])
    plt.title(title)
    # Guardar la imagen resultante
    verificar_crear_dir(dir_out)
    norm_str = '_norm' if norm else ''
    nombre_archivo = f'grupo_{num_grupo}_{title}{norm_str}.jpg'
    plt.savefig(dir_out + nombre_archivo)
    plt.close()

def comparacion_vectorizadores(num_grupo, normalizar, vectorizadores=vectorizadores):
    grupo = grupo_1 if num_grupo == 1 else grupo_2 
    # Obtener dataset de las categorías seleccionadas
    dataset = fetch_20newsgroups(subset='all', categories=grupo, shuffle=True, random_state=42)
    clases = dataset.target
    nombres_clases = dataset.target_names
    #
    # Limpieza básica a los textos para quitar ruido
    # Tener en cuenta que los textos están en inglés
    textos_limpios = [limpieza_texto(i, lista_stopwords('en')) for i in dataset.data]
    #
    # Inicializar los 5 vectorizadores. Todos se configuran para tener 300 elementos,
    # de modo que estén en igualdad de condiciones
    v_bow = VectorizadorFrecuencias(tipo='bow', max_elementos=300)
    v_tfidf = VectorizadorFrecuencias(tipo='tfidf', max_elementos=300)
    v_hash = VectorizadorHash(n_elementos=300)
    v_word2vec = VectorizadorWord2Vec('en')
    v_doc2vec = VectorizadorDoc2Vec(n_elementos=300)
    #
    # Ajustar los modelos que deben ser ajustados sobre el corpus
    v_bow.ajustar(textos_limpios)
    v_tfidf.ajustar(textos_limpios)
    v_doc2vec.entrenar_modelo(textos_limpios)
    #
    # Obtener los vectores para cada vectorizador
    dict_vectores = {}
    for v in vectorizadores:
        print(f'Vectorizando con técnica {v}...')
        if 'conocidas' in v:
            v_mod = v.split('_')[0]
            dict_vectores[v] = eval(f'v_{v_mod}.vectorizar(textos_limpios, quitar_desconocidas=True)')
        else:
            dict_vectores[v] = eval(f'v_{v}.vectorizar(textos_limpios)')
    #
    # Normalizar los vectores
    if normalizar:
        for v in vectorizadores:
            dict_vectores[v] = dict_vectores[v] / dict_vectores[v].max(axis=0)
    #
    # Aplicar t-sne para dejar vectores en 2 dimensiones
    dict_tsne = {}
    for v in vectorizadores:
        print(f'Reducción de dimensionalidad a vector {v}...')
        dict_tsne[v] = manifold.TSNE(n_components=2, init="pca").fit_transform(dict_vectores[v])
    #
    # Graficar los puntos para cada técnica
    for v in vectorizadores:
        embedding_plot(dict_tsne[v], clases, v, num_grupo, normalizar, nombres_clases)


########################################

# Barrido para realizar las pruebas
for num_grupo in [1, 2]:
    for normalizar in [True, False]:
        print(f'\n -------------- Grupo: {num_grupo}, normalizar: {normalizar}')
        comparacion_vectorizadores(num_grupo, normalizar, vectorizadores=vectorizadores)
