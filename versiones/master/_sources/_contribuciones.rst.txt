.. _contribuciones:

¿Cómo contribuir?
=================

Guía para hacer contribuciones a la librería ConTexto
-----------------------------------------------------

En esta guía encontrará los pasos necesarios para proponer y contribuir con nuevas características o funcionalidades para **ConTexto**. A continuación se explica cómo hacer un *fork* del código de GitHub, y cómo crear un *pull-request* para proponer cambios a la librería. 

Un *fork* crea una copia del código oficial del repositorio en GitHub a un repositorio local, desde donde se pueden hacer cambios. El *pull-request* es la manera de solicitar que se incorporen en el código oficial los cambios y/o adiciones realizadas por un usuario externo en un *fork* del repositorio.

.. note::
        Los cambios propuestos por los usuarios serán evaluados por el equipo desarrollador de ConTexto; solo ellos decidirán si consideran pertinente y adecuado implementarlos parcial o completamente.

1. Antes de solicitar cambios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1.1** Verifique la correcta `instalación <https://ucd-dnp.github.io/ConTexto/versiones/master/seccion_instalacion.html>`_ de ConTexto y de los paquetes adicionales que requiere para su funcionamiento.

**1.2.** Verifique `la documentación <https://ucd-dnp.github.io/ConTexto/>`_ de la librería para asegurarse de no proponer funcionalidades ya existentes.

**1.3.** Puede considerar enviar un `correo electrónico <mailto:ucd@dnp.gov.co>`_ a los miembros de la Unidad de Científicos de Datos, UCD, antes de proponer un cambio para validar si se está trabajando en una actualización similar. También puede revisar el `Tablero de seguimiento <https://github.com/users/ucd-dnp/projects/1>`_ , donde se reportan las acciones pendientes y en desarrollo de la librería. 

**1.4.** En caso de querer reportar un inconveniente con el código, documentación, instalación o problema en general, se puede comunicar directamente al correo electrónico ucd@dnp.gov.co o abrir un `issue <https://github.com/ucd-dnp/ConTexto/issues>`_ para que el equipo desarrollador haga seguimiento del error.

2. Hacer fork del repositorio original
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El fork (bifurcación) consiste en copiar el código de un proyecto original, que sea público, en un repositorio local. De esta manera es posible modificar el código sin alterar el original al hacer commits sobre el nuevo repositorio. 

.. note::
        Al hacer el fork, se copia el código con los cambios realizados con commits de los desarrolladores del proyecto original y este se actualiza en caso de que añadan cambios.

**Pasos para hacer fork**

**2.1.** Iniciar sesión de GitHub y abrir el repositorio del cual se quiere copiar el código

**2.2.** Dirigirse a la parte superior derecha de la página, donde se encuentra el botón Fork

.. figure:: _static/image/contribuciones/create_fork.jpg
    :align: center
    :alt: 
    :figclass: align-center

Una vez se haya presionado el botón Fork se tendrá una copia del repositorio en la cuenta personal

**2.3.** Clonar el fork

Luego de copiar el repositorio, será posible clonar el fork a la máquina de trabajo personal. Para ello, se escribe el siguiente comando desde el terminal de Git Bash:

.. code-block:: console

        $ git clone https://github.com/{usuario}/{repositorio}.git

Donde {usuario} es el nombre de usuario personal de GitHub y {repositorio} el nombre del repositorio

3. Hacer pull-request con los cambios hechos por el usuario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez hechos los cambios deseados sobre el repositorio copiado con fork, es posible proponer a los desarrolladores del proyecto original los cambios hechos con un pull-request. 

**Pasos para hacer pull-request**

**3.1.** Iniciar sesión en GitHub y abrir el repositorio fork

**3.2.** Oprimir el botón Pull request en la parte superior de la pantalla

.. figure:: _static/image/contribuciones/barra_pull_request.jpg
    :align: center
    :alt: 
    :figclass: align-center

**3.3.** Oprimir el enlace "create a pull request" al final del mensaje de bienvenida a los pull requests que aparece en medio de la pantalla

.. figure:: _static/image/contribuciones/Welcome_pull_requests.jpg
    :align: center
    :alt: 
    :figclass: align-center

Luego de oprimir este botón aparecerá en la pantalla la información general sobre el dueño y nombre del repositorio original, el dueño y nombre del repositorio fork, el número de commits, el número de archivos modificados, los nombres de los commits, entre otros, además del botón con la opción de hacer el pull-request. Esta información se ve de la siguiente manera

.. figure:: _static/image/contribuciones/comparing_changes.jpg
    :align: center
    :alt: 
    :figclass: align-center

Adicionalmente, debajo encuentran los cambios hechos en el código con las líneas de código de color verde cuando fueron añadidas y de color rojo cuando fueron eliminadas

**3.4.** Oprimir el botón Create pull request y llenar formulario

.. figure:: _static/image/contribuciones/boton_create_pull_request.jpg
    :align: center
    :alt: 
    :figclass: align-center

Al oprimir este botón se abrirá una página con un formulario donde se debe que escribir los detalles por las cuales se desea hacer el pull request, los cambios realizados, las funcionalidades nuevas, los elementos eliminados, las correcciones hechas, etc. El formulario se ve de la siguiente manera

.. figure:: _static/image/contribuciones/formulario_pull_request.jpg
    :align: center
    :alt: 
    :figclass: align-center

**3.5.** Enviar formulario

Una vez terminado el formulario se oprime el botón Create pull request en la parte inferior derecha del formulario

.. note::
        Se recomienda fuertemente no desmarcar la opción *Allow edits by maintainers* al final del formulario; Esto permite que el equipo desarrollador pueda hacer cambios sobre el pull-request y evitar solicitar cambios menores sobre su solicitud.


**3.6.** Pull-request aceptado

En caso de que los desarrolladores acepten el pull request, se notificará por medio de correo electrónico al usuario que lo solicitó y se integrará el código al repositorio original. Adicionalmente, el estado del pull-request en GitHub cambiará a Merged

4. Criterios a tener en cuenta para añadir funcionalidades a ConTexto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A continuación se presentan 7 criterios que se tienen que tener en cuenta por un usuario que desee hacer cambios a la librería. Un pull-request podrá ser rechazado por no contar con alguna de estos criterios. 

**4.1.** Mantener coherencia en la interfaz de cara a usuario. Si un nuevo módulo o funcionalidad cambia drásticamente la forma de utilizar la librería, podría considerarse como una reestructuración general que queda por fuera de los propósitos originales de los desarrolladores.

**4.2.** Mantener el código (clases, funciones, variables, etc.) y la documentación en **español**.

**4.3.** Evitar cambiar los nombres de funciones y parámetros ya existentes. Las propuestas con los cambios de nombres serán evaluados por los desarrolladores y se espera que haya una razón suficientemente clara y detallada de la razón del cambio. 

**4.4.** Evitar añadir nuevas dependencias de paquetes y software. Hacerlo solo si representa un avance significativo en funcionalidad o desempeño que a la vez sean demostrables.

**4.5.** Todo el código en Python de la librería sigue el estilo `pep8`, por lo cual se espera que los cambios propuestos en el código sigan este formato. Se propone utilizar la librería *autopep8* para ajustar el estilo del código. Esta se instala con el siguiente comando:

.. code-block:: console

        pip install autopep8

Con el siguiente código en la línea de comando se adecúa el script al formato `pep8`:

.. code-block:: console

        autopep8 nombre_script.py --in-place

**4.6.** Todo script que haga parte de la librería debe estar debidamente comentado para que sea claro qué se está haciendo.

**4.7.** Se recomienda fuertemente hacer commits granulares por cada cambio que se proponga, con el fin de aceptar con mayor facilidad estos cambios. Más específicamente, realizar commits por cada archivo o script modificado. Adicionalmente, se recomienda separar en commits distintos las inclusiones de nuevas funcionalidades y los cambios en el código ya existente, incluso si se encuentran en el mismo script.

**4.8.** En caso de agregar una función nueva o modificar una existente, tener en cuenta el estilo de documentación de cada función. La documentación se escribe al comienzo de cada función en formato string. Contiene una descripción de la función, una para cada parámetro y una última para el objeto retornado. Los parámetros se describen luego de ser definidos con **:param *nombre*: (*tipo*)** y el objeto que retorna la función se describe luego de definir **:return *nombre*: (*tipo*)**. 

.. figure:: _static/image/contribuciones/documentacion_ejemplo.jpg
    :align: center
    :alt: 
    :figclass: align-center

**4.9.** El formulario del pull-request, donde se describen los cambios hechos para ser añadidos, tiene que ser lo suficientemente claro para que los desarrolladores entiendan el cambio propuesta y su relevancia. 

.. note::
        Los cambios propuestos por usuarios externos a la librería serán verificados por los desarrolladores de la librería y solo ellos decidirán si se incluye en su totalidad, parcialmente o si no se incluye


5. Propuestas y contribuciones por fuera del pull-request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En caso de que un usuario tenga una propuesta concreta y desee informársela a los desarrolladores de ConTexto, sin hacer uso del pull-request, puede enviar un correo electrónico a ucd@dnp.gov.co con la nueva funcionalidad o cambio que desearía que se integre.
