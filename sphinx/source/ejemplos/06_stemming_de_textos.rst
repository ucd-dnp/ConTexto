.. _06_stemming_de_textos:

Stemming de textos
==================

Este ejemplo muestra las principales funcionalidades del módulo :py:mod:`Stemming <stemming>` de la librería. Este módulo permite aplicar *stemming* a textos. El *stemming* es un método para reducir todas las formas flexionadas de palabras a su "raíz" o "tallo" (*stem*, en inglés), cuando estas comparten una misma raíz. Por ejemplo, las palabras niños, niña y niñez tienen todas la misma raíz: "niñ". A diferencia de la lematización, en donde cada lema es una palabra que existe en el vocabulario del lenguaje correspondiente, las palabras raíz que se obtienen al aplicar *stemming* no necesariamente existen por sí solas como palabra. Aplicar *stemming* a textos puede simplificarlos, al unificar palabras que comparten la misma raíz, y evitando así tener un vocabulario más grande de lo necesario.


Importar funciones necesarias y defición de textos de prueba
------------------------------------------------------------

En este caso se importa la función :py:func:`stemming.stem_texto`, que aplica *stemming* a un texto de entrada, y la clase :py:class:`Stemmer <stemming.Stemmer>`, que puede ser utilizada directamente, entre otras cosas, para agilizar el proceso de hacer *stemming* a una lista de varios textos. Adicionalmente, se definen algunos textos para desarrollar los ejemplos.

.. code-block:: python

    >>> import time
    >>> from contexto.stemming import Stemmer, stem_texto

    >>> # textos de prueba
    >>> texto = 'Esta es una prueba para ver si las funciones son correctas y funcionan bien. Perritos y gatos van a la casita'
    >>> texto_limpiar = "Este texto, con signos de puntuación y mayúsculas, ¡será limpiado antes de pasar por la función!"
    >>> texto_ingles = 'This is a test writing to study if these functions are performing well.'
    >>> textos = [
    >>>     "Esta es una primera entrada en el grupo de textos",
    >>>     "El Pibe Valderrama empezó a destacar jugando fútbol desde chiquitin",
    >>>     "De los pájaros del monte yo quisiera ser canario",
    >>>     "Finalizando esta listica, se incluye una última frase un poquito más larga que las anteriores."
    >>> ]

Ejemplo de Stemming
-------------------

La función :py:func:`stemming.stem_texto` se encarga de aplicar *stemming* a un texto de entrada. Esta función tiene parámetros opcionales para determinar el lenguaje del texto de entrada (si es "auto", lo detectará automáticamente). Adicionalmente, el parámetro *limpiar* permite hacer una limpieza básica al texto antes de aplicar el *stemming*.

.. code-block:: python

    >>> # Determinar automáticamente el lenguaje del texto
    >>> texto_stem = stem_texto(texto, 'auto')
    >>> print(texto_stem)

    >>> # Prueba en otro lenguaje
    >>> stem_english = stem_texto(texto_ingles, 'inglés')
    >>> print('-------')
    >>> print(stem_english)

    >>> # Prueba limpiando un texto antes
    >>> print('-------')
    >>> print(stem_texto(texto_limpiar, limpiar=True))

    esta es una prueb par ver si las funcion son correct y funcion bien. perrit y gat van a la casit
    -------
    this is a test write to studi if these function are perform well.
    -------
    este text con sign de puntuacion y mayuscul ser limpi antes de pas por la funcion


*Stemming* de varios textos utilizando un solo objeto de la clase `Stemmer`
---------------------------------------------------------------------------

Si se desea aplicar *stemming* a un conjunto de textos, puede ser más rápido definir un único objeto de clase :py:class:`Stemmer <stemming.Stemmer>` y pasar este objeto en el parámetro *stemmer* de la función :py:func:`stemming.stem_texto`. Al hacer esto puede haber un ahorro de tiempo, pues se evita inicializar un nuevo objeto de clase `Stemmer` para cada texto. Este ahorro de tiempo será mayor a medida que sean más los textos que se desean procesar.

A continuación se muestra una comparación de tiempos para dos opciones:

1. Aplicar *stemming* a una lista de textos, aplicando la función :py:func:`stemming.stem_texto` a cada uno sin ninguna otra consideración.
2. Definir un objeto de clase :py:class:`Stemmer <stemming.Stemmer>` y utilizarlo para procesar la misma lista de textos

.. code-block:: python

    >>> # Opción 1: se inicializa el stemmer en cada texto
    >>> tic = time.time()
    >>> for t in textos:
    >>>     print(stem_texto(t))

    >>> tiempo_1 = time.time() - tic

    >>> # Opción 2: se utiliza solo un lematizador para todos los textos
    >>> print('----------')
    >>> tic = time.time()
    >>> stemmer = Stemmer(lenguaje='español')
    >>> for t in textos:
    >>>     print(stem_texto(t, stemmer=stemmer))

    >>> tiempo_2 = time.time() - tic

    >>> print('\n***************\n')
    >>> print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
    >>> print(f'Tiempo con opción 2: {tiempo_2} segundos\n')

    esta es una primer entrad en el grup de text
    el pib valderram empez a destac jug futbol desd chiquitin
    de los pajar del mont yo quis ser canari
    finaliz esta listic, se inclu una ultim fras un poquit mas larg que las anterior.
    ----------
    esta es una primer entrad en el grup de text
    el pib valderram empez a destac jug futbol desd chiquitin
    de los pajar del mont yo quis ser canari
    finaliz esta listic, se inclu una ultim fras un poquit mas larg que las anterior.

    ***************

    Tiempo con opción 1: 0.005089521408081055 segundos

    Tiempo con opción 2: 0.004584312438964844 segundos
