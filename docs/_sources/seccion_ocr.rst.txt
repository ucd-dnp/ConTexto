.. _seccion_ocr:

.. |br| raw:: html

   <br />

.. |ul| raw:: html

   <ul>

.. |/ul| raw:: html

   </ul>

.. |li| raw:: html

   <li>

.. |/li| raw:: html

   </li>

OCR
+++

En esta sección se brinda mayor información relacionada con los
parámetros *psm* y *oem* utilizados por la función de OCR 
(Reconocimiento Óptico de Caracteres) de la librería.

.. note::
        * Los lenguajes disponibles para el OCR dependen de los idiomas instalados en Tesseract. Para mayor información sobre como instalar nuevos idioma, referirse a la sección :ref:`Instalación de Tessereact <instalacion_tesseract>`.
        
:oem: (int) {0, 1, 2, 3}. OEM hace referencia al modo del motor OCR (OCR engine mode \
    en inglés). Tesseract tiene 2 motores, Legacy Tesseract y LSTM, y los parámetros de 'oem' \
    permiten escoger cada uno de estos motores por separado, ambos al tiempo o \
    automáticamente:

    |ul| 
    |br|
    |li| 0: utilizar únicamente el motor Legacy. |/li| 
    |li| 1: utilizar únicamente el motor de redes neuronales LSTM. |/li| 
    |li| 2: utilizar los motores Legacy y LSTM. |/li| 
    |li| 3: escoger el motor según lo que hay disponible. |/li| 
    |/ul| 

:psm: (int) {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}. PSM hace referencia a \
    los modos de segmentación de las páginas (page segmentation modes, en inglés) de la \
    librería Pytesseract. Cada número hace referencia a un modo de segmentación: \

    |ul| 
    |br|
    |li| 0: orientation y detección de script (OSD) únicamente. |/li| 
    |li| 1: segmentación automática de páginas con OSD. |/li| 
    |li| 2: segmentación automática de páginas sin OSD ni OCR. |/li| 
    |li| 3: segmentación completamente automática de páginas sin OSD. |/li| 
    |li| 4: supone una única columna de texto de tamaños variables. |/li| 
    |li| 5: supone un único bloque uniforme de texto alineado de forma vertical. |/li| 
    |li| 6: asume un único bloque uniforme de texto. |/li| 
    |li| 7: trata la imagen como una única línea de texto. |/li| 
    |li| 8: trata la imagen como una única palabra. |/li| 
    |li| 9: trata la imagen como una única palabra dentro de un círculo. |/li| 
    |li| 10: trata la imagen como un único carácter. |/li| 
    |li| 11: Buscador de texto disperso. Encontrar la mayor cantidad de texto posible sin un orden en particular. |/li| 
    |li| 12: Buscador de texto disperso con OSD. |/li| 
    |li| 13: trata el texto como una única línea, sin utilizar métodos específicos de Tesseract. |/li| 
    |/ul| 