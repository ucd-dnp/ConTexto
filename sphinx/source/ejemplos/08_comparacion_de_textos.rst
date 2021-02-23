.. _08_comparacion_de_textos:

Comparación de textos
=====================

Este ejemplo muestra las principales funcionalidades del módulo :py:mod:`Comparación <comparacion>`, de la librería. Este módulo permite calcular distintas métricas de distancia y similitud entre dos o mas textos. La capacidad para cuantificar qué tan similares o diferentes son un grupo de textos o cadenas de caracteres entre sí puede ser muy útil para ciertos procesos como detección de textos atípicos, identificación de afinidad entre documentos y estandarización de valores *string*, entre otros.

Importar paquetes necesarios y adecuar textos de prueba
-------------------------------------------------------

El primer paso es importar las tres clases del módulo de `comparacion` con las que se va a trabajar, y definir los textos para correr los ejemplos.

.. code-block:: python

    >>> from contexto.comparacion import Similitud, Distancia, DiferenciaStrings
    >>> from contexto.vectorizacion import *

    >>> # Textos para probar las medidas de similitud y distancia
    >>> textos_prueba = [
    >>>     'primero de los dos textos de prueba',
    >>>     'segundo de los textos de evaluación',
    >>>     'una tercera oración que se empieza a alejar de los textos anteriores',
    >>>     'este no tiene ninguna relación con nada'
    >>> ]

    >>> otros_textos = [
    >>>     'primer texto del segundo grupo de prueba',
    >>>     'segundo de la segunda lista de textos'
    >>> ]

Adicionalmente, para el cálculo de varias distancias y similitudes es necesaria una representación numérica o vectorial de los textos. Para esto se puede trabajar directamente con los vectores que representan cada uno de los textos, o se puede utilizar alguno de los vectorizadores del módulo :py:mod:`Vectorización <vectorizacion>`.

En este ejemplo se van a probar ambas opciones, por lo que es necesario inicializar los vectorizadores que se van a utilizar y también obtener las representaciones vectoriales de los textos de prueba.

.. code-block:: python

    >>> ## Preparar los insumos
    
    >>> # Definir algunos vectorizadores para hacer diferentes pruebas
    >>> v_bow = VectorizadorFrecuencias()
    >>> v_tf = VectorizadorFrecuencias(tipo='tfidf', idf=False)
    >>> v_tfidf = VectorizadorFrecuencias(tipo='tfidf')
    >>> v_hashing = VectorizadorHash()
    >>> v_word2vec = VectorizadorWord2Vec()
    
    >>> # Ajustar los vectorizadores (cuando aplique) al corpus de textos
    >>> v_bow.ajustar(textos_prueba)
    >>> v_tf.ajustar(textos_prueba)
    >>> v_tfidf.ajustar(textos_prueba)
    
    >>> # Obtener representaciones vectoriales de los textos y guardarlas en un diccionario
    >>> vectores = {}
    >>> llaves = ['bow', 'tf', 'tfidf', 'hash', 'word2vec']
    >>> for i, v in enumerate([v_bow, v_tf, v_tfidf, v_hashing, v_word2vec]):
    >>>     vectores[llaves[i]] = v.vectorizar(textos_prueba)


Medidas de similitud entre textos
---------------------------------

La clase :py:class:`Similitud <comparacion.Similitud>` permite calcular dos métricas de similitud, coseno y Jaccard, para cuantificar qué tan parecidos son dos textos entre sí. Entre más alto sea el valor de similitud (valor máximo es 1), más similares serán los dos textos.

Inicializar los objetos de clase `Similitud`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al inicializar los objetos de clase :py:class:`Similitud <comparacion.Similitud>` se pasa como parámetro un vectorizador para poder obtener las representaciones vectoriales de los textos de entrada que se le pasen. Si no se pasa ningún vectorizador, por defecto inicializará uno de la clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>`, del idioma especificado por el usuario (por defecto: español). Si a los métodos del objeto de clase :py:class:`Similitud <comparacion.Similitud>` se pasan vectores en vez de textos como entrada, no importa qué vectorizador tenga, pues no lo utilizará.

Es importante recalcar que si se pasa un vectorizador al objeto de Similitud, este ya debe estar ajustado, en caso de que aplique. Esto es particularmente relevante para los vectores de clases :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>` y :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>`.

.. code-block:: python

    >>> ## Inicializar objetos de clase Similitud
    >>> 
    >>> s_bow = Similitud(v_bow)
    >>> s_tf = Similitud(v_tf)
    >>> s_tfidf = Similitud(v_tfidf)
    >>> s_hashing = Similitud(v_hashing)
    >>> s_word2vec = Similitud(v_word2vec)

Similitud coseno
~~~~~~~~~~~~~~~~

La similitud coseno es un valor entre -1 y 1 que mide qué tan "alineados" están dos vectores. Este valor se puede obtener al llamar el método :py:meth:`coseno() <comparacion.Similitud.coseno>` del objeto de clase :py:class:`Similitud <comparacion.Similitud>`. Como argumentos se pueden pasar:

* Dos textos (o vectores). En este caso se retornará un arreglo de numpy de dos dimensiones, con el valor de la similitud entre las dos entradas.
* Una lista de *n* textos (o vectores). En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *nxn* simétrica, en donde la posición *i,j* muestra la similitud del texto/vector *i* con el texto/vector *j*.
* Dos listas de *n1* y *n2* textos (o vectores), respectivamente. En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *n1xn2*, en donde la posición *i,j* muestra la similitud del texto/vector *i* de la primera lista con el texto/vector *j* de la segunda lista.

Los vectorizadores basados en frecuencias (sin consideraciones adicionales, como tener en cuenta la frecuencia inversa IDF) arrojarán resultados muy similares al medir la similitud coseno, incluso si los valores de los vectores generados no son los mismos.

.. code-block:: python

    >>> ## Calcular similitudes con vectorizadores basados en frecuencias de términos
    >>> coseno_bow = s_bow.coseno(textos_prueba)
    >>> coseno_tf = s_tf.coseno(textos_prueba)
    >>> coseno_hashing = s_hashing.coseno(textos_prueba)
    
    >>> # La vectorización TF-IDF tiene unos resultados distintos
    >>> coseno_tfidf = s_tfidf.coseno(textos_prueba)
    
    >>> print('Similitudes entre los textos de prueba (BOW, TF o HASHING):')
    >>> print(coseno_bow)
    >>> print('----------\nSimilitudes entre los textos de prueba (TF-IDF):')
    >>> print(coseno_tfidf,'\n')

    Similitudes entre los textos de prueba (BOW, TF o HASHING):
    [[1.         0.70710678 0.40201513 0.        ]
     [0.70710678 1.         0.42640143 0.        ]
     [0.40201513 0.42640143 1.         0.        ]
     [0.         0.         0.         1.        ]]
    ----------
    Similitudes entre los textos de prueba (TF-IDF):
    [[1.         0.49693115 0.22998344 0.        ]
     [0.49693115 1.         0.25454493 0.        ]
     [0.22998344 0.25454493 1.         0.        ]
     [0.         0.         0.         1.        ]] 

En general, los vectorizadores basados en frecuencias tendrán diferencias mayores dependiendo de las palabras que estén presentes en los textos. Los vectorizadores densos como word2vec o doc2vec son menos radicales, lo que permite encontrar similitud entre textos con significados parecidos, incluso si no tienen tantas palabras en común.

También es posible ingresar directamente los vectores pre-calculados. Esto debería arrojar los mismos resultados que ingresando los textos, siempre y cuando se haya utilizado el mismo vectorizador.

.. code-block:: python

    >>> coseno_doc2vec = s_word2vec.coseno(textos_prueba)
    >>> print('Similitudes entre los textos de prueba (Word2Vec):')
    >>> print(coseno_doc2vec)
    
    >>> coseno_tfidf_vec = s_tfidf.coseno(vectores['tfidf'])
    >>> iguales = (coseno_tfidf == coseno_tfidf_vec).all()
    >>> print('-----------')
    >>> print('Igualdad entre utilizar los textos directamente o sus representaciones vectoriales:', iguales,'\n')
    
    Similitudes entre los textos de prueba (Word2Vec):
    [[1.0000001  0.9347326  0.6558729  0.23863341]
     [0.9347326  0.9999998  0.64198124 0.22747502]
     [0.6558729  0.64198124 0.9999997  0.49457312]
     [0.23863341 0.22747502 0.49457312 1.0000004 ]]
    -----------
    Igualdad entre utilizar los textos directamente o sus representaciones vectoriales: False

En este caso la validación dio que las representaciones vectoriales no son exactamente iguales. Esto se debe al grado de precisión que tiene Python para manejar números muy pequeños, el cual tiene cierto margen de error.

Sin embargo, si se mira la diferencia entre ambos objetos, se puede ver que son prácticamente la mísma representación numérica.

.. code-block:: python

    >>> print('Diferencia entre utilizar los textos directamente o sus representaciones vectoriales:\n')
    >>> print(coseno_tfidf - coseno_tfidf_vec)

    Diferencia entre utilizar los textos directamente o sus representaciones vectoriales:

    [[0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00]
     [0.00000000e+00 2.22044605e-16 0.00000000e+00 0.00000000e+00]
     [0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00]
     [0.00000000e+00 0.00000000e+00 0.00000000e+00 2.22044605e-16]]

Similitud de Jaccard
~~~~~~~~~~~~~~~~~~~~

La similitud de Jaccard es un valor entre 0 y 1 que mide cuántos elementos tienen en común dos vectores, al calcular la intersección sobre la unión de los elementos. Este valor se puede obtener al llamar el método :py:meth:`jaccard() <comparacion.Similitud.jaccard>` del objeto de clase :py:class:`Similitud <comparacion.Similitud>`. Las entradas y salidas de este método son iguales a las del método :py:meth:`coseno() <comparacion.Similitud.coseno>`.

El cálculo de la similitud de Jaccard funciona bien con vectorizadores basados en frecuencias (BOW, TF-IDF, Hashing), o directamente con los textos sin vectorizar, aunque en este segundo caso pueden presentarse resultados distintos. Esto se debe a que, sí se pasan directamente los textos sin vectorizar, la "unión" de elementos se definirá como todos los términos que aparecen en por lo menos uno de los dos textos. Por otro lado, si se usa, por ejemplo, un vectorizador BOW con un vocabulario más amplio para hacer la vectorización, es posible que hayan palabras en dicho vocabulario que cuentan en la unión de elementos, pero realmente no están en ninguno de los dos textos a comparar.

.. code-block:: python

    >>> # Utilizar el parámetro "vectorizar=True" debería dar el mismo resultado
    >>> # que aplicar la función directamente sobre vectores pre computados
    >>> a = s_bow.jaccard(textos_prueba, vectorizar=True)
    >>> b = s_bow.jaccard(vectores['bow'])
    >>> print((a == b).all())
    
    >>> # Al aplicar la función directamente sobre los textos, los resultados pueden
    >>> # variar, dado que solo se toma en cuenta el vocabulario de cada par de textos
    >>> # a comparar (a diferencia del vocabulario total del corpus que se tiene en 
    >>> # cuenta en el vectorizador)
    >>> c = s_bow.jaccard(textos_prueba)
    >>> a == c

    True
    array([[ True,  True, False,  True],
           [ True,  True, False,  True],
           [False, False,  True,  True],
           [ True,  True,  True,  True]])

Mientras los vectorizadores utilizados sean basados en frecuencias, el cálculo de similitud Jaccard funcionará bien. Por el otro lado, los vectorizadores word2vec y doc2vec generan una representación densa, por lo que no dan buenos resultados al utilizarse en este caso.

.. code-block:: python

    >>> # Cálculo utilizando vectorizadores basados en frecuencias
    >>> jaccard_tfidf = s_tfidf.jaccard(textos_prueba, vectorizar=True)
    >>> jaccard_hashing = s_hashing.jaccard(textos_prueba, vectorizar=True)
    >>> print('Similitudes entre los textos de prueba (TF-IDF o HASHING):')
    >>> print(jaccard_tfidf)
    >>> 
    >>> # Cálculo utilizando word2vec
    >>> jaccard_word2vec = s_word2vec.jaccard(textos_prueba, vectorizar=True)
    >>> print('-------\nSimilitudes entre los textos de prueba (Word2Vec):')
    >>> print(jaccard_word2vec)
    
    Similitudes entre los textos de prueba (TF-IDF o HASHING):
    [[1.         0.375      0.21428571 0.        ]
     [0.375      1.         0.23076923 0.        ]
     [0.21428571 0.23076923 1.         0.        ]
     [0.         0.         0.         1.        ]]
    -------
    Similitudes entre los textos de prueba (Word2Vec):
    [[1. 1. 1. 1.]
     [1. 1. 1. 1.]
     [1. 1. 1. 1.]
     [1. 1. 1. 1.]]


Similitudes entre dos grupos de textos distintos 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como se mencionó anteriormente, es posible medir la similitud entre dos grupos de textos distintos. Para esto, se deben introducir como argumentos dos listas de textos o vectores distintas. Los métodos de la clase :py:class:`Similitud <comparacion.Similitud>` calcularán la similitud indicada entre cada uno de los elementos de la primera lista y cada uno de los elementos de la segunda lista.

.. code-block:: python

    >>> jaccard_bow = s_bow.jaccard(textos_prueba, otros_textos)
    >>> coseno_word2vec = s_word2vec.coseno(textos_prueba, otros_textos[0])
    >>> 
    >>> print('Similitudes de Jaccard entre dos grupos de textos (BOW):')
    >>> print(jaccard_bow)
    >>> 
    >>> print('-------\nSimilitudes coseno entre los textos de prueba y otro texto (Word2Vec):')
    >>> print(coseno_word2vec)
    
    Similitudes de Jaccard entre dos grupos de textos (BOW):
    [[0.18181818 0.2       ]
     [0.2        0.375     ]
     [0.05555556 0.125     ]
     [0.         0.        ]]
    -------
    Similitudes coseno entre los textos de prueba y otro texto (Word2Vec):
    [[0.70599896]
     [0.77385116]
     [0.4849984 ]
     [0.24222623]]


Medidas de distancia entre textos
---------------------------------

La clase :py:class:`Distancia <comparacion.distancia>` permite calcular varias métricas de distancia para cuantificar qué tan diferentes son dos textos entre sí. Entre más bajo sea el valor de distancia (valor mínimo es 0), más similares serán los dos textos.

Inicializar los objetos de clase `Distancia`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al inicializar los objetos de clase :py:class:`Distancia <comparacion.distancia>` se pasa como parámetro un vectorizador para poder obtener las representaciones vectoriales de los textos de entrada que se le pasen. Si no se pasa ningún vectorizador, por defecto inicializará uno de la clase :py:class:`VectorizadorWord2Vec <vectorizacion.VectorizadorWord2Vec>`, del idioma especificado por el usuario (por defecto: español). Si a los métodos del objeto de clase :py:class:`Distancia <comparacion.distancia>` se pasan vectores en vez de textos como entrada, no importa qué vectorizador tenga, pues no lo utilizará.

Es importante recalcar que si se pasa un vectorizador al objeto de Similitud, este ya debe estar ajustado, en caso de que aplique. Esto es particularmente relevante para los vectores de clases :py:class:`VectorizadorFrecuencias <vectorizacion.VectorizadorFrecuencias>` y :py:class:`VectorizadorDoc2Vec <vectorizacion.VectorizadorDoc2Vec>`.

.. code-block:: python

    >>> ## Inicializar objetos de clase Distancia
    >>> d_bow = Distancia(v_bow)
    >>> d_tf = Distancia(v_tf)
    >>> d_tfidf = Distancia(v_tfidf)
    >>> d_hashing = Distancia(v_hashing)
    >>> d_word2vec = Distancia(v_word2vec)


Métricas de distancias
~~~~~~~~~~~~~~~~~~~~~~

La clase :py:class:`Distancia <comparacion.distancia>` permite calcular más de 5 métricas de distancia distintas, que se muestran en las siguientes celdas de este cuaderno. En general, los argumentos de entrada y las salidas funcionan igual al caso de las similitudes. Se tienen los siguientes casos:

* Dos textos (o vectores). En este caso se retornará un arreglo de numpy de dos dimensiones, con el valor de la distancia entre las dos entradas.
* Una lista de *n* textos (o vectores). En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *nxn* simétrica, en donde la posición *i,j* muestra la distancia del texto/vector *i* con el texto/vector *j*.
* Dos listas de *n1* y *n2* textos (o vectores), respectivamente. En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *n1xn2*, en donde la posición *i,j* muestra la distancia del texto/vector *i* de la primera lista con el texto/vector *j* de la segunda lista.

En este caso, los valores de distancias generalmente variarán dependiendo del vectorizador utilizado (a diferencia de las similitudes, que en algunos casos calculaban los mismos valores para vectorizadores distintos). En todo caso, a pesar de que cambien los valores y las escalas, en general sí se debería mantener un mismo orden. Es decir, textos más cercanos y más lejanos entre sí deberían mantener este comportameniento sin importar el vectorizador utilizado.

.. code-block:: python

    >>> ## Métricas de distancia definidas
    
    >>> # Distancia L1
    >>> l1_bow = d_bow.l1(textos_prueba)
    
    >>> # Distancia L2
    >>> l2_word2vec =d_word2vec.l2(textos_prueba)
    
    >>> # Distancia Hamming
    >>> hamming_hashing = d_hashing.hamming(textos_prueba)
    
    >>> print('Distancias L2 entre los textos de prueba (Word2Vec):')
    >>> print(l2_word2vec)
    >>> print('-----\nDistancias de Hamming entre los textos de prueba (HASHING):')
    >>> print(hamming_hashing)

    Distancias L2 entre los textos de prueba (Word2Vec):
    [[ 0.       10.218398 20.964655 31.797607]
     [10.218398  0.       22.503887 33.3239  ]
     [20.964655 22.503887  0.       23.959114]
     [31.797607 33.3239   23.959114  0.      ]]
    -----
    Distancias de Hamming entre los textos de prueba (HASHING):
    [[0.   0.08 0.14 0.13]
     [0.08 0.   0.13 0.12]
     [0.14 0.13 0.   0.18]
     [0.13 0.12 0.18 0.  ]]

La distancia Minkowski es una generalización de las operaciones que se utilizan para calcular la distancia L1 o L2. El parámetro p permite definir el grado a utilizar en el cálculo de la distancia.

Por ejemplo, si p=1, se calculará la distancia L1 y si p=2 se calculará la distancia L2.

.. code-block:: python

    >>> ## Distancia Minkowski 

    >>> # Distancia con grado 3
    >>> l3_tfidf =d_tfidf.minkowski(textos_prueba, p=3) 

    >>> # Misma distancia L2
    >>> minkowski_2_word2vec = d_word2vec.minkowski(textos_prueba, p=2) 
    >>> iguales = (l2_word2vec == minkowski_2_word2vec).all()

    >>> print('Distancias de Minkowski (grado 3) entre los textos de prueba (TF-IDF):')
    >>> print(l3_tfidf)
    >>> print('-----\nDistancias de Minkowski grado 2 iguales a distancias L2 (Word2Vec):', iguales, '\n')

    Distancias de Minkowski (grado 3) entre los textos de prueba (TF-IDF):
    [[0.         0.76622556 0.82452962 0.93553864]
     [0.76622556 0.         0.82547379 0.95425713]
     [0.82452962 0.82547379 0.         0.88428327]
     [0.93553864 0.95425713 0.88428327 0.        ]]
    -----
    Distancias de Minkowski grado 2 iguales a distancias L2 (Word2Vec): True

Una de las distancias que se pueden calcular es la distancia de Jaccard. Esta distancia es complementaria a la similitud de Jaccard, por lo que la suma de ambas medidas siempre debe ser igual a 1.

.. code-block:: python

    >>> # Distancia Jaccard
    >>> jaccard_tfidf = d_tfidf.jaccard(textos_prueba)
    >>> 
    >>> # La suma de la distancia y similitud de jaccard entre dos vectores debería dar 1
    >>> jaccard_tfidf + s_tfidf.jaccard(textos_prueba, vectorizar=True)

    array([[1., 1., 1., 1.],
           [1., 1., 1., 1.],
           [1., 1., 1., 1.],
           [1., 1., 1., 1.]])

Otras métricas de distancias
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adicionalmente a las funciones que la clase :py:class:`Distancia <comparacion.distancia>` trae implementadas, el método :py:meth:`distancia_pares() <comparacion.Distancia.distancia_pares>` permite calcular otras distancias, que se especifican por medio del parámetro *tipo_distancia*. Las métricas que se pueden utilizar son las soportadas por scikit-learn y scipy. Para mayor información, se puede consultar la 
`documentación de scikit-learn <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html>`_ .

Algunas de estas métricas pueden requerir o aceptar argumentos adicionales. Estos parámetros pueden ser pasados al método :py:meth:`distancia_pares() <comparacion.Distancia.distancia_pares>` con el mismo nombre con el que aparezcan en la documentación de scikit-learn y `la documentación de scipy <https://docs.scipy.org/doc/scipy/reference/spatial.distance.html>`_ .

.. code-block:: python

    >>> # Algunos ejemplos:
    >>> chebyshev_word2vec = d_word2vec.distancia_pares(textos_prueba, tipo_distancia='chebyshev')
    >>> rogerstanimoto_bow = d_bow.distancia_pares(textos_prueba, tipo_distancia='rogerstanimoto')
    >>> braycurtis_tfidf = d_tfidf.distancia_pares(textos_prueba, tipo_distancia='braycurtis')
    >>> 
    >>> print('\n ::: Distancia chebyshev')
    >>> print(chebyshev_word2vec)
    >>> 
    >>> print('\n::: Distancia rogerstanimoto')
    >>> print(rogerstanimoto_bow)
    >>> 
    >>> print('\n::: Distancia braycurtis')
    >>> print(braycurtis_tfidf)
    
     ::: Distancia chebyshev
    [[0.         1.83772638 3.40704679 6.52587652]
     [1.83772638 0.         3.68807423 6.6068573 ]
     [3.40704679 3.68807423 0.         4.78639138]
     [6.52587652 6.6068573  4.78639138 0.        ]]
    
    ::: Distancia rogerstanimoto
    [[0.         0.35714286 0.64705882 0.72222222]
     [0.35714286 0.         0.60606061 0.68571429]
     [0.64705882 0.60606061 0.         0.87804878]
     [0.72222222 0.68571429 0.87804878 0.        ]]
    
    ::: Distancia braycurtis
    [[0.         0.51793548 0.77659126 1.        ]
     [0.51793548 0.         0.76752362 1.        ]
     [0.77659126 0.76752362 0.         1.        ]
     [1.         1.         1.         0.        ]]


Distancias entre dos grupos de textos distintos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como se mencionó anteriormente, es posible medir la distancia entre dos grupos de textos distintos. Para esto, se deben introducir como argumentos dos listas de textos o vectores distintas. Los métodos de la clase :py:class:`Distancia <comparacion.distancia>` calcularán la distancia indicada entre cada uno de los elementos de la primera lista y cada uno de los elementos de la segunda lista.

Esto aplica para cualquiera de los métodos de la clase :py:class:`Distancia <comparacion.distancia>`.

.. code-block:: python

    >>> l1_hash = d_hashing.l1(textos_prueba, otros_textos)
    >>> braycurtis_tfidf = d_tfidf.distancia_pares(vectores['tfidf'], otros_textos[0], tipo_distancia='braycurtis')
    >>> 
    >>> print('Distancias L1 entre dos grupos de textos (HASHING):')
    >>> print(l1_hash)
    >>> 
    >>> print('-------\nDistancias (disimilitud) de Bray–Curtis entre los textos de prueba y otro texto (TF-IDF):')
    >>> print(braycurtis_tfidf)

    Distancias L1 entre dos grupos de textos (HASHING):
    [[3.55648903 2.66666667]
     [3.30403593 1.78798701]
     [5.35935341 4.44391275]
     [5.29150262 4.97908464]]
    -------
    Distancias (disimilitud) de Bray–Curtis entre los textos de prueba y otro texto (TF-IDF):
    [[0.58829081]
     [0.54109359]
     [0.91533873]
     [1.        ]]


Diferencias entre textos a nivel de caracteres
-------------------------------------------------

Finalmente, la clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>` permite calcular métricas, tanto de similitud como de distancia, para cuantificar a nivel de caracteres qué tan parecidos o diferentes son dos textos entre sí. Esta clase se recomienda para comparaciones de cadenas de caracteres (strings) relativamente cortas, como nombres, direcciones y otras cadenas de caracteres similares. Para textos más largos, se recomiendan las clases :py:class:`Similitud <comparacion.similitud>` y/o :py:class:`Distancia <comparacion.distancia>`.

Definir textos de prueba e inicializar objeto de clase DiferenciaStrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como se mencionó anteriormente, esta clase funciona mejor con textos cortos, por lo que se definen 4 strings más cortos para correr el ejemplo. También se define un objeto de clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>`, que contiene todos los métodos necesarios para calcular las similitudes y distancias.

.. code-block:: python

    >>> ## Textos de prueba
    >>> t1 = 'pescado'
    >>> t2 = 'pecsado'
    >>> t3 = 'Jonhatan Ruiz Diaz'
    >>> t4 = 'Jonatan Ruis Díaz'
    >>> strings = [t1, t2, t3, t4]
    ​
    >>> ## Inicializar objeto de clase Distancia
    >>> dif_strings = DiferenciaStrings()


Cálculo de medidas de distancia y similitud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>` utiliza por debajo la librería jellyfish para calcular las diferencias y similitudes a niveles de caracteres. Para mayor información sobre las medidas disponibles y en qué consiste cada una, se puede consultar la 
`documentación de jellyfish <https://jellyfish.readthedocs.io/en/latest/comparison.html>`_.

Para todos los métodos de esta clase, las entradas y salidas funcionan muy similar a los vistos anteriormente para `Similitud` y `Distancia`:

* Dos textos. En este caso se retornará un arreglo de numpy de dos dimensiones, con el valor de la comparación entre las dos entradas.
* Una lista de *n* textos. En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *nxn* simétrica, en donde la posición *i,j* muestra la comparación del texto/vector *i* con el texto/vector *j*.
* Dos listas de *n1* y *n2* textos, respectivamente. En este caso se retornará un arreglo de numpy de dos dimensiones, que representa una matriz de *n1xn2*, en donde la posición *i,j* muestra la comparación del texto *i* de la primera lista con el texto *j* de la segunda lista.

La gran diferencia en este caso es que la clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>` no utiliza representaciones vectoriales de los textos, por lo que siempre deben ingresarse los textos a comparar en forma de *strings*.

.. code-block:: python

    >>> ## Diferencia entre dos textos
    >>> d1 = dif_strings.distancia_levenshtein(t3,t4)
    >>> d2 = dif_strings.distancia_damerau_levenshtein(t1,t2)
    >>> d3 = dif_strings.distancia_hamming(strings) 
    ​>>> 
    >>> print('Distancia de Levenshtein entre 2 textos de prueba:')
    >>> print(d1)
    >>> print('------\nDistancias de Hamming entre los textos de prueba:')
    >>> print(d3)

    Distancia de Levenshtein entre 2 textos de prueba:
    [[3.]]
    ------
    Distancias de Hamming entre los textos de prueba:
    [[ 0.  2. 17. 17.]
     [ 2.  0. 17. 17.]
     [17. 17.  0. 15.]
     [17. 17. 15.  0.]]
     ​
.. code-block:: python

    >>> ## Similitud entre strings
    
    >>> # Similitud entre dos textos
    >>> s1 = dif_strings.similitud_jaro(t1,t2)
    >>> # Similitud entre lista de textos
    >>> s2 = dif_strings.similitud_jaro_winkler(strings)
    ​
    >>> print('Similitud de Jaro entre 2 textos de prueba:')
    >>> print(s1)
    >>> print('------\nSimilitudes de Jaro Winkler entre los textos de prueba:')
    >>> print(s2)

    Similitud de Jaro entre 2 textos de prueba:
    [[0.95238095]]
    ------
    Similitudes de Jaro Winkler entre los textos de prueba:
    [[1.         0.96190476 0.2989418  0.30112045]
     [0.96190476 1.         0.2989418  0.30112045]
     [0.2989418  0.2989418  1.         0.90254902]
     [0.30112045 0.30112045 0.90254902 1.        ]]

Normalización de medidas de distancia
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para los métodos de distancia (:py:meth:`distancia_levenshtein() <comparacion.DiferenciaStrings.distancia_levenshtein>`, :py:meth:`distancia_damerau_levenshtein() <comparacion.DiferenciaStrings.distancia_damerau_levenshtein>` y :py:meth:`distancia_hamming() <comparacion.DiferenciaStrings.distancia_hamming>`) es posible utilizar el parámetro norm, que por defecto es igual a None, para normalizar la distancia calculada.

Si norm=1, se dividirá la distancia encontrada por la longitud (número de caracteres) del texto más corto de los dos a comparar. Si norm=2, se dividirá la distancia encontrada por la longitud (número de caracteres) del texto más largo. En este segundo caso se puede garantizar que el valor resultante será un número entre 0 y 1.

.. code-block:: python

    >>> # Diferencia entre lista de textos
    >>> d1 = dif_strings.distancia_damerau_levenshtein(strings)

    >>> # Normalizar dividiendo por el texto más corto
    >>> d2= dif_strings.distancia_damerau_levenshtein(strings, norm=1)

    >>> # Normalizar dividiendo por el texto más largo (se garantiza que queda entre 0 y 1)
    >>> d3= dif_strings.distancia_damerau_levenshtein(strings, norm=2)
    ​​
    >>> print('Distancia de Damerau Levenshtein, sin normalizar:')
    >>> print(d1)
    >>> print('------\nDistancia de Damerau Levenshtein, dividiendo por longitud de texto corto:')
    >>> print(d2)
    >>> print('------\nDistancia de Damerau Levenshtein, dividiendo por longitud de texto largo:')
    >>> print(d3)

    Distancia de Damerau Levenshtein, sin normalizar:
    [[ 0.  1. 17. 16.]
     [ 1.  0. 17. 16.]
     [17. 17.  0.  3.]
     [16. 16.  3.  0.]]
    ------
    Distancia de Damerau Levenshtein, dividiendo por longitud de texto corto:
    [[0.         0.14285714 2.42857143 2.28571429]
     [0.14285714 0.         2.42857143 2.28571429]
     [2.42857143 2.42857143 0.         0.17647059]
     [2.28571429 2.28571429 0.17647059 0.        ]]
    ------
    Distancia de Damerau Levenshtein, dividiendo por longitud de texto largo:
    [[0.         0.14285714 0.94444444 0.94117647]
     [0.14285714 0.         0.94444444 0.94117647]
     [0.94444444 0.94444444 0.         0.16666667]
     [0.94117647 0.94117647 0.16666667 0.        ]]


Comparaciones entre dos grupos de strings distintos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Como se mencionó anteriormente, es posible comparar dos grupos de textos distintos. Para esto, se deben introducir como argumentos dos listas de textos distintas. Los métodos de la clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>` calcularán la métrica de similitud o distancia indicada entre cada uno de los elementos de la primera lista y cada uno de los elementos de la segunda lista.

Esto aplica para cualquiera de los métodos de la clase :py:class:`DiferenciaStrings <comparacion.DiferenciaStrings>`.

.. code-block:: python

    >>> d1 = dif_strings.distancia_levenshtein(strings, 'pescados', norm=2)
    >>> s1 = dif_strings.similitud_jaro_winkler(strings, ['pescador', 'John Díaz'])

    >>> print('Distancias de Levenshtein entre un grupo de strings y otro texto, dividiendo por longitud de texto largo:')
    >>> print(d1)

    >>> print('-------\nSimilitudes de Jaro-Winkler entre dos grupos de strings:')
    >>> print(s1)

    Distancias de Levenshtein entre un grupo de strings y otro texto, dividiendo por longitud de texto largo:
    [[0.125     ]
     [0.375     ]
     [0.94444444]
     [0.88235294]]
    -------
    Similitudes de Jaro-Winkler entre dos grupos de strings:
    [[0.975      0.41798942]
     [0.92857143 0.41798942]
     [0.28703704 0.62698413]
     [0.28921569 0.54989107]]
     