# ConTexto - Librería de procesamiento y análisis de textos

![screenshot](https://raw.githubusercontent.com/ucd-dnp/contexto/master/recursos/contexto.jpg "ConTexto")

[![PyPI version fury.io](https://badge.fury.io/py/ConTexto.svg)](https://pypi.org/project/ConTexto/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ConTexto.svg)](https://pypi.org/project/ConTexto/)
 [![PyPI license](https://img.shields.io/pypi/l/ConTexto.svg)](https://pypi.org/project/ConTexto/) [![Downloads](https://pepy.tech/badge/contexto)](https://pepy.tech/project/contexto) [![GitHub forks](https://img.shields.io/github/forks/ucd-dnp/ConTexto.svg?style=social&label=Fork&maxAge=2592000)](https://github.com/ucd-dnp/ConTexto/)

## Descripción

La librería de procesamiento y análisis de texto, ConTexto, tiene como objetivo principal proporcionar herramientas que simplifiquen las tareas y proyectos que involucren procesamiento y análisis de texto. La librería fue desarrollada en el lenguaje de programación de <em>Python</em> y contiene un conjunto de funciones que permiten realizar transformaciones y análisis de textos de forma simple, utilizando diferentes técnicas para lectura y escritura de archivos de texto, incluyendo reconocimiento óptico de caracteres (OCR), limpieza de textos y remoción de palabras no deseadas para el análisis (<em>stop words</em>), traducción y corrección de textos, generación de nubes de palabras, cálculo de similitudes entre textos, entre otras.

La librería surge como solución a tres principales aspectos. En primer lugar, la necesidad de integrar todos los esfuerzos y desarrollos que ha hecho la Unidad de Científicos de Datos (UCD) del DNP, en proyectos relacionados con la analítica de texto; en segundo lugar, evitar reprocesos en la construcción de scripts para estas tareas, y finalmente, aumentar la cantidad de librerías enfocadas en el análisis de texto en español que existen actualmente.

- A continuación podrá consultar la siguiente información:
  
  - [Prerrequisitos](#prerrequisitos)
  - [Instalación](#instalaci%C3%B3n)
  - [Documentación](#documentaci%C3%B3n)
  - [Ejemplo](#ejemplo)
  - [Contribuciones](#contribuciones)
  - [Licencia](#licencia)
  - [Contacto](#contacto)   

## Prerrequisitos

Antes de proceder con la instalación de ConTexto asegúrese de tener instalado (Estos dos paquetes son necesarios para utilizar el reconocimiento óptico de caracteres (OCR) de ConTexto):

* Tesseract
* Poppler v0.68.0

Para mayor información consultar la [sección de instalación](https://ucd-dnp.github.io/ConTexto/versiones/master/seccion_instalacion.html)

## Instalación

Se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador. Se debe mencionar que se requiere hacer instalaciones adicionales para el correcto funcionamiento de algunos módulos de la librería. Para más información, consultar la [sección de instalación en la página de documentación](https://ucd-dnp.github.io/ConTexto/versiones/master/seccion_instalacion.html).

Para realizar la instalación por medio del gestor de paquetes ``pip`` utilizar los siguientes comandos:

```linux
python -m pip install --upgrade pip
pip install contexto
```

Para realizar la instalación por medio de ``Conda`` utilizar el siguiente comando:

```linux
pip install --extra-index-url https://pypi.org/simple/ contexto
```

## Documentación

La librería cuenta con una documentación que detalla las funciones que la conforman, al igual que ejemplos de uso y demás información de interés relacionada con esta. Para acceder a la documentación, siga el siguiente enlace:

[Documentación - ConTexto - Librería de procesamiento y análisis de textos.](https://ucd-dnp.github.io/ConTexto/)

## Ejemplo

En esta sección nos enfocaremos en presentar unos cortos ejemplos de uso de algunas funciones de la librería teniendo dos enfoques en particular: la limpieza de textos y la visualización de textos. Para mayor información y detalle sobre ejemplos de estas y otras funciones de la librería, se puede consultar la [sección de ejemplos]( https://ucd-dnp.github.io/ConTexto/versiones/master/seccion_ejemplos.html) de la documentación.

### Ejemplo - Limpieza de textos

Para este ejemplo utilizaremos el siguiente texto de prueba.
```python
texto_prueba = '''hola, esto es una prueba para verificar que la limpieza
sea hecha con precisión, empeño y calidad! Esperamos que esté todo de 10.

Desde Amazonas hasta la Guajira y san andrés, desde John y María hasta Ernesto,
esperamos       que todo funcione de manera correcta.'''
```

Se debe importar el módulo de limpieza.

```python
from contexto.limpieza import *
```

La librería cuenta con varias funciones de limpieza como son limpieza_basica, limpieza_texto, remover_acentos, remover_palabras_cortas y otras.

* La función **limpieza_texto** permite realizar una limpieza más completa del texto. La función permite:
  
	- Pasar todo el texto a minúsculas
	- Quitar signos de puntuación
	- Quitar stopwords (palabras y/o expresiones). Para esto, se pueden pasar directamente las listas de palabras y expresiones a quitar, o se puede pasar un archivo que contenga esta información. (configurable)
	- Quitar palabras de una longitud menor a n caracteres (configurable)
	- Quitar números (configurable)
	- Quitar acentos (configurable)
```python
limpio_completo = limpieza_texto(texto_prueba, n_min=3, quitar_acentos=True, 
	lista_palabras = ['esto','sea', 'con', 'que', 'para', 'este', 'una'])

print(limpio_completo)
```
```python
hola prueba verificar limpieza hecha precision empeno calidad esperamos todo desde amazonas hasta guajira san andres desde john maria hasta ernesto esperamos todo funcione manera correcta
```

### Ejemplo - Visualización de textos

Para este ejemplo, se va a trabajar con el texto de la novela **"Don Quijote de la Mancha"**, escrita por Miguel de Cervantes Saavedra. El texto completo de esta novela está en la carpeta de `ejemplos/entrada` del repositorio, y fue descargado desde la página del [Proyecto Gutenberg](https://www.gutenberg.org/), que tiene a su disposición miles de libros de forma gratuita.

Procedemos a importar los módulos necesarios.

```python
from contexto.lectura import leer_texto
from contexto.limpieza import limpieza_texto, lista_stopwords, remover_stopwords
from contexto.exploracion import grafica_barchart_frecuencias
from contexto.exploracion import obtener_ngramas, par_nubes
```

La función **leer_texto** del módulo **lectura** es utilizada para extraer el texto del archivo que contiene la novela. Luego, se realiza una limpieza estándar del texto, para que esté mejor adecuado para su exploración. Para esto, se utilizan las funciones **limpieza_texto** y **lista_stopwords**, del módulo **limpieza**.

Finalmente, en el texto aparece en varias ocasiones la expresión "project gutenberg", el nombre del proyecto que pone a disposición la novela. Como esta información no está directamente relacionada al texto que nos interesa, se va a remover utilizando la función **remover_stopwords**.

* Cargar y limpiar texto de prueba

```python
ruta_cuento = 'entrada/cervantes_don_quijote.txt'

texto_prueba = leer_texto(ruta_cuento)
texto = limpieza_texto(texto_prueba, quitar_numeros=False, n_min=3, lista_palabras=lista_stopwords())
texto = remover_stopwords(texto, lista_expresiones=['project gutenberg'])
```

Una vez limpio el texto, procedemos a utilizar la función **obtener_ngramas** que permite encontrar n-gramas, o conjuntos de n palabras seguidas, donde n es un número entero mayor a cero. Por ejemplo, si n=1 o n=2, la función obtendrá las palabras o los bigramas del texto, respectivamente.Con esta información se puede obtener la frecuencia de cada n-grama, y así conocer cuáles son los más mencionados en el texto. 

Esto puede ser graficado de varias maneras, como por ejemplo mediante nubes de palabras, en las cuales el tamaño de un término es proporcional a su frecuencia de aparición.

* Obtener listas de palabras y bigramas más frecuentes

```python
unigramas = obtener_ngramas(texto, 1)
bigramas = obtener_ngramas(texto, 2)

bigramas[98:105]
```
```python
['ingenioso hidalgo',
 'hidalgo mancha',
 'mancha compuesto',
 'compuesto miguel',
 'miguel cervantes',
 'cervantes saavedra',
 'saavedra tasaron']
```

* Graficar y guardar nubes de palabras y bigramas

Si se utiliza el parámetro "ubicacion_archivo", la imagen generada se guardará en la ubicación especificada.

La función **par_nubes** permite generar un par de nubes de palabras (una junto a otra).

```python
par_nubes(texto, n1=1, n2=2, ubicacion_archivo='salida/nube_uni_bi.jpg')
```

![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/recursos/nube_uni_bi.jpg "Nube de palabras")

* Gráficas de barras con las frecuencias

Los n-gramas más frecuentes también se pueden visualizar mediante gráficas más estándar como, por ejemplo, gráficos de barras que muestren los términos más frecuentes. La función **grafica_barchart_frecuencias** permite obtener estas gráficas.

```python
grafica_barchart_frecuencias(texto, ubicacion_archivo='salida/barras_palabras.jpg', 
                             titulo='Frecuencias de palabras', dim_figura=(7,4))
```

![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/recursos/barras_palabras.jpg "Frecuencia de palabras")

## Control de cambios

Para ver todos los cambios en las versiones de `ConTexto` ver el archivo [changelog](https://github.com/ucd-dnp/ConTexto/wiki/Changelog)

## Contribuciones a ConTexto

Todas las contribuciones, reportes de errores, corrección de errores, las mejoras de la documentación y las ideas son bienvenidas.

Puede encontrar una descripción detallada de cómo contribuir en la [Wiki de ConTexto](https://github.com/ucd-dnp/ConTexto/wiki/)

También lo invitamos a revisar el [:calendar: Tablero **TODO** de ConTexto](https://github.com/users/ucd-dnp/projects/1), donde hay una serie de temas listados en los que el equipo UCD se encuentra trabajando.

## Licencia [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

### **MIT License** 

La librería ConTexto - Librería de procesamiento y análisis de textos se encuentra publicada bajo la licencia MIT <br />
Copyleft (c) 2020 Departamento Nacional de Planeación - DNP Colombia

Para mayor información puede consultar el archivo de [Licencia](https://github.com/ucd-dnp/contexto/blob/master/LICENSE)

## :telephone_receiver: Contacto

Para comunicarse con la Unidad de Científicos de Datos (UCD) de la Dirección de Desarrollo Digital (DDD) del DNP, lo puede hacer mediante el correo electrónico ucd@dnp.gov.co
