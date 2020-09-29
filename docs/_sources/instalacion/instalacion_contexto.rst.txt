.. _instalacion_basica:

Instalación ConTexto
====================

Para la instalación de la librería se debe utilizar el gestor de paquetes ``pip``, por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador. Esta instalación no presenta restricciones de arquitectura, es decir, funciona tanto para arquitecturas de 32 bits como arquitecturas de 64 bits.

    .. code-block:: console

        pip install contexto


Otra alternativa de instalación corresponde a utilizar los archivos compilados wheel que se encuentran cargados en el repositorio de GitHub de la librería. Al utilizar los archivos wheel instalará las dependencias de ConTexto, equivalente a utilizar el comando ``pip install contexto`` y adicionalmente instalará el framework `PyTorch <https://pytorch.org/>`_ (con instalación para uso de CPU) y el paquete `Stanza <https://stanfordnlp.github.io/stanza/>`_ , estos últimos se utilizan en el módulo de :py:mod:`Lematización <lematizacion>`.

.. warning::
        * La instalación utilizando los archivos wheel solo soporta Python en arquitecturas de 64 bits (x64)
        * Versión máxima soportada de Python v3.8.5        

Para *Python 3.8x* usar:
    .. code-block:: console
    	
    	pip install https://github.com/ucd-dnp/ConTexto/blob/master/bin/ConTexto-0.1.0-py38-none-any.whl?raw=true
        
Para *Python 3.7x* usar:
    .. code-block:: console
    
        pip install https://github.com/ucd-dnp/ConTexto/blob/master/bin/ConTexto-0.1.0-py37-none-any.whl?raw=true

Para *Python 3.6x* usar:
    .. code-block:: console
    
        pip install https://github.com/ucd-dnp/ConTexto/blob/master/bin/ConTexto-0.1.0-py36-none-any.whl?raw=true