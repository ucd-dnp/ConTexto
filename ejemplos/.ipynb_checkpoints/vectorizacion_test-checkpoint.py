import os
import sys

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.limpieza import limpieza_texto, lista_stopwords
from contexto.vectorizacion import *

# Corpus de prueba
textos_prueba = [
    'Este es el primer texto de prueba para la vectorización y sus elementos.',
    'Una segunda oración permite evaluar si hay elementos en común para vectorizar.',
    'Tercera frase que consiste en un texto complementario con palabras comúnmente utilizadas.',
    'En esta oración y la siguiente se introducen elementos para completar un grupo de por lo menos 5.',
    'Finalmente, esta frase cierra un grupo de 5 oraciones para probar la vectorización.',
    'Una última frase para ampliar un poco el grupo.']

# Limpieza básica a los textos para quitar ruido
textos_limpios = [limpieza_texto(i, lista_stopwords(), quitar_numeros=False) for i in textos_prueba]

# Texto que no hace parte del corpus original
texto_nuevo = 'hola, esta es una frase de prueba para aplicar la vectorización'

### 1. Vectorizadores por frecuencia de términos ###

## 1.1 Inicializar los vectorizadores
v_bow = VectorizadorFrecuencias()
# Este tiene en cuenta palabras y bigramas, y solo coge las 20 más frecuentes
v_tfidf = VectorizadorFrecuencias('tfidf', rango_ngramas=(1, 2), max_elementos=20)

## 1.2 Ajustar los vectorizadores
# Se van a guardar los vectorizadores ajustados en archivos para su posterior uso
v_bow.ajustar(textos_limpios, archivo_salida='out/v_bow.pk')
v_tfidf.ajustar(textos_limpios, archivo_salida='out/v_tfidf.pk')

## 1.3 Vocabulario de un vectorizador entrenado
print(v_bow.vocabulario())
print(v_tfidf.vocabulario())

## 1.4 Vectorizar textos utilizando los vectorizadores entrenados
vector_bow = v_bow.vectorizar(texto_nuevo, disperso=True)  # Salida como matriz dispersa
vector_tfidf = v_tfidf.vectorizar(texto_nuevo, disperso=False)  # Salida como un numpy array

## 1.5 Transformada inversa
'''
Nótese que al realizar la transformada inversa se pierde el orden de las palabras.
Esto se debe a que estos métodos de vectorización no tienen en cuenta el orden
sino la frecuencia de aparición de cada término.
Además, si un término no está en el vocabulario del vectorizador, no va a estar
incluído en el vector y por lo tanto no se podrá recuperar en la transformada
inversa.
'''
print(textos_limpios[0])
print(v_bow.inversa(v_bow.vectorizar(textos_prueba))[0])

print(textos_limpios[2])
print(v_tfidf.inversa(v_tfidf.vectorizar(textos_prueba))[2])

## 1.6 Cargar un vectorizador ajustado previamente
'''
Al cargar un vectorizador ajustado previamente (mediante el parámetro "archivo_modelo")
Los demás parámetros de inicialización no serán tenidos en cuenta, pues esos parámetros
se tomarán del vectorizador cargado.
'''
v_bow_2 = VectorizadorFrecuencias(archivo_modelo='out/v_bow.pk')
v_tfidf_2 = VectorizadorFrecuencias(archivo_modelo='out/v_tfidf.pk')

# Se vectoriza el mismo texto con los vectorizadores cargados
vector_bow_2 = v_bow_2.vectorizar(texto_nuevo, disperso=True)  # Salida como matriz dispersa
vector_tfidf_2 = v_tfidf_2.vectorizar(texto_nuevo, disperso=False)  # Salida como un numpy array

# Se comprueba que los vectores resultantes sean iguales
np.all((vector_bow == vector_bow_2).toarray())
np.all(vector_tfidf == vector_tfidf_2)

### 2. Vectorizador por hashing ###

## 2.1 Inicializar el vectorizador
# Se define que los vectores tendrán 50 elementos
v_hash = VectorizadorHash(n_elementos=50)

## 2.2 Vectorizar textos utilizando el vectorizador
'''
A pesar de que el objeto HashingVectorizer de la librería scikit-learn
incluye la función "fit", esta en la práctica no hace nada, pues este
tipo de vectorizador funciona sin vocabulario y no debe ser ajustado.
Por lo tanto, en la librería no se ha incluído esta opción. En vez de eso,
el objeto se aplica directamente a los textos para vectorizarlos.

Por este mismo motivo, el VectorizadorHash no permite la transformación
inversa para identificar las palabras de un vector.
'''
vectores_prueba = v_hash.vectorizar(textos_prueba)
vectores_prueba.shape

vector_nuevo = v_hash.vectorizar(texto_nuevo, disperso=False)
vector_nuevo.shape

### 3. Vectorizador por Word2Vec ###

## 3.1 Inicializar el vectorizador
v_word2vec = VectorizadorWord2Vec()

## 3.2 Vectorizar textos utilizando el vectorizador
'''
Este vectorizador obtiene los vectores de cada palabra de un texto, y luego las 
promedia para obtener un único vector para el texto completo.
'''
vector = v_word2vec.vectorizar(texto_nuevo)
vector.shape

## 3.3 Textos con palabras desconocidas (no incluídas en el modelo)
'''
El argumento booleano 'quitar_desconocidas' en la función vectorizar_texto hará que
la función sea ligeramente más demorada, pero quizás más precisa, al no tener en cuenta palabras
que no están incluídas en el modelo. Cuando este argumento es False (valor por defecto),
para cada palabra desconocida se incluirá un vector de solo ceros, lo que afectará el vector 
promedio resultante.
'''

texto_1 = 'En este texto todas las palabras son conocidas, por lo que los resultados deberían ser iguales'
texto_2 = 'En este texto hay asfafgf términos desconocidos FGs<g gsi<gi<sbf'

for i, t in enumerate([texto_1, texto_2]):
    print('\n------------------')
    print(f'Texto {i+1}:')
    print(f'"{t}"')
    v1 = v_word2vec.vectorizar(t, quitar_desconocidas=False)
    v2 = v_word2vec.vectorizar(t, quitar_desconocidas=True)
    print(f'Diferencia promedio: {(v1 - v2).mean()}')

## 3.4 Obtener palabras y vectores de un texto
df_palabras = v_word2vec.vectores_palabras(texto_nuevo, tipo='dataframe')
dict_palabras = v_word2vec.vectores_palabras(texto_nuevo, tipo='diccionario')

## 3.5 Similitudes entre textos
'''
Esta función aprovecha las facilidades de la librería Spacy para medir la
similaridad entre 2 palabras o textos.
'''
t1 = 'los perros y los gatos suelen pelear mucho.'
t2 = 'caninos y felinos entran en disputas con frecuencia.'
t3 = 'este tercer texto habla sobre un tema distinto a los otros dos'

for i in [t1, t2]:
    for j in [t2, t3]:
        if i != j:
            similitud = v_word2vec.similitud_textos(i, j)
            print('-----------------------')
            print(f'Texto 1: {i}')
            print(f'Texto 2: {j}')
            print(f'Similitud entre textos: {similitud}')

### 4. Vectorizador por Doc2Vec ###

## 4.1 Inicializar el vectorizador
# Se configura para que tenga 100 elementos y se entrene por 25 épocas
'''
Dado que el "corpus" de entrenamiento va a se pequeño (5 textos cortos), puede haber 
error si ningúna palabra cumple con el parámetro "minima_cuenta=5" (valor por defecto).
Para evitar este error en este caso, se cambia ese parámetro a 1 (valor mínimo).
'''
v_doc2vec = VectorizadorDoc2Vec(n_elementos=100, epocas=25, minima_cuenta=1)

## 4.2 Entrenar el modelo en un corpus
v_doc2vec.entrenar_modelo(textos_limpios, archivo_salida='out/v_doc2vec.pk')

## 4.3 Vectorizar textos utilizando el vectorizador
vector = v_doc2vec.vectorizar(texto_nuevo)
vector.shape

## 4.4 Cargar un vectorizador entrenado previamente
v_doc2vec_2 = VectorizadorDoc2Vec(archivo_modelo='out/v_doc2vec.pk')

# Se vectoriza el mismo texto con el vectorizador cargado
vector_2 = v_doc2vec_2.vectorizar(texto_nuevo)

# Se comprueba que ambos vectores resultantes sean iguales
np.all(vector == vector_2)