.. _control_de_cambios:

Control de cambios
==================

Todos los cambios importantes de la librería *ConTexto* serán documentados en esta sección.

v0.2.0 (2021-07- )
++++++++++++++++++

Agregado
--------
- Se agregó función para generar :py:func:`gráfico_de_dispersión_léxica <exploracion.graficar_dispersion>` en el módulo de :py:mod:`Exploración <exploracion>`.
- Se agregó :ref:`Ejemplo de gráfico de dispersión léxica <Gráficos de dispersión léxica>` con palabras y bi-gramas a la sección de :ref:`ejemplos <seccion_ejemplos>`.
- Se agregó compatibilidad para instalación por medio de conda. 
- Se habilitó la librería *ConTexto* para la versión 3.9 de Python.

Modificado
----------
- Se hace compatible con la versión 3.0.6 o mayor de *Spacy*.
- Se complementó la lista de stopwords.
- Se actualizó el :ref:`ejemplo de exploración y visualización <03_exploracion_y_visualizacion>` de textos.
- Se actualizó y modificó la :ref:`documentación <index>` de la librería.
- Se modificó el gráfico de :py:func:`co-ocurrencias <exploracion.graficar_coocurrencias>`.
- Se modificó :ref:`ejemplo de gráfico de co-ocurrencias <Calcular coocurrencias y graficarlas>` con la modificación de la función :py:func:`graficar_coocurrencias() <exploracion.graficar_coocurrencias>` a la sección de :ref:`ejemplos <seccion_ejemplos>`.
- Se modificó el instalador de *ConTexto*. Ya no es necesario realizar la instalación del paquete *Stanza* manualmente.

Obsoleto
--------
- No hay soporte para *Python* versión 3.6.1

Borrado
-------
- Se eliminaron nombres repetidos en la lista de nombres.

Arreglado
---------
- Se corrigieron errores en la parte *pre-OCR*.