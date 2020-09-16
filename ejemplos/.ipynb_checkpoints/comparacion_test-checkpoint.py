import os
import sys

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.limpieza import *
from contexto.vectorizacion import *
from contexto.comparacion import Similitud, Distancia, DiferenciaStrings

# Textos para probar las medidas de similitud y distancia
textos_prueba = [
    'primero de los dos textos de prueba',
    'segundo de los textos de evaluación',
    'una tercera oración que se empieza a alejar de los textos anteriores',
    'este no tiene ninguna relación con nada'
]

### 0. Preparar los insumos ###

## 0.1 Definir algunos vectorizadores para hacer diferentes pruebas
v_bow = VectorizadorFrecuencias()
v_tf = VectorizadorFrecuencias(tipo='tfidf', idf=False)
v_tfidf = VectorizadorFrecuencias(tipo='tfidf')
v_hashing = VectorizadorHash()
v_word2vec = VectorizadorWord2Vec()

## 0.2 Ajustar los vectorizadores (cuando aplique) al corpus de textos
v_bow.ajustar(textos_prueba)
v_tf.ajustar(textos_prueba)
v_tfidf.ajustar(textos_prueba)

## 0.3 Obtener representaciones vectoriales de los textos
vectores = {}
llaves = ['bow', 'tf', 'tfidf', 'hash', 'word2vec']
for i, v in enumerate([v_bow, v_tf, v_tfidf, v_hashing, v_word2vec]):
    vectores[llaves[i]] = v.vectorizar(textos_prueba)

### 1. Medidas de similitud entre textos ###

## 1.1 Inicializar objetos de clase Similitud
# Si se pasa un vectorizador al objeto de Similitud, este ya debe estar ajustado
s_bow = Similitud(v_bow)
s_tf = Similitud(v_tf)
s_tfidf = Similitud(v_tfidf)
s_hashing = Similitud(v_hashing)
s_word2vec = Similitud(v_word2vec)

## 1.2 Similitud coseno
"""
Los vectorizadores basados en frecuencias (sin consideraciones adicionales, como
tener en cuenta la frecuencia inversa IDF) arrojarán resultados muy similares
"""
coseno_bow = s_bow.coseno(textos_prueba)
coseno_tf = s_tf.coseno(textos_prueba)
coseno_hashing = s_hashing.coseno(textos_prueba)

# La vectorización TF-IDF tiene unos resultados distintos
coseno_tfidf = s_tfidf.coseno(textos_prueba)

"""
En general, los vectorizadores basados en frecuencias tendrán diferencias mayores
dependiendo de las palabras que estén presentes en los textos. Los vectorizadores
densos como word2vec o doc2vec son menos radicales, lo que permite encontrar
similitud entre textos con significados parecidos, incluso si no comparten tantas palabras
"""
coseno_doc2vec = s_word2vec.coseno(textos_prueba)

"""
También es posible ingresar directamente los vectores pre-calculados.
Esto debería arrojar los mismos resultados
"""

coseno_tfidf_vec = s_tfidf.coseno(vectores['tfidf'])
(coseno_tfidf == coseno_tfidf_vec).all()

## 1.3 Similitud de Jaccard
"""
El cálculo de la similitud de Jaccard puede funcionar con vectorizadores
basados en frecuencias (BOW, TF-IDF, Hashing), o directamente con los textos,
aunque en este segundo caso pueden presentarse resultados distintos
"""

# Utilizar el parámetro "vectorizar=True" debería dar el mismo resultado
# que aplicar la función directamente sobre vectores pre computados
a = s_bow.jaccard(textos_prueba, vectorizar=True)
b = s_bow.jaccard(vectores['bow'])
(a == b).all()

# Al aplicar la función directamente sobre los textos, los resultados pueden
# variar, dado que solo se toma en cuenta el vocabulario de cada par de textos
# a comparar (a diferencia del vocabulario total del corpus que se tiene en 
# cuenta en el vectorizador)
c = s_bow.jaccard(textos_prueba)
a == c

# Se puede utilizar otro vectorizador. Mientras sean vectorizadores basados en
# frecuencias, el cálculo de similitud Jaccard funcionará bien.
s_tfidf.jaccard(textos_prueba, True)
s_hashing.jaccard(textos_prueba, True)

# Los vectorizadores word2vec y doc2vec generan una representación densa, por lo que 
# no dan buenos resultados al utilizarse en este caso
s_word2vec.jaccard(textos_prueba, True)

### 2. Medidas de distancia entre textos ###

## 2.1 Inicializar objetos de clase Distancia
# Si se pasa un vectorizador al objeto de Distancia, este ya debe estar ajustado
d_bow = Distancia(v_bow)
d_tf = Distancia(v_tf)
d_tfidf = Distancia(v_tfidf)
d_hashing = Distancia(v_hashing)
d_word2vec = Distancia(v_word2vec)

## 2.2 Métricas de distancia definidas

# Distancia L1
l1_bow = d_bow.l1(textos_prueba)

# Distancia L2
l2_word2vec =d_word2vec.l2(textos_prueba)

# Distancia Minkowski 
l3_hashing =d_hashing.minkowski(textos_prueba, p=3) # norma L3

minkowski_2_word2vec = d_word2vec.minkowski(textos_prueba, p=2) # Misma norma L2
(l2_word2vec == minkowski_2_word2vec).all()

# Distancia Hamming
hamming_hashing = d_hashing.hamming(textos_prueba)

# Distancia Jaccard
jaccard_tfidf = d_tfidf.jaccard(textos_prueba)

# La suma de la distancia y similitud de jaccard entre dos vectores debería dar 1
jaccard_tfidf + s_tfidf.jaccard(textos_prueba, vectorizar=True)

## 2.3 Otras métricas de scikit-learn y scipy
"""
Adicionalmente a las funciones que la clase Distancia trae implementadas, se puede
utilizarn utilizar otras métricas soportadas por scikit-learn y scipy.
Para mayor información: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
"""

# Algunos ejemplos:
chebyshev_word2vec = d_word2vec.distancia_pares(textos_prueba, tipo_distancia='chebyshev')
rogerstanimoto_bow = d_bow.distancia_pares(textos_prueba, 'rogerstanimoto')
braycurtis_tfidf = d_tfidf.distancia_pares(textos_prueba, 'braycurtis')

### 3. Medidas de similitud y distancia entre strings ###
'''
Esta clase (DiferenciaStrings) se recomienda para comparaciones de strings 
relativamente cortos, como nombres, direcciones y otras cadenas de caracteres similares.
Para textos más largos, se recomiendan las clases "Similitud" o "Distancia".
'''
## 3.1 Textos de prueba
t1 = 'pescado'
t2 = 'pecsado'
t3 = 'Jonhatan Ruiz Diaz'
t4 = 'Jonatan Ruis Díaz'
strings = [t1, t2, t3, t4]

## 3.2 Inicializar objeto de clase Distancia
dif_strings = DiferenciaStrings()

## 3.3 Medidas de diferencias entre strings
# Diferencia entre dos textos
dif_strings.distancia_levenshtein([t1,t2])
dif_strings.distancia_hamming([t3,t4]) 

# Diferencia entre lista de textos
dif_strings.distancia_damerau_levenshtein(strings)
# Normalizar dividiendo por el texto más corto
dif_strings.distancia_damerau_levenshtein(strings, norm=1)
# Normalizar dividiendo por el texto más largo (se garantiza que queda entre 0 y 1)
dif_strings.distancia_damerau_levenshtein(strings, norm=2)

## 3.4 Medidas de similitud entre strings
# Similitud entre dos textos
dif_strings.similitud_jaro([t1,t2])

# Similitud entre lista de textos
dif_strings.similitud_jaro_winkler(strings)