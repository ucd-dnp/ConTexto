.. _instalacion_basica:

Instalación ConTexto
====================

Instalación usando pip
----------------------

Por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y así evitar conflictos de versiones con el entorno de desarrollo base del computador.

    .. code-block:: console

        pip install contexto


.. warning::
        Para versiones de ``Python <= 3.8.4`` es necesario actualizar el gestor de paquetes ``pip`` antes de la instalación de *ConTexto*. Para versiones superiores se recomienda hacer la actualización para evitar errores.

        Para actualizar el gestor de paquetes ``pip`` puede usar el siguiente comando:

            .. code-block:: console

                python -m pip install --upgrade pip

        * Versiones soportadas de ``Python >= 3.6.2``.
        * *ConTexto* está disponible para Windows x64 y Linux.
        * *ConTexto* no fue probada en arquitecturas de 32 bits para Windows, por lo que se podrían presentar errores.



Instalación usando conda
------------------------

Para realizar la instalación en ``Anaconda / Miniconda`` utilizar el siguiente comando:


    .. code-block:: console

        pip install --extra-index-url https://pypi.org/simple/ contexto