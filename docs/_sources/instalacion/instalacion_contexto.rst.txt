.. _instalacion_basica:

Instalación ConTexto
====================

Instalación básica
------------------

Para la instalación de la librería se debe utilizar el gestor de paquetes ``pip``, por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador. Esta instalación no presenta restricciones de arquitectura, es decir, funciona tanto para arquitecturas de 32 bits como arquitecturas de 64 bits.

    .. code-block:: console

        pip install contexto


Instalación completa
--------------------

Otra alternativa de instalación corresponde a utilizar los archivos compilados wheel que se encuentran cargados en el repositorio de GitHub de la librería. Al utilizar los archivos wheel se instalarán las dependencias de ConTexto, equivalente a utilizar el comando ``pip install contexto`` y adicionalmente se instalará el framework `PyTorch <https://pytorch.org/>`_ (con instalación para uso de CPU) y el paquete `Stanza <https://stanfordnlp.github.io/stanza/>`_, estos últimos se utilizan en el módulo de :py:mod:`Lematización <lematizacion>`, sin embargo, su instalación no es de caracter obligatorio, ya que por defecto se utiliza el lematizador de `spaCy <https://spacy.io/>`_.

.. warning::
        * La instalación utilizando los archivos wheel solo soportan Python en arquitecturas de 64 bits (x64) para Windows. Para Linux no se presenta esta restricción.
        * Versión máxima soportada de Python v3.8.5
        * Versión mínima soportada de Python v3.6.1

.. code-block:: console

        pip install contexto -f https://ucd-dnp.github.io/ConTexto/contexto_stable.html
