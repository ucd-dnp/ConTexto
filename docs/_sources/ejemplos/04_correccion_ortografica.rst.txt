.. _04_correccion_ortografica:

Corrección ortográfica
======================

Este ejemplo muestra las principales funcionalidades del módulo `correccion`, de la librería . Este módulo permite realizar corrección ortográfica de textos, lo que puede simplificar los documentos, al estandarizar palabras que deberían ser escritas de la misma forma y evitando así tener un vocabulario más grande de lo necesario.

Importar funciones necesarias y definir textos de prueba
--------------------------------------------------------

En este caso se importa la función `corregir_texto`, que aplica corrección ortográfica a un texto de entrada, y la clase `Corrector`, que tiene algunas funcionalidades adicionales que pueden ser de utilidad. Adicionalmente, se definen algunos textos con mala ortografía para desarrollar los ejemplos.

.. code-block:: python

    >>> from contexto.correccion import Corrector, corregir_texto

    >>> # textos de prueba
    >>> texto = 'Ojalá halya un buen hasado de polllo, para poder comer delizioso palabrainventada.'
    >>> texto_ingles = 'This is a tets writtyng to estudy if tese functions are performing guell.'
    >>> textos = [
    >>>     "Esta es una pirmera emtrada en hel grupo de testos",
    >>>     "El Pibe Valderrama empesó a deztacar jugando fútvol desde chikitin",
    >>>     "De los pajaros del monnte yo quixiera ser canarrio",
    >>>     "Finalisando esta lizta, se inclulle una última frace un pokito más larga ke las amteriores."
    >>> ]


Corrección de textos y detección de palabras conocidas, desconocidas y candidatas
---------------------------------------------------------------------------------

La función :py:func:`correccion.corregir_texto` se encarga de detectar palabras desconocidas (que no están en el diccionario del corrector) en un texto y buscar una palabra correcta para corregirlas, dentro de una distancia determinada.

.. code-block:: python

    >>> texto_corregido = corregir_texto(texto)
    >>> print(texto_corregido)

    Ojalá haya un buen pasado de pollo, para poder comer delicioso palabrainventada.

.. code-block:: python

    >>> # Prueba en otro lenguaje
    >>> corregido_ingles = corregir_texto(texto_ingles, 'en')
    >>> print(corregido_ingles)

    This is a test written to study if these functions are performing gull.

.. code-block:: python

    >>> # Si se deja el parámetro lenguaje en "auto", la función identificará
    >>> # qué lenguaje es el predominante. Esto hará que la corrección sea un
    >>> # poco más demorada
    >>> corregido_ingles = corregir_texto(texto_ingles, lenguaje='auto')

    This is a test written to study if these functions are performing gull.

Al utilizar la clase `Corrector` es posible identificar explícitamente las palabras conocidas y desconocidas identificadas en un texto de entrada, así como las palabras candidatas para corregir una palabra desconocida.

.. code-block:: python

    >>> # Definir un objeto de la clase Corrector
    >>> corrector = Corrector(lenguaje='es')

    >>> # Detectar palabras conocidas y desconocidas en un texto
    >>> conocidas = corrector.palabras_conocidas(texto)
    >>> desconocidas = corrector.palabras_desconocidas(texto)

    >>> # Palabras candidatas para corregir una palabra mal escrita
    >>> candidatas = corrector.palabras_candidatas('hasado')

    >>> print(f'Palabras en el texto que fueron reconocidas: {conocidas}')
    >>> print('----')
    >>> print(f'Palabras en el texto que no fueron reconocidas: {desconocidas}')
    >>> print('----')
    >>> print(f'Palabras candidatas para corregir la palabra "hasado": {candidatas}')

    Palabras en el texto que fueron reconocidas: {'para', 'un', 'buen', 'comer', 'poder', 'de', 'ojalá'}
    ----
    Palabras en el texto que no fueron reconocidas: {'hasado', 'palabrainventada', 'delizioso', 'halya', 'polllo'}
    ----
    Palabras candidatas para corregir la palabra "hasado": {'asado', 'pasado', 'basado', 'casado'}
    

Modificar el diccionario del corrector, para añadir, eliminar o cambiar la preferencia de las palabras
------------------------------------------------------------------------------------------------------

La clase `Corrector` usa, para varios lenguajes, unos diccionarios predefinidos, que contienen el vocabulario "válido" o conocido, junto con la frecuencia de cada palabra. Estas frecuencias fueron obtenidas a partir de un corpus, o conjunto de documentos, determinado.

Es posible modificar estos diccionarios para alcanzar 3 propósitos distintos:

Incluir palabras como "correctas", a pesar de no estar en el diccionario original
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Por ejemplo, términos científicos o tecnológicos.

.. code-block:: python

    >>> # Crear objeto de la clase Corrector y mostrar las palabras que no son reconocidas
    >>> corrector = Corrector(lenguaje='es')
    >>> print(corrector.palabras_desconocidas(texto))

    >>> ## Caso 1: Añadir una nueva palabra al diccionario
    >>> corrector.agregar_palabras('palabrainventada')
    >>> print(corrector.palabras_desconocidas(texto))

    {'hasado', 'polllo', 'palabrainventada', 'delizioso', 'halya'}
    {'hasado', 'halya', 'polllo', 'delizioso'}

Quitar palabras que, a pesar de que aparecen en el diccionario original, no se desean marcar como correctas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> ## Caso 2: Quitar una palabra del diccionario
    >>> t = 'Head y house son palabras en inglés. En español deberían ser marcadas como desconocidas.'

    >>> print(corrector.palabras_desconocidas(t))

    >>> corrector.quitar_palabras(['head', 'house'])

    >>> print(corrector.palabras_desconocidas(t))

    set()
    {'house', 'head'}


Modificar las frecuencias de algunas palabras, de forma que tengan prelación sobre otras al momento de realizar una corrección
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En el texto original queremos que "hasado" se corrija por "asado". Sin embargo, la palabra "pasado" tiene mayor frecuencia en el diccionario, por lo que se toma como la más probable.

Esto lo podemos modificar por medio del diccionario, para obtener el resultado deseado (esto puede tener efectos adversos, utilizar con cuidado).

.. code-block:: python

    >>> ## Caso 3: Modificar la frecuencia de una palabra, para que tenga prioridad en correcciones

    >>> for p in corrector.palabras_candidatas('hasado'):
    >>>     freq = corrector.frecuencia_palabra(p)
    >>>     print(f'{p}: {freq}')

    >>> dict_asado = {'asado': corrector.frecuencia_palabra('pasado') + 1}
    >>> corrector.actualizar_diccionario(dict_asado)

    >>> for p in corrector.palabras_candidatas('hasado'):
    >>>     freq = corrector.frecuencia_palabra(p)
    >>>     print(f'{p}: {freq}')

    >>> texto_corregido = corrector.correccion_ortografia(texto)

    >>> print('----')
    >>> print('Texto corregido, después de cambiar algunas frecuencias en el diccionario:',texto_corregido, sep='\n')

    pasado: 149286
    basado: 4187
    casado: 20297
    asado: 2322
    pasado: 149286
    basado: 4187
    casado: 20297
    asado: 149287
    ----
    Texto corregido, después de cambiar algunas frecuencias en el diccionario:
    Ojalá haya un buen asado de pollo, para poder comer delicioso palabrainventada.

Las frecuencias de palabras también se pueden modificar con un archivo json que contenga el diccionario.

.. note::
        La carpeta `entrada <https://github.com/ucd-dnp/ConTexto/tree/master/ejemplos/entrada>`_ de la sección de ejemplos del `Repositorio de GitHub de ConTexto <https://github.com/ucd-dnp/ConTexto>`_ tiene insumos que servirán para correr varios ejemplos de la librería **ConTexto**. En este caso en particular, se va a utilizar el archivo `dict_ortografia.json`

.. code-block:: python

    >>> ubicacion_dict = 'entrada/dict_ortografia.json'
    >>> corrector.actualizar_diccionario(ubicacion_dict)

    >>> print(corrector.frecuencia_palabra('asado'))
    >>> print(corrector.frecuencia_palabra('palabrainventada'))

    230000
    2


Corrección de varios textos utilizando un solo objeto de la clase `Corrector`
-----------------------------------------------------------------------------

Si se desea aplicar corrección ortográfica a un conjunto de textos, puede ser más rápido definir un único objeto de clase `Corrector`, y pasar este objeto en el parámetro *corrector* de la función :py:func:`correccion.corregir_texto`. Al hacer esto puede haber un ahorro de tiempo, pues se evita inicializar un nuevo objeto de clase `Corrector` para cada texto. Este ahorro de tiempo será mayor a medida que sean más los textos que se desean corregir.

A continuación se muestra una comparación de tiempos para dos opciones:

1. Corregir una lista de textos, aplicando la función `corregir_texto` a cada uno sin ninguna otra consideración.
2. Definir un objeto de clase `Corrector` y utilizarlo para corregir la misma lista de textos

.. code-block:: python

    >>> import time

    >>> # Opción 1: se inicializa el corrector en cada texto
    >>> tic = time.time()
    >>> for t in textos:
    >>>     print(corregir_texto(t))

    >>> tiempo_1 = time.time() - tic

    >>> # Opción 2: se utiliza solo un corrector para todos los textos
    >>> print('--------------------')
    >>> tic = time.time()
    >>> corrector = Corrector('spanish')
    >>> for t in textos:
    >>>     print(corregir_texto(t, corrector=corrector))

    >>> tiempo_2 = time.time() - tic

    >>> print('\n***************')
    >>> print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
    >>> print(f'Tiempo con opción 2: {tiempo_2} segundos\n')

    Esta es una primera entrada en hel grupo de estos
    El Pibe Valderrama empezó a destacar jugando fútbol desde chikitin
    De los pajaros del monte yo quisiera ser canario
    Finalisando esta lista, se incluye una última grace un polito más larga ke las anteriores.
    --------------------
    Esta es una primera entrada en hel grupo de estos
    El Pibe Valderrama empezó a destacar jugando fútbol desde chikitin
    De los pajaros del monte yo quisiera ser canario
    Finalisando esta lista, se incluye una última grace un polito más larga ke las anteriores.

    ***************
    Tiempo con opción 1: 5.750852346420288 segundos

    Tiempo con opción 2: 4.660573720932007 segundos