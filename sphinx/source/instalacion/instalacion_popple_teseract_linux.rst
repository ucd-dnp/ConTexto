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

Para realizar la instalación de Tesseract solo se necesita ejecutar el siguiente comando:

.. code-block:: python

    >>> sudo apt install tesseract-ocr