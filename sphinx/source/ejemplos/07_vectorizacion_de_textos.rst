.. _07_vectorizacion_de_textos:

Vectorización de textos
=======================

Este ejemplo muestra las principales funcionalidades del módulo :py:mod:`Vectorización <vectorizacion>` de la librería. Este módulo permite generar representaciones vectoriales o numéricas de textos a través de distintas técnicas. La capacidad de representar un texto de forma numérica es muy útil para análisis posteriores de textos, tales como comparaciones, agrupaciones, entrenamiento de modelos de clasificación, entre otros.


Importar paquetes necesarios y adecuar el texto de prueba
---------------------------------------------------------

El primer paso es importar las funciones del módulo de :py:mod:`Vectorización <vectorizacion>` y definir los textos para correr los ejemplos. Adicionalmente, se importan y utilizan las funciones :py:func:`limpieza.limpieza_texto` y :py:func:`limpieza.lista_stopwords` del módulo :py:mod:`Limpieza <limpieza>`, para hacer un procesamiento previo de los textos antes de generar sus representaciones vectoriales.

.. code-block:: python

    >>> from contexto.limpieza import limpieza_texto, lista_stopwords
    >>> from contexto.vectorizacion import *

    >>> # Corpus de prueba
    >>> textos_prueba = [
    >>>     'Este es el primer texto de prueba para la vectorización y sus elementos.',
    >>>     'Una segunda oración permite evaluar si hay elementos en común para vectorizar.',
    >>>     'Tercera frase que consiste en un texto complementario con palabras comúnmente utilizadas.',
    >>>     'En esta oración y la siguiente se introducen elementos para completar un grupo de por lo menos 5.',
    >>>     'Finalmente, esta frase cierra un grupo de 5 oraciones para probar la vectorización.',
    >>>     'Una última frase para ampliar un poco el grupo.']

    >>> # Limpieza básica a los textos para quitar ruido
    >>> textos_limpios = [limpieza_texto(i, lista_stopwords(), quitar_numeros=False) for i in textos_prueba]

    >>> # Texto que no hace parte del corpus original
    >>> texto_nuevo = 'hola, este es un texto de prueba. Se desea aplicar la vectorización en este texto.'


Vectorizaciones por frecuencia de términos
------------------------------------------

La clase :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>` permite aplicar las técnicas Bag of Words (BOW), Term Frecuency (TF) y Term Frequency – Inverse Document Frequency (TF-IDF) para generar representaciones vectoriales de textos basadas en la frecuencia con la que aparecen ciertas palabras o términos en cada texto.

Inicializar y ajustar los vectorizadores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para utilizar estos tipos de vectorización es necesario definir un objeto de clase :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>`, especificando aspectos como:

- Qué tipo de técnica aplicar (BOW, TF o TF-IDF).
- El rango de n-gramas que se desea tener en cuenta (solo palabras, palabras y bigramas, etc.).
- Si se quiere limitar el tamaño del vocabulario del vectorizador a los *n* términos más frecuentes. Esto puede ser útil cuando se tienen muchos textos de larga longitud, lo que puede llegar a generar un vocabulario demasiado grande si no se acota.

Una vez se define el objeto del vectorizador, es necesario ajustarlo sobre un corpus, para que aprenda el vocabulario que va a utilizar. Al momento de ajustar el vectorizador se puede utilizar el parámetro *archivo_salida*. Si este parámetro se utiliza, el vectorizador ajustado va a quedar guardado como un objeto tipo *Pickle* en la ubicación definida por el usuario.

.. code-block:: python

    >>> ## Inicializar los vectorizadores

    >>> # Vectorizador BOW
    >>> v_bow = VectorizadorFrecuencias()

    >>> # Vectorizador TF-IDF. Este tiene en cuenta palabras y bigramas, y solo coge las 20 más frecuentes
    >>> v_tfidf = VectorizadorFrecuencias('tfidf', rango_ngramas=(1, 2), max_elementos=20)

    >>> ## Ajustar los vectorizadores
    >>> # Se van a guardar los vectorizadores ajustados en archivos para su posterior uso
    >>> v_bow.ajustar(textos_limpios, archivo_salida='salida/v_bow.pk')
    >>> v_tfidf.ajustar(textos_limpios, archivo_salida='salida/v_tfidf.pk')

Vocabulario de los vectorizadores ajustados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez cada vectorizador ha sido ajustado, se puede acceder a su vocabulario llamando el método :py:meth:`vocabulario() <vectorizacion.VectorizadorFrecuencias.vocabulario>`. Esto retorna un DataFrame de Pandas con el término asignado a cada posición de los vectores resultantes. A continuación se muestran los términos de las primeras 10 posiciones para los 2 vectorizadores ajustados. 

Se puede observar que `v_tfidf` incluye términos y bigramas, tal y como se estableció al definir esa variable.

.. code-block:: python

    >>> ## Vocabulario de un vectorizador entrenado
    >>> from IPython.display import display

    >>> display(v_bow.vocabulario().head(10), v_tfidf.vocabulario().head(10))

* Vocabulario vectorizador BOW

========  ===================
posición  palabra
========  ===================
0         ampliar
1         cierra
2         complementario
3         completar
4         común
5         comúnmente
6         consiste
7         elementos
8         evaluar
9         finalmente
========  ===================

* Vocabulario vectorizador TF-IDF

========  ===================
posición  palabra
========  ===================
0         ampliar
1         elementos
2         frase
3         grupo
4         oración
5         oración permite
6         oración siguiente
7         palabras
8         palabras comúnmente
9         permite
========  ===================

Vectorizar textos utilizando los vectorizadores entrenados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez se tiene el vectorizador ajustado, la función `vectorizar` permite obtener, para uno o varios textos de entrada, un arreglo (*array*) en numpy de 2 dimensiones. La cantidad de filas de este arreglo corresponde al número de textos vectorizados, y la cantidad de columnas corresponde al tamaño del vocabulario del vectorizador. El argumento *disperso* permite  obtener como salida una matriz dispersa (disperso=True) o un arreglo de numpy (disperso=False). Esto puede traducirse en un ahorro significativo de memoria en el caso de que se tengan muchos textos y/o un vocabulario muy grande.

Es importante anotar que si algún texto de entrada tiene palabras que no hacen parte del vocabulario del vectorizador, estas no serán tenidas en cuenta.

.. code-block:: python

    >>> vector_bow = v_bow.vectorizar(texto_nuevo, disperso=True)  # Salida como matriz dispersa
    >>> vector_tfidf = v_tfidf.vectorizar(texto_nuevo, disperso=False)  # Salida como un numpy array

    >>> print('El vector de BOW sale como una matriz dispersa:')
    >>> print(vector_bow)
    >>> print('\n--------')
    >>> print('El vector de TF-IDF sale como un numpy array:')
    >>> print('Dimensiones de la salida:', vector_tfidf.shape)
    >>> print(vector_tfidf)

    El vector de BOW sale como una matriz dispersa:
      (0, 20)   1
      (0, 24)   2
      (0, 26)   1

    --------
    El vector de TF-IDF sale como un numpy array:
    Dimensiones de la salida: (1, 20)
    [[0.         0.         0.         0.         0.         0.
      0.         0.         0.         0.         0.         0.
      0.         0.         0.         0.         0.         0.
      0.89442719 0.4472136 ]]


Transformada inversa de un vector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La función :py:func:`inversa() <vectorizacion.VectorizadorFrecuencias.inversa>` de la clase :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>` permite, a partir de un vector, obtener las palabras que componen el texto representado por dicho vector. 

Nótese que al realizar la transformada inversa se pierde el orden de las palabras. Esto se debe a que estos métodos de vectorización no tienen en cuenta el orden sino la frecuencia de aparición de cada término. Además, si un término no está en el vocabulario del vectorizador, no va a estar incluído en el vector y por lo tanto no se podrá recuperar en la transformada
inversa.

.. code-block:: python

    >>> print(textos_limpios[0])
    >>> print(v_bow.inversa(v_bow.vectorizar(textos_prueba))[0])
    
    >>> print(textos_limpios[2])
    >>> print(v_tfidf.inversa(v_tfidf.vectorizar(textos_prueba))[2])
    
    primer texto prueba vectorización elementos
    ['elementos' 'primer' 'prueba' 'texto' 'vectorización']
    tercera frase consiste texto complementario palabras comúnmente utilizadas
    ['frase' 'palabras' 'palabras comúnmente' 'texto']


Cargar un vectorizador ajustado previamente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previamente vimos cómo se puede guardar un vectorizador ajustado, por medio del parámetro *archivo_salida* de la función `ajustar`. Este vectorizador, ya ajustado, se puede cargar y utilizar, al momento de definir un nuevo objeto de la clase :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>`. Para cargar un vectorizador ajustado previamente se debe utilizar el parámetro *archivo_modelo*, especificando dónde está el archivo con el vectorizador ya ajustado. Al usar esta opción, los demás parámetros de inicialización no serán tenidos en cuenta, pues esos parámetros se tomarán del vectorizador cargado.

.. code-block:: python

    >>> v_bow_2 = VectorizadorFrecuencias(archivo_modelo='salida/v_bow.pk')
    >>> v_tfidf_2 = VectorizadorFrecuencias(archivo_modelo='salida/v_tfidf.pk')
    
    >>> # Se vectoriza el mismo texto con los vectorizadores cargados
    >>> vector_bow_2 = v_bow_2.vectorizar(texto_nuevo, disperso=True)  # Salida como matriz dispersa
    >>> vector_tfidf_2 = v_tfidf_2.vectorizar(texto_nuevo, disperso=False)  # Salida como un numpy array
    
    >>> # Se comprueba que los vectores resultantes sean iguales
    >>> print(np.all((vector_bow == vector_bow_2).toarray()))
    >>> print(np.all(vector_tfidf == vector_tfidf_2))
    
    True
    True


Vectorización por medio de *Hashing*
------------------------------------

La clase :py:class:`VectorizadorHash <vectorizacion.VectorizadorHash>` utiliza el *hashing trick* para determinar directamente (sin necesidad de ajustar sobre un corpus) la posición de cada término de un texto dentro de un vector numérico. Esta técnica es rápida y ligera en memoria, pues no requiere aprender ni guardar un vocabulario. Esto también tiene algunas desventajas; por ejemplo, a partir de un vector no se puede aplicar una transformada inversa para conocer qué palabras contenía el texto.

Adicionalmente, cuando se consideran muchos textos, o textos muy grandes, existe la posibilidad de que se presenten 'colisiones'. Una colisión se da cuando el vectorizador representa de la misma manera a dos términos distinitos, lo cual introduce ambiguedad en la vectorización y disminuye la calidad de la representación numérica de los textos. Para evitar este problema, se puede configurar el objeto de clase :py:class:`VectorizadorHash <vectorizacion.VectorizadorHash>` para que tenga muchos más elementos (por medio del parámetro *n_elementos*) a medida que se trabaja con textos de mayor longitud y vocabulario.

.. code-block:: python

    >>> ## Inicializar el vectorizador
    >>> # En este caso se define que los vectores tendrán 50 elementos
    >>> v_hash = VectorizadorHash(n_elementos=50)
    
    >>> ## Aplicar el vectorizador directamente a los textos (no hace falta ajustar antes)
    >>> vectores_prueba = v_hash.vectorizar(textos_prueba)
    >>> print("Dimensiones del grupo de vectores:", vectores_prueba.shape)
    
    >>> # El valor de cada elemento será proporcional a la frecuencia de aparición de un término en el texto
    >>> vector_nuevo = v_hash.vectorizar(texto_nuevo, disperso=False)
    >>> print('----------')
    >>> print("Dimensiones del vector:", vector_nuevo.shape)
    >>> print(vector_nuevo)
    
    Dimensiones del grupo de vectores: (6, 50)
    ----------
    Dimensiones del vector: (1, 50)
    [[ 0.   0.  -0.2  0.   0.   0.   0.2  0.   0.2  0.   0.   0.   0.   0.
       0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.   0.4 -0.2 -0.2
       0.   0.   0.   0.   0.   0.   0.  -0.2  0.   0.  -0.2  0.   0.  -0.4
       0.   0.   0.6  0.   0.   0.2  0.   0. ]]


Vectorización utilizando *word embeddings* - Word2Vec
-----------------------------------------------------

La clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` utiliza por debajo las funcionalidades de la librería 
`spaCy <https://spacy.io/>`_ para cargar *embeddings*, o representaciones vectoriales densas, de palabras en diferentes idiomas. Estas *embeddings* son representaciones de 300 elementos para cada palabra que exista en el diccionario del modelo, y ya han sido previamente entrenadas sobre un corpus de texto muy grande, utilizando técnicas como *Word2Vec* y *GloVe*.

La clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` permite utilizar y acceder a estas representaciones ya entrenadas que, a diferencia de los vectores basados en frecuencias, permiten a través del entrenamiento previo capturar información del contexto de las palabras. De esta manera, las representaciones densas de las palabras 'hombre' y 'niño' van a ser similares entre sí en ese espacio de 300 dimensiones, mientas que las palabras 'hombre' y 'cuchara' van a estar más alejadas.

Inicializar y aplicar el vectorizador
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al definir un objeto de la clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` es necesario definir el lenguaje y el tamaño del modelo que se desea utilizar. De manera similar al caso de lematización, en este caso spaCy tiene modelos de varios tamaños para cada lenguaje. Entre más grande sea el modelo, este contará con vectores para un vocabulario más grande. Los modelos de spaCy que soportan la vectorización son el mediano ('md') y el grande ('lg').

Dado que se carga un modelo previamente entrenado, no es necesario ajustar este vectorizador. Al igual que con el `VectorizadorHash`, los objetos de clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` pueden ser aplicados directamente a una palabra o texto de entrada para obtener su vector. Cuando el texto de entrada tiene dos o más palabras, la función `vectorizar` obtendrá el vector de cada palabra que compone el texto, y luego calculará el promedio de todos los vectores para obtener un único vector de salida.

.. note::
    La primera vez que se utilice una combinación particular de lenguaje + tamaño, la librería descargará el modelo correspondiente en el computador del usuario. Para poder usar este modelo, se debe reiniciar la sesión de Python y correr la función de nuevo.

.. code-block:: python

    >>> ## Inicializar el vectorizador
    >>> v_word2vec = VectorizadorWord2Vec()
    >>> 
    >>> ## Vectorizar textos utilizando el vectorizador
    >>> 
    >>> vector = v_word2vec.vectorizar(texto_nuevo)
    >>> print("Dimensiones del vector:", vector.shape)
    >>> print("Primeros 10 elementos del vector:\n", vector[0,:10])
    
    Dimensiones del vector: (1, 300)
    Primeros 10 elementos del vector: 
     [ 0.3364028   0.7943878  -0.5733206   1.1075957   1.1357956  -1.3824669
      0.53068686  0.662284   -0.33499992  0.22997226]


Textos con palabras desconocidas (no incluídas en el modelo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como se mencionó en la sección anterior, un texto se vectoriza sacando el promedio de los vectores de cada palabra. Por grande que sea el vocabulario del modelo pre-entrenado que se utiliza, es posible que un nuevo texto contenga palabras que no se encuentran en el vocabulario del modelo. En este caso, el método `vectorizar` del objeto de clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` puede manejar las palabras desconocidas de dos formas distintas.

El argumento booleano *quitar_desconocidas* en el método `vectorizar`, cuando se hace igual a True, hará que no se tengan en cuenta las palabras que no están incluídas en el modelo. De esta manera, el vector del texto será el promedio de solamente los vectores de palabras que están presentes en el vocabulario del modelo. Cuando este argumento es False (valor por defecto), para cada palabra desconocida se incluirá un vector de solo ceros, lo que afectará el vector promedio resultante.

A continuación se hace la vectorización de 2 textos distintos. En el primer texto todas las palabras hacen parte del vocabulario del modelo, por lo que el valor del parámetro *quitar_desconocidas* no va a afectar el vector de salida. Por otro lado, el segundo texto tiene 3 palabras desconocidas. En este caso, los valores del vector resultante van a ser ligeramente menores si se utiliza *quitar_desconocidas=False*, pues los vectores de solo ceros (correspondientes a las palabras desconocidas) afectarán el promedio del vector de salida.

.. code-block:: python

    >>> texto_1 = 'En este texto todas las palabras son conocidas, por lo que los resultados deberían ser iguales'
    >>> texto_2 = 'En este texto hay asfafgf términos desconocidos FGs<g gsi<gi<sbf'

    >>> for i, t in enumerate([texto_1, texto_2]):
    >>>     print('\n------------------')
    >>>     print(f'Texto {i+1}:')
    >>>     print(f'"{t}"')
    >>>     v1 = v_word2vec.vectorizar(t, quitar_desconocidas=False)
    >>>     v2 = v_word2vec.vectorizar(t, quitar_desconocidas=True)
    >>>     print(f'Diferencia promedio: {(v1 - v2).mean()}')
    
    ------------------
    Texto 1:
    "En este texto todas las palabras son conocidas, por lo que los resultados deberían ser iguales"
    Diferencia promedio: 0.0
    
    ------------------
    Texto 2:
    "En este texto hay asfafgf términos desconocidos FGs<g gsi<gi<sbf"
    Diferencia promedio: -0.017988834530115128


Obtener palabras y vectores de un texto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si se desea, es posible obtener los vectores correspondientes a las palabras (incluidas en el modelo) que componen un texto. Esto se puede hacer mediante el método `vectores_palabras`, que puede devolver un DataFrame de Pandas o un diccionario de Python con cada palabra del texto y su correspondiente vector. 

.. code-block:: python

    >>> df_palabras = v_word2vec.vectores_palabras(texto_nuevo, tipo='dataframe')
    >>> dict_palabras = v_word2vec.vectores_palabras(texto_nuevo, tipo='diccionario')

    >>> df_palabras

=====  =============  =========  =========  =========  =========  =========  =========  =========  =========  =========  ===  =========  =========  =========  =========  =========  =========  =========  =========  =========  =========
index  palabra        x_1        x_2        x_3        x_4        x_5        x_6        x_7        x_8        x_9        ...    x_291      x_292      x_293      x_294      x_295      x_296      x_297      x_298      x_299    x_300
=====  =============  =========  =========  =========  =========  =========  =========  =========  =========  =========  ===  =========  =========  =========  =========  =========  =========  =========  =========  =========  =========
0      hola           2.02740    -1.274000  -1.36240   1.66310    0.923830   -0.150770  0.345830   1.36940    0.61444    ...  1.35750    0.38467    0.505280   0.858590   1.36380    1.527900   -1.262800  0.82706    -0.85570   1.188800
1      ,              1.34940    2.957500   -0.60029   -1.40760   1.909200   -0.285360  0.581940   2.43280    -1.59410   ...  -1.31810   0.24310    0.353180   0.727520   2.83400    -0.051198  3.489500   1.34580    -2.10970   -0.455530
2      este           -1.18150   4.074300   -3.72130   5.79750    -1.925600  -1.465900  -1.253400  -0.48991   -1.67700   ...  -0.38054   -1.09720   -0.531430  -3.957000  -0.24913   -1.922400  2.318000   1.02020    2.88400    1.210200
3      es             -5.67930   -1.851200  -6.46630   -1.57010   -1.770900  -4.910200  0.362290   5.48250    -1.92520   ...  -7.98300   -1.78740   -7.126600  -1.653700  2.02190    3.560900   -1.280100  -0.48058   0.65105    -2.964400
4      un             0.89790    5.847700   -8.07040   8.84070    -5.782700  4.143200   -0.571410  -0.40119   -4.93190   ...  3.62440    -3.06400   -0.009281  -8.710900  2.13160    -6.541200  0.267060   3.80520    6.24080    2.837600
5      texto          -1.28030   0.235800   -1.87390   0.90060    -0.246720  -2.607000  0.063837   5.56190    0.33668    ...  1.07400    2.13570    -5.215400  -2.547800  -3.13900   -0.193810  -1.107400  0.75978    0.73341    0.052985
6      de             0.38853    0.099683   5.99970    -0.83435   3.742600   -1.322600  3.394800   -2.84590   3.28950    ...  -7.32290   -1.18470   0.010714   -3.567100  0.70618    -1.429100  -1.557600  2.12330    0.92697    1.500900
7      prueba         1.43410    1.177200   -0.87280   0.85857    -3.028900  -1.197400  0.492080   1.47920    -2.09090   ...  3.26440    0.39533    1.870100   -1.900300  2.28250    -0.399500  -0.059084  0.11512    -1.33580   -1.433700
8      .              1.65170    -1.963400  -0.60317   -1.44970   -4.645600  -2.654800  1.787100   2.00860    2.55950    ...  -2.95930   0.74480    2.189800   0.798260   2.64470    -1.984700  -3.354100  -0.39062   -1.83260   -3.034700
9      Se             3.44230    3.517600   -0.98323   9.61150    21.457001  1.370800   9.016600   -7.84960   -6.47540   ...  1.33140    -9.96640   -2.405100  6.446200   -8.91220   11.387000  1.724500   -1.94600   -2.71580   2.913400
10     desea          -4.29940   1.219600   0.87215    -0.35671   0.492250   -1.972400  -0.203840  7.01900    3.22810    ...  1.99170    -3.23270   -1.868300  -1.517700  0.66831    0.154560   -3.252000  0.28146    1.07270    -1.384100
11     aplicar        -1.40740   1.299100   2.13120    0.30753    -0.928430  -0.020372  -2.409200  0.80072    -1.60250   ...  -0.57665   2.95660    0.028279   -0.052178  -2.21730   -1.184800  -1.614600  -0.92878   -2.93960   -1.921600
12     la             4.81890    -1.975100  3.98690    -9.48320   14.446000  -7.265700  2.178200   -8.03830   6.41720    ...  -0.94738   2.05770    -5.546100  5.935200   -0.55970   2.730500   -4.170200  -0.59639   0.24436    2.381200
13     vectorización  -0.28528   1.867000   0.71944    -0.46232   0.076307   -2.183900  -1.985400  1.27820    -1.78520   ...  0.90734    1.39140    -2.335200  1.182900   -1.13460   -0.324270  0.553240   -0.17405   -1.53170   -1.541200
14     en             4.98830    -3.279500  6.72300    2.27280    2.543900   2.365700   -2.844600  -2.96690   -1.61240   ...  -1.73490   -0.80675   1.798400   1.553700   9.86970    0.683280   3.565700   3.63670    4.76150    -0.695040
15     este           -1.18150   4.074300   -3.72130   5.79750    -1.925600  -1.465900  -1.253400  -0.48991   -1.67700   ...  -0.38054   -1.09720   -0.531430  -3.957000  -0.24913   -1.922400  2.318000   1.02020    2.88400    1.210200
16     texto          -1.28030   0.235800   -1.87390   0.90060    -0.246720  -2.607000  0.063837   5.56190    0.33668    ...  1.07400    2.13570    -5.215400  -2.547800  -3.13900   -0.193810  -1.107400  0.75978    0.73341    0.052985
17     .              1.65170    -1.963400  -0.60317   -1.44970   -4.645600  -2.654800  1.787100   2.00860    2.55950    ...  -2.95930   0.74480    2.189800   0.798260   2.64470    -1.984700  -3.354100  -0.39062   -1.83260   -3.034700
=====  =============  =========  =========  =========  =========  =========  =========  =========  =========  =========  ===  =========  =========  =========  =========  =========  =========  =========  =========  =========  =========

18 rows × 301 columns


Calcular similitudes entre textos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finalmente, y aunque hay un módulo de **ConTexto** dedicado exclusivamente al cálculo de distancias y similitudes entre textos, los objetos de la clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>` cuentan con la función :py:func:`similitud_textos() <vectorizacion.VectorizadorWord2Vec.similitud_textos>`, para medir la similitud entre dos palabras o textos.

.. code-block:: python

    >>> ## 3.5 Similitudes entre textos
    >>> '''
    >>> Esta función aprovecha las facilidades de la librería Spacy para medir la
    >>> similaridad entre 2 palabras o textos.
    >>> '''
    >>> t1 = 'los perros y los gatos suelen pelear mucho.'
    >>> t2 = 'caninos y felinos entran en disputas con frecuencia.'
    >>> t3 = 'este tercer texto habla sobre un tema distinto a los otros dos'
    
    >>> for i in [t1, t2]:
    >>>     for j in [t2, t3]:
    >>>         if i != j:
    >>>             similitud = v_word2vec.similitud_textos(i, j)
    >>>             print('-----------------------')
    >>>             print(f'Texto 1: {i}')
    >>>             print(f'Texto 2: {j}')
    >>>             print(f'Similitud entre textos: {similitud}')
    
    -----------------------
    Texto 1: los perros y los gatos suelen pelear mucho.
    Texto 2: caninos y felinos entran en disputas con frecuencia.
    Similitud entre textos: 0.6875509408308378
    -----------------------
    Texto 1: los perros y los gatos suelen pelear mucho.
    Texto 2: este tercer texto habla sobre un tema distinto a los otros dos
    Similitud entre textos: 0.5168476867313971
    -----------------------
    Texto 1: caninos y felinos entran en disputas con frecuencia.
    Texto 2: este tercer texto habla sobre un tema distinto a los otros dos
    Similitud entre textos: 0.4299091504956323


Vectorización utilizando *document embeddings* - Doc2Vec
--------------------------------------------------------

La clase :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>` utiliza por debajo las funcionalidades de la librería 
`Gensim <https://radimrehurek.com/gensim/>`_ para entrenar un vectorizador en un corpus o conjunto de textos, de manera que sea capaz de representar documentos mediante *embeddings*, o representaciones vectoriales densas. Estas *embeddings* son representaciones de un número de elementos definido por el usuario. Tanto para entrenar el vectorizador como para utilizarlo posteriormente, es necesario hacer un procesamiento sobre los textos de entrada. Las funciones internas de la clase :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>` se encargan de este procesamiento.

Inicializar y entrenar el vectorizador
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al igual que los vectorizadores basados en frecuencias (`ver sección <07_vectorizacion_de_textos.html#vectorizaciones-por-frecuencia-de-terminos>`__) , los objetos de clase :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>` deben ser entrenados o ajustados sobre un corpus de textos. El primer paso es inicializar el objeto del vectorizador; para esto, se deben definir los siguientes parámetros:

- Número de elementos que tendrán los vectores
- Frecuencia mínima que debe tener cada término en el corpus para ser tenido en cuenta en el modelo. Esto se utiliza para evitar que términos muy poco frecuentes afecten el entrenamiento.
- Número de iteraciones (épocas) que realiza la red neuronal al entrenar el modelo.

En este ejemplo el corpus de entrenamiento es muy pequeño (5 textos cortos), y ninguna palabra cumple con el parámetro *minima_cuenta=5* (valor por defecto). Esto puede generar errores, por lo que en este caso se cambia este parámetro a 1 (valor mínimo).

Adicionalmente, al entrenar el vectorizador, por medio del método `entrenar_modelo`, se utiliza el parámetro *archivo_salida* (opcional) para guardar el modelo entrenado en la ubicación establecida por el usuario.

.. code-block:: python

    >>> ## Inicializar el vectorizador
    >>> # Se configura para que tenga 100 elementos y se entrene por 25 épocas
    >>> v_doc2vec = VectorizadorDoc2Vec(n_elementos=100, epocas=25, minima_cuenta=1)
    
    >>> ## Entrenar el modelo en un corpus
    >>> v_doc2vec.entrenar_modelo(textos_limpios, archivo_salida='salida/v_doc2vec.pk')

Vectorizar textos utilizando el vectorizador
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al igual que con los otros vectorizadores, el método `vectorizar` acepta un texto o una lista de textos como entrada y devuelve un arreglo numpy de dos dimensiones con los vectores generados. Normalmente, esta operación de vectorización puede producir diferentes vectores para un mismo texto de entrada, que aunque tienen valores distintos, son similares entre sí en el espacio *n_elementos*-dimensional.

Sin embargo, la clase :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>` cuenta con una semilla para asegurar que siempre se obtenga el mismo vector para el mismo texto de entrada.

.. code-block:: python

    >>> vector = v_doc2vec.vectorizar(texto_nuevo)
    >>> print("Dimensiones del vector:", vector.shape)
    >>> print("Primeros 10 elementos del vector:\n", vector[0,:10])

    Dimensiones del vector: (1, 100)
    Primeros 10 elementos del vector: 
     [ 0.00011651 -0.00289909 -0.00298333 -0.00355879  0.00197437  0.00171644
      0.00276862  0.00240826  0.00056794 -0.00210888]


Cargar un vectorizador entrenado previamente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previamente vimos cómo se puede guardar un vectorizador entrenado, por medio del parámetro *archivo_salida* de la función `entrenar_modelo`. Este vectorizador, ya ajustado, se puede cargar y utilizar, al momento de definir un nuevo objeto de la clase :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>`. Para cargar un vectorizador ajustado previamente se debe utilizar el parámetro *archivo_modelo*, especificando dónde está el archivo con el vectorizador ya ajustado. Al usar esta opción, los demás parámetros de inicialización no serán tenidos en cuenta, pues esos parámetros se tomarán del vectorizador cargado.

.. code-block:: python

    >>> ## Cargar un vectorizador entrenado previamente
    >>> v_doc2vec_2 = VectorizadorDoc2Vec(archivo_modelo='salida/v_doc2vec.pk')

    >>> # Se vectoriza el mismo texto con el vectorizador cargado
    >>> vector_2 = v_doc2vec_2.vectorizar(texto_nuevo)

    >>> # Se comprueba que ambos vectores resultantes sean iguales
    >>> np.all(vector == vector_2)

    True
