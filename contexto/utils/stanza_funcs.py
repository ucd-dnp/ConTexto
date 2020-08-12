import os
import stanza
import torch

# Información sobre los procesadores disponibles:
# https://stanfordnlp.github.io/stanza/pipeline.html#processors


def stanza_pipeline(
        lenguaje,
        procesadores='tokenize, pos, lemma',
        modelo_lemas='',
        modelo_ner='',
        modelo_pos=''):
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


def modificar_modelo(
        nlp_pipe,
        tipo,
        nuevo_diccionario,
        archivo_entrada='',
        archivo_salida='',
        gpu=False):
    # opciones de tipo: 'lemma', 'pos', 'tokenize'
    # Definir ubicación del modelo
    if archivo_entrada == '':
        procesador = [
            i for i in nlp_pipe.loaded_processors if tipo.lower() in str(i).lower()][0]
        archivo_entrada = procesador.config['model_path']
    # Cargar modelo y diccionarios del modelo
    locacion = 'gpu' if gpu else 'cpu'
    modelo = torch.load(archivo_entrada, map_location=locacion)
    dict_palabras, dict_compuesto = modelo['dicts']
    # Añadir nuevas palabras
    for key in nuevo_diccionario:
        if isinstance(key, tuple):
            dict_compuesto[key] = nuevo_diccionario[key]
        else:
            dict_palabras[key] = nuevo_diccionario[key]
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
