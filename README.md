# ConTexto - Librería de procesamiento y análisis de textos

![screenshot](https://raw.githubusercontent.com/ucd-dnp/contexto/master/docs/_images/contexto.jpg "LEILA")

## Descripción

La librería de procesamiento y análisis de texto, ConTexto, tiene como objetivo principal proporcionar herramientas que simplifiquen las tareas y proyectos que involucren análisis de texto. La librería fue desarrollada en el lenguaje de programación de <em>Python</em> y contiene un conjunto de funciones que permiten realizar transformaciones y análisis de textos de forma simple, utilizando diferentes técnicas, para lectura y escritura de archivos de texto, incluyendo reconocimiento óptico de caracteres (OCR), limpieza de textos y remoción de palabras no deseadas para el análisis (<em>stop words</em>), traducción y corrección de textos, generación de nubes de palabras, cálculo de similitudes entre textos, entre otras, reconocidas por su buen desempeño.

La librería surge como solución a tres principales aspectos, primero, la necesidad de integrar todos los esfuerzos y desarrollos que ha hecho la Unidad de Científicos de Datos (UCD) del DNP, en proyectos relacionados con la analítica de texto, segundo, evitar reprocesos en la construcción de scripts para estas tareas, y finalmente, contribuir en la reducción de la escasez de librerías enfocadas en el análisis de texto en español que existe actualmente. 

- A continuación podrá consultar la siguiente información:
  - [Ejemplo](#ejemplo)
  - [Documentación](#documentaci%C3%B3n)  
  - [Instalación](#instalaci%C3%B3n)
  - [Contribuciones](#contribuciones)
  - [Licencia](#licencia)
  - [Contacto](#contacto)

## Ejemplo

En esta sección presentaremos dos ejemplos de funciones de la librería, el primero correspondiente a la limpieza de textos y el segundo sobre la visualización de textos. Para mayor información y detalle sobre ejemplos de estas y otras funciones de la librería, puede consultar la [sección de ejemplos]( https://ucd-dnp.github.io/ConTexto/seccion_ejemplos.html) de la documentación.

### Ejemplo - Limpieza de textos

Para este ejemplo utilizaremos el siguiente texto de prueba.
```
texto_prueba = '''hola, esto es una prueba para verificar que la limpieza
sea hecha con precisión, empeño y calidad! Esperamos que esté todo de 10.

Desde Amazonas hasta la Guajira y san andrés, desde John y María hasta Ernesto,
esperamos       que todo funcione de manera correcta.'''
```

Se debe importar el módulo de limpieza.

```
from contexto.limpieza import *
```

La librería cuenta con varias funciones de limpieza como son:

* **limpieza_basica**, pasa el texto a minúsculas, elimina signos de puntuación y números.
```
limpio_basico = limpieza_basica(texto_prueba)
print(limpio_basico)
```
```
hola esto es una prueba para verificar que la limpieza sea hecha con precisión empeño y calidad esperamos que esté todo de desde amazonas hasta la guajira y san andrés desde john y maría hasta ernesto esperamos que todo funcione de manera correcta
```
Si desea mantener los caracteres numéricos se debe asignar el parámetro quitar_numeros como *False*
```
limpio_basico_nums = limpieza_basica(texto_prueba, quitar_numeros=False)
print(limpio_basico_nums)
```
```
hola esto es una prueba para verificar que la limpieza sea hecha con precisión empeño y calidad esperamos que esté todo de 10 desde amazonas hasta la guajira y san andrés desde john y maría hasta ernesto esperamos que todo funcione de manera correcta
```

* **remover_acentos**, remueve acentos del texto (diéresis, tildes y virgulillas).
```
sin_acentos = remover_acentos(limpio_basico)
print(sin_acentos)
```
```
hola esto es una prueba para verificar que la limpieza sea hecha con precision empeno y calidad esperamos que este todo de desde amazonas hasta la guajira y san andres desde john y maria hasta ernesto esperamos que todo funcione de manera correcta
```

* **remover_palabras_cortas**, permite remover palabras con una longitud estrictamente menor a *n_min*.
```
quitar_caracteres = remover_palabras_cortas(sin_acentos, n_min=5)
print(quitar_caracteres)
```
```
prueba verificar limpieza hecha precision empeno calidad esperamos desde amazonas hasta guajira andres desde maria hasta ernesto esperamos funcione manera correcta
```

* La función **limpieza_texto** permite realizar una limpieza más completa del texto, ya que contiene las funcionalidades descritas anteriormente y otras.
La función permite:
  
	- Pasar todo el texto a minúsculas
	- Quitar signos de puntuación
	- Quitar stopwords (palabras y/o expresiones). Para esto, se pueden pasar directamente las listas de palabras y expresiones a quitar, o se puede pasar un archivo que contenga esta información.
	- Quitar palabras de una longitud menor a n caracteres (configurable)
	- Quitar números (configurable)
	- Quitar acentos (configurable)
  
```
limpio_completo = limpieza_texto(texto_prueba, n_min=3, quitar_acentos=True, 
	lista_palabras = ['esto','sea', 'con', 'que', 'para', 'este', 'una'])

print(limpio_completo)
```
```
hola prueba verificar limpieza hecha precision empeno calidad esperamos todo desde amazonas hasta guajira san andres desde john maria hasta ernesto esperamos todo funcione manera correcta
```

### Ejemplo - Visualización de textos

![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/docs/_static/image/graficos/nube_bi.jpg "Nube de palabras")
![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/docs/_static/image/graficos/nube_uni_bi.jpg "Nube de palabras")
![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/docs/_static/image/graficos/barras_palabras.jpg "Nube de palabras")
![screenshot](https://raw.githubusercontent.com/ucd-dnp/ConTexto/master/docs/_static/image/graficos/barras_bigramas.jpg "Nube de palabras")



## Documentación

La librería cuenta con una documentación que detalla las funciones que la conforman, al igual que ejemplos de uso y demás información de interés relacionada con esta, para acceder a la documentación siga el siguiente link:

[Documentación - ConTexto - Librería de procesamiento y análisis de textos.](https://ucd-dnp.github.io/ConTexto/)

## Instalación

Para la instalación de la librería se debe utilizar el gestor de paquetes ``pip``, por buenas prácticas se sugiere antes de la instalación crear un entorno virtual que permita aislar las librerías y evitar conflictos de versiones con el entorno de desarrollo base del computador. Se debe mencionar que se requiere hacer instalaciones adicionales, para más información consultar la sección de instalación en la página de [documentación](https://ucd-dnp.github.io/ConTexto/seccion_instalacion.html).

```
pip install contexto
```

## Contribuciones

Para sugerir mejoras, cambios en la librería o seguir el avance de la solución de errores reportados, debe acceder a la sección de [Issues](https://github.com/ucd-dnp/contexto/issues) del repositorio.

## Licencia

La librería LEILA - Calidad de datos se encuentra publicada bajo la licencia MIT <br />
Copyleft (c) 2020 Departamento Nacional de Planeación - DNP Colombia

Para mayor información puede consultar el archivo de [Licencia](https://github.com/ucd-dnp/contexto/blob/master/LICENSE)

## Contacto

Para comunicarse con la Unidad de Científicos de Datos (UCD) de la Dirección de Desarrollo Digital (DDD) del DNP, lo puede hacer mediante el correo electrónico ucd@dnp.gov.co
