# Documentación ConTexto - Librería de procesamiento y análisis de textos

![screenshot](https://raw.githubusercontent.com/ucd-dnp/contexto/master/recursos/contexto.jpg "ConTexto")

[![PyPI version fury.io](https://badge.fury.io/py/ConTexto.svg)](https://pypi.org/project/ConTexto/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ConTexto.svg)](https://pypi.org/project/ConTexto/)
 [![PyPI license](https://img.shields.io/pypi/l/ConTexto.svg)](https://pypi.org/project/ConTexto/) [![Downloads](https://pepy.tech/badge/contexto)](https://pepy.tech/project/contexto) [![GitHub forks](https://img.shields.io/github/forks/ucd-dnp/ConTexto.svg?style=social&label=Fork&maxAge=2592000)](https://github.com/ucd-dnp/ConTexto/)

## Descripción

Esta rama del repositorio tiene como objetivo principal organizar la documentación de las diferentes versiones de ConTexto para hacer el hosting de estas a través del servicio [GitHub Pages](https://pages.github.com/).

Para acceder a información relevante de la librería debe dirigirse a la [rama principal](https://github.com/ucd-dnp/ConTexto) del repositorio o acceder a la [documentación de la librería](https://ucd-dnp.github.io/ConTexto/).

## Actualización de la documentación

### 1. Cree un entorno virtual e instale las librerías necesarias mediante el archivo requirements.txt o proceda a instalar las siguientes librerías.

```console
pip install contexto
pip install sphinx==4.0.0
pip install pydata_sphinx_theme
pip install sphinx_copybutton
pip install sphinx-multiversion
```

### 2. Actualizar los documentos

* Active el branch gh-pages
* Borre la carpeta versiones
* Modifique el archivo **sphinx/source/conf.py** en caso de ser necesario (si se crea un nuevo release)
* Desde la carpeta base corra el comando 
    ```console
    sphinx-multiversion ./sphinx/source .
    ```
* Haga commit y push en el branch gh-pages con los nuevos archivos

### 3. Solución a posibles errores

#### - El tema sphinx_rtd_theme no tiene la pestaña de versiones

* Debe asegurarse que el archivo de configuración **sphinx/source/conf.py** tenga definida la ruta de templates ***templates_path = ['_templates']***

* Incluir la plantilla de versiones ***sphinx/source/_templates/versions.html***

* Para mayor detalle puede consultar el enlace: [**ReadTheDocs Theme**](https://holzhaus.github.io/sphinx-multiversion/master/templates.html#readthedocs-theme). Vale la pena mencionar que se utiliza una plantilla similar a la presentada en el enlace anterior. Sin embargo, se modificó para poder cambiar el nombre del branch master

#### - Al actualizar la documentación no se genera la documentación de un release o branch

* Debe verificar la configuración del archivo **sphinx/source/conf.py**
    Las variables ***smv_tag_whitelist*** y ***smv_branch_whitelist*** contienen expresiones regulares que permiten ignorar tags o ramas en particular
	* Para mayor información puede consultar el enlace [**Configuración sphinx-multiversion**](https://holzhaus.github.io/sphinx-multiversion/master/configuration.html)

* Otra posible causa de este error es que no estén sincronizados los tags remotos con los tags locales. Puede utilizar los siguientes comando:
	* Permite consultar los tags locales
	```console
	git tag
	```

	* Permite consultar los tags remotos
	```console
	git ls-remote --tags
	```

	* Permite sincronizar los tags remotos/locales
	```console
	git fetch --prune
	```
         
#### - Los nombres de las versiones están mal
    
* En el tema *ReadTheDocs* hay dos partes donde se puede ver la versión que se está consultando.
    
    1. En la esquina superior izquierda debajo del logo. Este valor se toma de la variable ***version*** del archivo ***sphinx/source/conf.py***. Para modificar el valor de una versión en particular se debe modificar esta variable en la rama o release respectivo.

    2. En la esquina inferior izquierda en la sección de versiones. Los nombres de las versiones se toman del **nombre de las ramas o tags**, a excepción de la rama master. El nombre de la rama master se está modificando en el template sphinx/source/_templates/versions.html
