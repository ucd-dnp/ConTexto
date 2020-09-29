.. _05_lematizacion_de_textos:

Lematización de textos
======================

Este ejemplo muestra las principales funcionalidades del módulo :py:mod:`Lematización <lematizacion>`, de la librería. Este módulo permite realizar lematización de textos, una operación que consiste en transormar las palabras de su forma flexionada (plural, femenino, conjugaciones, etc.) a su lema correspondiente, el cual es el representante de todas las formas flexionadas de una misma palabra. Por ejemplo, las palabras niños, niña y niñito tienen todas el mismo lema: niño. Realizar lematización sobre textos puede simplificarlos, al unificar palabras que comparten el mismo lema, y evitando así tener un vocabulario más grande de lo necesario.


Definir textos de prueba
------------------------

El módulo de lematización de **ConTexto** cuenta con dos lematizadores distintos, cada uno apoyado en una librería de NLP (Procesamiento del Lenguaje Natural) distinta: `spaCy <https://spacy.io/>`_ y `Stanza <https://stanfordnlp.github.io/stanza/>`_. En este ejemplo se mostrará el usto de ambas clases, :py:class:`LematizadorSpacy <lematizacion.LematizadorSpacy>` y :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>`, y de la función :py:func:`lematizacion.lematizar_texto`, que puede utilizar cualquiera de los dos lematizadores.

En primer lugar, se definen los textos que se utilizarán para correr los ejemplos.

.. code-block:: python

    >>> import time
    >>> from contexto.lematizacion import LematizadorSpacy, LematizadorStanza
    >>> from contexto.lematizacion import lematizar_texto

    >>> # textos de prueba
    >>> texto = 'esta es una prueba para ver si las funciones son correctas y funcionan bien. Perritos y gatos van a la casita'
    >>> texto_ingles = 'this is a test writing to study if these functions are performing well'
    >>> textos = [
    >>>     "Esta es una primera entrada en el grupo de textos",
    >>>     "El Pibe Valderrama empezó a destacar jugando fútbol desde chiquitin",
    >>>     "De los pájaros del monte yo quisiera ser canario",
    >>>     "Finalizando esta listica, se incluye una última frase un poquito más larga que las anteriores."
    >>> ]


Lematización de textos utilizando spaCy
---------------------------------------

La función :py:func:`lematizacion.lematizar_texto` se encarga de aplicar lematización a todas las palabras de un texto de entrada. Al realizarse con el lematizador de spaCy, que se utiliza por defecto, el usuario puede elegir el lenguaje y el tamaño del modelo. Para la mayoría de lenguajes hay 3 tamaños de modelos: pequeño ('sm'), mediano ('md') y grande ('lg'). Entre más grande sea el modelo, es posible que tenga un vocabulario más amplio o características adicionales, pero también el archivo del modelo será más grande.

La primera vez que se utilice una combinación particular de lenguaje + tamaño, la librería descargará el modelo correspondiente en el computador del usuario. Para usarlo, se debe reiniciar la sesión y correr la función de nuevo.

.. code-block:: python

    >>> # Lematización con librería Spacy 
    >>> texto_lematizado = lematizar_texto(texto)
    >>> print(texto_lematizado)

    >>> print('----')
    >>> # Prueba en otro lenguaje (en este caso se detecta automáticamente que es inglés)
    >>> lemma_english = lematizar_texto(texto_ingles, 'auto', dim_modelo='small')
    >>> print(lemma_english)

    este ser uno probar parir ver si los funcionar ser correcto y funcionar bien perrito y gato ir a lo casita
    ----
    this be a test write to study if these function be perform well


Agregar lemas personalizados al `LematizadorSpacy`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los modelos cuentan con algunos diccionarios de lemas, que utilizan para aplicar la lematización. Así, por ejemplo, el lematizador sabe que para la palabra "iba", su lema debería ser "ir".

Es posible que el diccionario del lematizador no contenga todos los casos que nos interesan, por lo que es necesario complementar el lematizador. Esto se puede hacer desde un archivo JSON o desde un diccionario de Python.

.. note::
        La carpeta `entrada <https://github.com/ucd-dnp/ConTexto/tree/master/ejemplos/entrada>`_ de la sección de ejemplos del `Repositorio de GitHub de ConTexto <https://github.com/ucd-dnp/ConTexto>`_ tiene insumos que servirán para correr varios ejemplos de la librería **ConTexto**. En este caso en particular, se va a utilizar el archivo `dict_lemas.json`.

.. code-block:: python

    >>> # Agregar lemas desde un archivo
    >>> archivo_lemmas = 'entrada/dict_lemas.json'
    >>> texto_lematizado_v2 = lematizar_texto(texto, dict_lemmas=archivo_lemmas)
    >>> print(texto_lematizado_v2)

    >>> # Agregar desde un diccionario
    >>> segundo_dict = {
    >>>     "casita": "casa",
    >>>     "casitas": "casa",
    >>>     "para": "para",
    >>>     "perrito": "perro",
    >>>     "perritos": "perro",
    >>>     "gatos": "gato"
    >>> }
    >>> texto_lematizado_v3 = lematizar_texto(texto, dict_lemmas=segundo_dict)
    >>> print('------')
    >>> print(texto_lematizado_v3)

    este ser uno probar parir ver si los funcionar ser correcto y funcionar bien perro y gato ir a lo casita
    ------
    este ser uno probar parir ver si los funcionar ser correcto y funcionar bien perro y gato ir a lo casa


Corrección de varios textos utilizando un solo objeto de la clase `LematizadorSpacy`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si se desea lematizar un conjunto de textos, puede ser más rápido definir un único objeto de clase :py:class:`LematizadorSpacy <lematizacion.LematizadorSpacy>`, y pasar este objeto en el parámetro *lematizador* de la función :py:func:`lematizacion.lematizar_texto`. Al hacer esto puede haber un ahorro de tiempo, pues se evita inicializar un nuevo objeto de clase :py:class:`LematizadorSpacy <lematizacion.LematizadorSpacy>` para cada texto. Este ahorro de tiempo será mayor a medida que sean más los textos que se desean lematizar.

A continuación se muestra una comparación de tiempos para dos opciones:

1. Lematizar una lista de textos, aplicando la función :py:func:`lematizacion.lematizar_texto` a cada uno sin ninguna otra consideración.
2. Definir un objeto de clase :py:class:`LematizadorSpacy <lematizacion.LematizadorSpacy>` y utilizarlo para lematizar la misma lista de textos.

.. code-block:: python

    >>> # Opción 1: se inicializa el lematizador en cada texto
    >>> tic = time.time()
    >>> for t in textos:
    >>>     print(lematizar_texto(t))

    >>> tiempo_1 = time.time() - tic

    >>> # Opción 2: se utiliza solo un lematizador para todos los textos
    >>> print('--------------------')
    >>> tic = time.time()
    >>> lematizador = LematizadorSpacy('es')
    >>> for t in textos:
    >>>     print(lematizar_texto(t, lematizador=lematizador))

    >>> tiempo_2 = time.time() - tic

    >>> print('\n***************\n')
    >>> print('Tiempo con opción 1: {} segundos\n'.format(tiempo_1))
    >>> print('Tiempo con opción 2: {} segundos\n'.format(tiempo_2))

    este ser uno primero entrar en el grupo de texto
    el pibe valderrama empezar a destacar jugar fútbol desde chiquitin
    de lo pájaro del montar yo querer ser canario
    finalizar este listica se incluir uno último frase uno poquito más largo que los anterior
    --------------------
    este ser uno primero entrar en el grupo de texto
    el pibe valderrama empezar a destacar jugar fútbol desde chiquitin
    de lo pájaro del montar yo querer ser canario
    finalizar este listica se incluir uno último frase uno poquito más largo que los anterior

    ***************

    Tiempo con opción 1: 17.106500387191772 segundos

    Tiempo con opción 2: 3.785933494567871 segundos


Lematización de textos utilizando Stanza
----------------------------------------

El parámetro *libreria* de la función :py:func:`lematizacion.lematizar_texto` permite elegir 'stanza', para utilizar esta librería. se encarga de aplicar lematización a todas las palabras de un texto de entrada. Si se define *liberia='stanza'*, la función utilizará el lematizador de la clase :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>`. La primera vez que se seleccione un modelo de un lenguaje determinado, la función descargará el modelo correspondiente en el computador del usuario. Este proceso puede durar algunos minutos, dependiendo de la conexión a internet.

.. warning::
    Es importante recalcar que para poder utilizar el :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>` es necesario tener los paquetes **torch, torhvision y stanza** instalados, que no vienen en la versión de ConTexto instalable a través de pip. Para mayor información puede consultar la :ref:`sección de instalación <seccion_instalacion>`.

.. code-block:: python

    >>> # Lematización con librería Stanza ###
    >>> texto_lematizado = lematizar_texto(texto, libreria='stanza')
    >>> print(texto_lematizado)

    >>> # Prueba en otro lenguaje
    >>> lemma_english = lematizar_texto(texto_ingles, lenguaje='ingles', libreria='stanza')
    >>> print('------')
    >>> print(lemma_english)

    este ser uno prueba para ver si el función ser correcto y funcionar bien perrito y gato ir a el casita
    ------
    this be a test writing to study if these function be perform well


Agregar lemas personalizados al `LematizadorStanza`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al igual que en el caso de spaCy, el :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>` permite añadir o modificar lemas, utilizando un archivo JSON o un diccionario de Python. Esto se hace con la función :py:func:`lematizacion.modificar_lemmas`, y se puede utilizar el parámetro *archivo_salida* para determinar dónde se quiere guardar el modelo resultante. 

De esta manera, este modelo puede ser luego cargado a un objeto de clase :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>` para seguirlo utilizando o modificando. Para cargar un modelo guardado previamente, es necesario utilizar el parámetro *modelo_lemas*, al definir el objeto lematizador.

.. note::
        La carpeta `entrada <https://github.com/ucd-dnp/ConTexto/tree/master/ejemplos/entrada>`_ de la sección de ejemplos del `Repositorio de GitHub de ConTexto <https://github.com/ucd-dnp/ConTexto>`_ tiene insumos que servirán para correr varios ejemplos de la librería **ConTexto**. En este caso en particular, se va a utilizar el archivo `dict_lemas.json`.

.. code-block:: python

    >>> ## Utilizar un archivo JSON al momento de lematizar
    >>> archivo_lemmas = 'entrada/dict_lemas.json'
    >>> texto_lematizado_v2 = lematizar_texto(texto,libreria='stanza',dict_lemmas=archivo_lemmas)
    >>> print(texto_lematizado_v2)
    >>> print('------')

    >>> ## Modificar los lemas utilizando un diccionario
    >>> segundo_dict = {
    >>>     "chiquitin": "chico",
    >>>     'valderrama': 'valderrama',
    >>>     'listica': 'lista'
    >>> }

    >>> # Inicializar lematizador para lenguaje español
    >>> lematizador = LematizadorStanza('es')
    >>> print(lematizador.lematizar(textos[1]))
    >>> # Modificar lemas y guardar el modelo resultante
    >>> lematizador.modificar_lemmas(dict_lemmas=segundo_dict, archivo_salida='salida/modelo_lemas_stanza.pt')
    >>> # Lemarizar de nuevo el mismo texto, después de la modificación
    >>> print(lematizador.lematizar(textos[1]))

    este ser uno prueba para ver si el función ser correcto y funcionar bien perro y gato ir a el casita
    ------
    el pibe valderramo empezar a destacar jugar fútbol desde chiquitin
    el pibe valderrama empezar a destacar jugar fútbol desde chico


Corrección de varios textos utilizando un solo objeto de la clase `LematizadorStanza`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si se desea lematizar un conjunto de textos, puede ser más rápido definir un único objeto de clase :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>`, y pasar este objeto en el parámetro *lematizador* de la función :py:func:`lematizacion.lematizar_texto`. Al hacer esto puede haber un ahorro de tiempo, pues se evita inicializar un nuevo objeto de clase :py:class:`LematizadorStanza <lematizacion.LematizadorStanza>` para cada texto. Este ahorro de tiempo será mayor a medida que sean más los textos que se desean lematizar.

A continuación se muestra una comparación de tiempos para dos opciones:

1. Lematizar una lista de textos, aplicando la función `lematizar_texto` a cada uno sin ninguna otra consideración.
2. Definir un objeto de clase `LematizadorStanza` y utilizarlo para lematizar la misma lista de textos.

.. code-block:: python

    >>> # Opción 1: se inicializa el lematizador en cada texto
    >>> tic = time.time()
    >>> for t in textos:
    >>>     print(lematizar_texto(t, libreria='stanza', modelo_lemas='salida/modelo_lemas_stanza.pt'))

    >>> tiempo_1 = time.time() - tic

    >>> # Opción 2: se utiliza solo un lematizador para todos los textos
    >>> print('--------------------')
    >>> tic = time.time()
    >>> # Se carga el modelo guardado previamente en el ejemplo
    >>> lematizador = LematizadorStanza('es', modelo_lemas='salida/modelo_lemas_stanza.pt')
    >>> for t in textos:
    >>>     print(lematizar_texto(t, lematizador=lematizador))

    >>> tiempo_2 = time.time() - tic

    >>> print('\n***************\n')
    >>> print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
    >>> print(f'Tiempo con opción 2: {tiempo_2} segundos\n')

    este ser uno primero entrada en el grupo de texto
    el pibe valderrama empezar a destacar jugar fútbol desde chico
    de el pájaro del monte yo querer ser canario
    finalizar este lista él incluir uno último frase uno poquito más largo que el anterior
    --------------------
    este ser uno primero entrada en el grupo de texto
    el pibe valderrama empezar a destacar jugar fútbol desde chico
    de el pájaro del monte yo querer ser canario
    finalizar este lista él incluir uno último frase uno poquito más largo que el anterior

    ***************

    Tiempo con opción 1: 4.91388726234436 segundos

    Tiempo con opción 2: 1.47633695602417 segundos