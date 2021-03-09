import os
import spacy


def cargar_modelo(dim_modelo, lenguaje, maxima_longitud=None):
    """
    Carga y retorna un modelo de lenguaje de spaCy del tamaño y lenguaje \
    fijado por el usuario. Para mayor información sobre estos modelos se \
    puede consultar la página de spaCy (https://spacy.io/models/).

    :param dim_modelo: (str). Tamaño del modelo de spaCy que se desea \
        utilizar. Puede ser una de las siguientes opciones, sin hacer \
        distinción entre mayúsculas y minúsculas:
        |ul|  |li| pequeño: {'pequeño', 'pequeno', 'small', 's', 'sm'} |/li|
        |li| mediano: {'mediano', 'medio', 'md', 'medium', 'm'} |/li|
        |li| grande: {'grande', 'large', 'lg', 'gr'} |/li|  |/ul|

        Entre más grande sea el modelo es posible que tenga un soporte de \
        sus características para un vocabulario más amplio. También \
        aumentará el tamaño del archivo de cada modelo. Si un \
        modelo de determinado lenguaje y tamaño no se encuentra en el \
        computador del usuario, la función lo descargará. Una vez descargado \
        el modelo correspondiente, el usuario debe correr la función de nuevo.

    :param lenguaje: (str). Lenguaje para el que se desea cargar el modelo \
        de spaCy. spaCy tiene modelos disponibles para varios lenguajes. \
        Para mayor información, visitar https://spacy.io/models/
    :param maxima_longitud: (int), valor por defecto: None. Parámetro \
        opcional que permite establecer la máxima longitud (número de \
        caracteres) que acepta el vectorizador en un texto de entrada. \
        Si este valor se deja en None, se utilizará la máxima longitud que \
        trae Spacy por defecto (1 millón de caracteres).
    :return: Modelo de spaCy, del tamaño y lenguaje especificados. Si el \
        modelo requerido no está disponible en el computador del usuario, \
        la función descargará el modelo correspondiente, lo cual puede tardar \
        algunos minutos, dependiendo del tamaño de los modelos y la \
        velocidad de conexión a internet del usuario. Si este es el caso, \
        la función retornará un modelo en blanco, del lenguaje especificado \
        por el usuario. A partir de la siguiente vez que se corra la \
        función, esta retornará el modelo ya descargado.
    """
    dim_modelo = dim_modelo.lower()
    # Estandarizar el tamaño del modelo
    if dim_modelo in ["grande", "large", "lg", "gr"]:
        dim_modelo = "lg"
    elif dim_modelo in ["mediano", "medio", "md", "medium", "m"]:
        dim_modelo = "md"
    elif dim_modelo in ["pequeño", "pequeno", "small", "s", "sm"]:
        dim_modelo = "sm"
    # Si no se puede distinguir el tamaño del modelo, se retorna un modelo
    # en blanco
    else:
        return spacy.blank(lenguaje)
    # Modelo a cargar de acuerdo a su tamaño y lenguaje
    if lenguaje == "en":
        language_model = f"{lenguaje}_core_web_{dim_modelo}"
    else:
        language_model = f"{lenguaje}_core_news_{dim_modelo}"
    # Se intenta cargar el modelo
    try:
        modelo = spacy.load(language_model)
    # Si no funciona, se trata de descargar el modelo, o se usa uno vacío
    except BaseException:
        try:
            print(
                (
                    "[INFO] Descargando modelo. Este proceso puede "
                    "tardar varios minutos.\n"
                )
            )
            os.system(f"python -m spacy download {language_model}")
            print("\n[INFO] El modelo ha sido descargado.")
            print(
                (
                    "[INFO] Por favor correr de nuevo el script, "
                    "o iniciar una nueva sesión de Python para cargarlo."
                )
            )
            print("[INFO] Hasta entonces, se utilizará un modelo en blanco.\n")
        except BaseException:
            print(
                (
                    "\n[INFO] El modelo no pudo ser descargado, "
                    "se cargará un modelo vacío.\n"
                )
            )
        modelo = spacy.blank(lenguaje)
    # Se ajusta la máxima longitud, si se especificó
    if maxima_longitud is not None:
        modelo.max_length = maxima_longitud
    # Devolver el modelo
    return modelo
