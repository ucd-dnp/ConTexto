.. _01_lectura_y_escritura_de_documentos:

Lectura y escritura de documentos
=================================

Este ejemplo muestra las principales funcionalidades de los módulos :py:mod:`Lectura <lectura>` y :py:mod:`Escritura <escritura>` de la librería. Estos módulos permiten extraer textos de archivos en diferentes formatos, así como escribir texto en nuevos archivos.

.. warning::
        Es necesario recordar que para el correcto funcionamiento del módulo de :py:mod:`Lectura <lectura>` es necesario tener instalados Poppler y Tesseract en el computador del usuario. Para más información sobre cómo instalar estos requerimientos, por favor consultar la :ref:`Documentación de instalación <seccion_instalacion>`.


Importar paquetes necesarios y definir documentos para la prueba
----------------------------------------------------------------

.. note::
        La carpeta `entrada <https://github.com/ucd-dnp/ConTexto/tree/master/ejemplos/entrada>`_ de la sección de ejemplos del `Repositorio de GitHub de ConTexto <https://github.com/ucd-dnp/ConTexto>`_ tiene insumos que servirán para correr varios ejemplos de la librería **ConTexto**. En este ejemplo se van a utilizar documentos que están en los siguientes formatos:

        * Archivo plano (.txt)
        * Archivos .PDF; uno digitalizado y uno escaneado (se requiere aplicar OCR para leer este)
        * Archivos de Microsoft Word (.doc y .docx)
        * Archivo tipo *Rich Text Format* (.rtf)
        * Imagen con texto (.png)

El módulo de :py:mod:`Lectura <lectura>` de **ConTexto** permite extraer texto de estos tipos de archivos.

.. code-block:: python

    >>> # Importar módulos y paquetes necesarios
    >>> import re

    >>> from contexto.lectura import Lector, leer_texto
    >>> from contexto.escritura import Escritor, escribir_texto

    >>> # Rutas de los archivos de los cuales se va a extraer texto
    >>> archivo_txt = 'entrada/prueba_in.txt'
    >>> archivo_pdf = 'entrada/prueba_in.pdf'
    >>> archivo_pdf_ocr = 'entrada/prueba_in_ocr.pdf'
    >>> archivo_docx = 'entrada/prueba_in.docx'
    >>> archivo_doc = 'entrada/prueba_in.doc'
    >>> archivo_rtf = 'entrada/prueba_in.rtf'
    >>> archivo_img = 'entrada/prueba_in.png'


Extraer texto de los documentos y escribir el texto extraído en nuevos archivos
-------------------------------------------------------------------------------

A continuación se definen dos listas, una de los documentos a leer y otra de los documentos en los que se quiere guardar el texto extraído. Los nuevos documentos quedarán guardados en la carpeta *salida*, una vez se corra el ejemplo.

.. code-block:: python

    >>> # Definir lista de archivos de entrada
    >>> archivos_in = [archivo_docx, archivo_pdf, archivo_pdf_ocr,
    >>>                archivo_txt, archivo_rtf, archivo_img]

    >>> # Definir lista de archivos de salida, simplemente cambiando el nombre de la carpeta ("salida" en vez de "entrada")
    >>> archivos_out = [re.sub('entrada', 'salida', i) for i in archivos_in]

A continuación se hace un recorrido por la lista de documentos de entrada, y para cada uno:

* Se determina si se necesita utilizar OCR (solo es necesario definirlo para el archivo de PDF escaneado. En las imagenes se utiliza OCR por defecto).
* Se utiliza la función :py:func:`lectura.leer_texto` para extraer el texto del documento.
* El texto extraído se guarda en el archivo de salida, utilizando la función :py:func:`escritura.escribir_texto`. Esta función permite guardar texto en archivos planos (.txt), PDF y Word (.docx). Si el nombre del archivo especificado es de otro tipo, la función guarda el texto como un archivo plano.

.. code-block:: python

    >>> for i, archivo in enumerate(archivos_in):
    >>>     aplicar_ocr = True if 'ocr' in archivo else False
    >>>     print('------------')
    >>>     print(archivo)
    >>>     texto = leer_texto(archivo, por_paginas=True, ocr=aplicar_ocr, preprocesamiento=3)
    >>>     escribir_texto(archivos_out[i], texto)

    ------------
    entrada/prueba_in.docx
    ------------
    entrada/prueba_in.pdf
    ------------
    entrada/prueba_in_ocr.pdf
    ------------
    entrada/prueba_in.txt
    ------------
    entrada/prueba_in.rtf
    Formato desconocido. Se escribirá en un formato plano (.txt).
    ------------
    entrada/prueba_in.png
    Formato desconocido. Se escribirá en un formato plano (.txt).


Utilizar el OCR para extraer textos de imágenes
-----------------------------------------------

El OCR (reconocimiento óptico de caracteres) se utiliza para extraer texto de archivos de imagen. **ConTexto** incorpora el OCR de Tesseract para extraer texto de imágenes (por ejemplo, documentos escaneados). Actualmente, la librería soporta archivos en formatos ".png", ".jpg" y ".jpeg". Para archivos PDF, la librería primero convierte las páginas a imágenes, y luego aplica el OCR.

Adicionalmente, la librería permite realizar algunas operaciones de preprocesamiento sobre las imágenes antes de aplicar el OCR. Estos preprocesamientos pueden permitir hacer una lectura más acertada de los textos de las imágenes. 

En este ejemplo, se va a leer el contenido de una imagen y se va a mostrar cómo diferentes preprocesamientos del OCR pueden llevar a diferentes resultados en la lectura. En primer lugar, se carga y grafica la imagen. No es necesario hacer esto para extraer el texto; solo se grafica acá por motivos didácticos.

.. code-block:: python

    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.image as mpimg
    
    >>> img = mpimg.imread(archivo_img)
    
    >>> plt.figure(figsize=(8,10))
    >>> imgplot = plt.imshow(img)
    >>> plt.axis('off')
    >>> plt.show()

.. figure:: ../_static/image/graficos/prueba_in.jpg
    :align: center
    :alt: 
    :figclass: align-center


El parámetro *preprocesamiento* de la función :py:func:`lectura.leer_texto` y de la clase :py:class:`Lector <lectura.Lector>` permite elegir entre 5 diferentes tratamientos previos a la imagen. Si el valor de *preprocesamiento* no está en el rango de 1 a 5, no se realizará ningún preprocesamiento sobre la imagen.

A continuación, se lee la imagen sin preprocesar y con dos tipos distintos de procesamiento, imprimiendo el resultado en cada caso.

.. code-block:: python

    >>> procesamientos = [0, 2, 4]
    >>> for p in procesamientos:
    >>>     print('---------------')
    >>>     if p == 0:
    >>>         print(f'Preprocesamiento: {p} (sin Preprocesamiento)')
    >>>     else:
    >>>         print(f'Preprocesamiento: {p}')
    >>>     texto = leer_texto(archivo_img, preprocesamiento=p)
    >>>     print(texto)

    ---------------
    Preprocesamiento: 0 (sin Preprocesamiento)
    fTextó contruidó de Í"
    fondo, paré probar
    Tesseract

    ---------------
    Preprocesamiento: 2
    Texto con ruido de
    fondo, para probar
    Tesseract

    ---------------
    Preprocesamiento: 4


Se puede observar que el mejor desempeño se obtiene con *preprocesamiento=2*. Cuando no se hace ningún procesamiento, el ruido de fondo de la imagen afecta el texto extraído. Por otro lado, con *preprocesamiento=4* la función no encuentra ningún texto. Dependiendo de la calidad de la imagen (o archivo PDF escaneado) de entrada, diferentes preprocesamientos (o no aplicar ninguno) tendrán mejor o peor desempeño.

Enderezar textos en imágenes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Además del parámetro *preprocesamiento*, la función :py:func:`lectura.leer_texto` y la clase :py:class:`Lector <lectura.Lector>` cuenta con el parámetro *enderezar*, por defecto igual a *False*. Cuando este parámetro se hace igual a *True*, la librería intentará identificar y corregir un giro en el texto de la imagen de la cual se desea extraer texto. Una vez se haga esta corrección de giro, se aplicará el OCR.

Este procesamiento adicional se puede combinar con cualquiera de los 5 preprocesamientos de la librería, o incluso se puede aplicar sin necesidad de utilizar el parámetro *preprocesamiento*. La corrección de giro puede ser bastante útil para textos torcidos, como en el caso de documentos escaneados.

.. code-block:: python

    >>> texto_torcido = 'entrada/texto_torcido.jpg'
    >>> img = mpimg.imread(texto_torcido)
    
    >>> plt.figure(figsize=(8,10))
    >>> imgplot = plt.imshow(img)
    >>> plt.axis('off')
    >>> plt.show()

.. figure:: ../_static/image/graficos/texto_torcido.jpg
    :align: center
    :alt: 
    :figclass: align-center


.. code-block:: python

    >>> enderezar = [False, True]
    >>> for e in enderezar:
    >>>     print('---------------')
    >>>     print(f'*Utilizando el parámetro enderezar={e}:*')
    >>>     texto = leer_texto(texto_torcido, preprocesamiento=4, enderezar=e)
    >>>     print(texto)

    ---------------
    *Utilizando el parámetro enderezar=False:*
    Texto torcido (con

    lgún grado de
    inclinación)
    
    ---------------
    *Utilizando el parámetro enderezar=True:*
    Texto torcido (con
    algún grado de
    inclinación)


Utilizar las clases `Lector` y `Escritor`
-----------------------------------------

Si se desea, también es posible utilizar las clases `Lector` y `Escritor` para leer y escribir archivos, respectivamente.

.. code-block:: python

    >>> # Definir objeto de clase Lector y extraer el texto
    >>> lector = Lector(archivo_img)
    >>> texto = lector.archivo_a_texto(preprocesamiento=2)
    
    >>> print(f'*El texto extraído es:* \n{texto}')
    
    >>> # Definir objeto de clase Escritor y escribir el texto en un nuevo archivo
    >>> escritor = Escritor('salida/prueba.txt', texto)
    >>> escritor.escribir_txt()
    
    *El texto extraído es:* 
    Texto con ruido de
    fondo, para probar
    Tesseract
