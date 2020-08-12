import os
import spacy

# Información sobre los modelos disponibles para cada idioma: 
# https://spacy.io/models/

def cargar_modelo(dim_modelo, lenguaje):
    dim_modelo = dim_modelo.lower()
    # Estandarizar el tamaño del modelo
    if dim_modelo in ['grande', 'large', 'lg', 'gr']:
        dim_modelo = 'lg'
    elif dim_modelo in ['mediano', 'medio', 'md', 'medium', 'm']:
        dim_modelo = 'md'
    elif dim_modelo in ['pequeño', 'pequeno', 'small', 's', 'sm']:
        dim_modelo = 'sm'
    # Si no se puede distinguir el tamaño del modelo, se retorna un modelo
    # en blanco
    else:
        return spacy.blank(lenguaje)
    # Modelo a cargar de acuerdo a su tamaño y lenguaje
    if lenguaje == 'en':
        language_model = f'{lenguaje}_core_web_{dim_modelo}'
    else:
        language_model = f'{lenguaje}_core_news_{dim_modelo}'
    # Se intenta cargar el modelo
    try:
        lematizador = spacy.load(language_model)
    # Si no funciona, se trata de descargar el modelo, o se usa uno vacío
    except BaseException:
        try:
            print(
                '[INFO] Descargando modelo. Este proceso puede tardar varios minutos.\n')
            os.system(f'python -m spacy download {language_model}')
            print('\n[INFO] El modelo ha sido descargado.')
            print(
                '[INFO] Por favor correr de nuevo el script, o iniciar una nueva sesión de Python para cargarlo.')
            print('[INFO] Hasta entonces, se utilizará un modelo en blanco.\n')
        except BaseException:
            print(
                '\n[INFO] El modelo no pudo ser descargado, se cargará un modelo vacío.\n')
        lematizador = spacy.blank(lenguaje)
    # Devolver el lematizador
    return lematizador