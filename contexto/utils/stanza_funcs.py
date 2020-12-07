import os
import stanza
import torch


def stanza_pipeline(lenguaje, procesadores='tokenize, pos, lemma', modelo_lemas='',
                    modelo_ner='', modelo_pos=''):
    """
    Carga y retorna un pipeline, o flujo de trabajo, de Stanza del y lenguaje y con los procesos \
        especificados por el usuario. Los procesos que el usuario puede elegir añadir al pipeline incluyen \
        tokenización, *Part of Speech* (POS), lematización y *Named Entity Recognition* (NER), entre otros. \
        Para mayor información sobre estos modelos y los pipelines se puede consultar la página web \
        de Stanza (https://stanfordnlp.github.io/stanza/pipeline.html#processors).

    :param lenguaje: (str). Lenguaje para el que se desean cargar los modelos de Stanza. Stanza tiene modelos \
        disponibles para varios lenguajes, dependiendo de la función a realizar. Para mayor información, visitar \
        https://stanfordnlp.github.io/stanza/available_models.html
    :param procesadores: (str). Valor por defecto: 'tokenize, pos, lemma'. Lista de procesadores, también \
        entendidos como procesos o tareas que se desean aplicar a un texto de entrada, que se desean incluir \
        en el pipeline. Se ingresa un string en el que los diferentes procesadores van separados por comas.
    :param modelo_lemas: (str). Valor por defecto: ''. Unicación de un archivo que contenga el modelo o procesador \
        que el usuario desea utilizar para aplicar lematización a los textos. Si este parámetro se deja vacío, se \
        utilizará el procesador disponible de la librería Stanza para el lenguaje especificado.  
    :param modelo_ner: (str). Valor por defecto: ''. Unicación de un archivo que contenga el modelo o procesador \
        que el usuario desea utilizar para aplicar *Named Entity Recognition* a los textos. Si este parámetro se deja \
        vacío, se utilizará el procesador disponible de la librería Stanza para el lenguaje especificado.
    :param modelo_pos: (str). Valor por defecto: ''. Unicación de un archivo que contenga el modelo o procesador \
        que el usuario desea utilizar para aplicar *Part of Speech* a los textos. Si este parámetro se deja vacío, se \
        utilizará el procesador disponible de la librería Stanza para el lenguaje especificado.                          
    :return: (stanza Pipeline). Pipeline de Stanza, del lenguaje especificado, con los procesadores determinados por \
        el usuario. Si los modelos requeridos no están disponibles en el computador del usuario, la función descargará \
        los modelos correspondientes, lo cual puede tardar algunos minutos dependiendo del tamaño de los modelos y la \
        velocidad de conexión a internet del usuario. 
    """
    # Configuración básica del pipeline
    config = {
        'processors': procesadores,
        'lang': lenguaje,
    }
    # Si se añade algún modelo custom, se agrega al diccionario
    if modelo_pos != '':
        config['pos_model_path'] = modelo_pos
    if modelo_lemas != '':
        config['lemma_model_path'] = modelo_lemas
    if modelo_ner != '':
        config['ner_model_path'] = modelo_ner
    # Intentar crear pipeline. Si el modelo no está descargado, se descarga
    # primero
    try:
        nlp_pipe = stanza.Pipeline(**config, verbose=0, )
    except BaseException:
        print('[INFO] Descargando modelo. Este proceso puede tardar varios minutos.\n')
        stanza.download(lenguaje)
        nlp_pipe = stanza.Pipeline(**config, verbose=0)
    # Retornar pipeline
    return nlp_pipe


def modificar_modelo(nlp_pipe, tipo, nuevo_diccionario, archivo_entrada='',
                     archivo_salida='', gpu=False):
    """
    A partir de un diccionario de entrada, modifica un procesador de un pipeline existente de Stanza.

    :param nlp_pipe: (stanza Pipeline). Pipeline de Stanza que contiene el procesador que se desea modificar.
    :param tipo: (str) ['lemma', 'pos', 'tokenize']. Tipo de procesador o modelo que se desea modificar.
    :param nuevo_diccionario: (dict). Diccionario de Python que contiene los elementos para añadir o modificar \
        en el modelo que se desea cambiar. Las llaves y los valores de este diccionario pueden tener distinta \
        información, dependiendo del tipo de modelo que se va a modificar. Por ejemplo, para modificar el \
        modelo de lematización (tipo='lemma'), las llaves del diccionario serán palabras y los valores del \
        diccionario serán los lemas.
    :param archivo_entrada: (str). Valor por defecto: ''. Ubicación del archivo que contiene el modelo o \
        procesador que se desea modificar. Si de deja vacío este parámetro, la modificación se hará sobre \
        el modelo que trae por defecto el pipeline de Stanza.
    :param archivo_salida: (str). Valor por defecto: ''. Ubicación y nombre del archivo en donde se desea \
        guardar el modelo o procesador modificado. Si este valor se deja vacío, la función retornará el \
        pipeline con el modelo modificado, pero el modelo no será guardado. 
    :param gpu: (bool). Valor por defecto: False. Parámetro opcional que permite al usuario especificar si \
        va a utilizar una GPU para cargar y modificar los objetos (modelos) de PyTorch.     
    :return: (stanza Pipeline). Pipeline de entrada, después de modificar el procesador o modelo determinado \
        por el usuario. 
    """
    # Definir ubicación del modelo
    tipo = tipo.lower()
    if archivo_entrada == '':
        procesador = [
            i for i in nlp_pipe.loaded_processors if tipo in str(i).lower()][0]
        archivo_entrada = procesador.config['model_path']
    # Cargar modelo y diccionarios del modelo
    locacion = 'gpu' if gpu else 'cpu'
    modelo = torch.load(archivo_entrada, map_location=locacion)
    if 'lemma' in tipo:
        dict_palabras, dict_compuesto = modelo['dicts']
        # Añadir nuevas palabras
        for key in nuevo_diccionario:
            if isinstance(key, tuple):
                dict_compuesto[key] = nuevo_diccionario[key]
            else:
                dict_palabras[key] = nuevo_diccionario[key]
    # TODO: falta completar los otros casos, se mirará cuando se incluya POS y NER en la librería
    else:
        dict_vocab = modelo['vocab']
        # Acá falta seguir el proceso para cada caso
    # Establecer dónde se va a guardar el modelo
    borrar_modelo = False
    if archivo_salida == '':
        borrar_modelo = True
        archivo_salida = "{}.pt".format(os.getpid())
    # Guardar modelo modificado
    torch.save(modelo, archivo_salida)
    # Cargar el modelo modificado
    tipo = tipo.lower()
    if tipo == 'lemma':
        nlp_pipe = stanza_pipeline('es', modelo_lemas=archivo_salida)
    elif tipo == 'pos':
        nlp_pipe = stanza_pipeline('es', modelo_pos=archivo_salida)
    elif tipo == 'ner':
        nlp_pipe = stanza_pipeline('es', modelo_ner=archivo_salida)
    # Si no se especificó una ubicación para el modelo resultante, este se
    # borra
    if borrar_modelo:
        os.remove(archivo_salida)
    # Devolver modelo modificado
    return nlp_pipe
