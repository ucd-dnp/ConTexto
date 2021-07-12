.. _instalacion_poppler_tesseract_linux:

Instalación de Poppler y Tesseract en Linux
===========================================

.. note::
    Para la instalación de paquetes en linux se utiliza el comando ``sudo``, por lo que se requiere contar con permisos de administrador.

Como primer paso se procede a actualizar el gestor de paquetes de linux utilizando el siguiente comando:

.. code-block:: python

    >>> sudo apt-get update -y

Instalación de Poppler.
-----------------------

Para realizar la instalación de Poppler solo se necesita ejecutar el siguiente comando:

.. code-block:: python    
    
    >>> sudo apt-get install -y poppler-utils

Instalación de Tesseract. 
-------------------------

#. Para realizar la instalación de Tesseract se necesita ejecutar el siguiente comando:

    .. code-block:: python

        >>> sudo apt install tesseract-ocr

#. Añadir otros idiomas al reconocimiento óptico de caracteres (OCR).

   .. note::
        * Para añadir otros idiomas al OCR se deben descargar los archivos de entrenamiento en el idioma deseado, los cuales se encuentran disponibles en:  https://github.com/tesseract-ocr/tessdata. (Para el desarrollo de este manual se hará el ejemplo con el idioma español)

        * Por defecto, en la instalación se cargan los archivos del idioma Inglés, sin embargo, estos corresponden a un corpus pequeño, por lo que se recomienda descargar nuevamente los archivos para este idioma desde el enlace mencionado anteriormente.



   Para el idioma español se descargara el archivo `spa.traineddata <https://github.com/tesseract-ocr/tessdata/blob/master/spa.traineddata>`_. El archivo descargado se debe copiar en la carpeta tessdata siguiendo la ruta de instalación de *Tesseract*, que por defecto para Linux es:

    .. code-block:: console

            /usr/share/tesseract-ocr/4.00/tessdata/
    