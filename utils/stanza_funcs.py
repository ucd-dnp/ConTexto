import os
import stanza
import torch

# Información sobre los procesadores disponibles:
# https://stanfordnlp.github.io/stanza/pipeline.html#processors


def stanza_pipeline(
        leng,
        procesors='tokenize, pos, lemma',
        lemma_model_path='',
        ner_model_path='',
        pos_model_path=''):
    # Configuración básica del pipeline
    config = {
        'processors': procesors,
        'lang': leng,
    }
    # Si se añade algún modelo custom, se agrega al diccionario
    if pos_model_path != '':
        config['pos_model_path'] = pos_model_path
    if lemma_model_path != '':
        config['lemma_model_path'] = lemma_model_path
    if ner_model_path != '':
        config['ner_model_path'] = ner_model_path
    # Intentar crear pipeline. Si el modelo no está descargado, se descarga
    # primero
    try:
        nlp_pipe = stanza.Pipeline(**config, verbose=0, )
    except BaseException:
        print('[INFO] Descargando modelo. Este proceso puede tardar varios minutos.\n')
        stanza.download(leng)
        nlp_pipe = stanza.Pipeline(**config, verbose=0)
    # Retornar pipeline
    return nlp_pipe


def modificar_modelo(tipo, new_dict, in_path='', out_path='', location='cpu'):
    # opciones de tipo: 'lemma', 'pos', 'tokenize'
    # Definir ubicación del modelo
    if in_path == '':
        processor = [
            i for i in nlp_pipe.loaded_processors if tipo.lower() in str(i).lower()][0]
        in_path = processor.config['model_path']
    # Cargar modelo y diccionarios del modelo
    model = torch.load(in_path, map_location=location)
    word_dict, composite_dict = model['dicts']
    # Añadir nuevas palabras
    for key in new_dict:
        if isinstance(key, tuple):
            composite_dict[key] = new_dict[key]
        else:
            word_dict[key] = new_dict[key]
    # Establecer dónde se va a guardar el modelo
    borrar_modelo = False
    if out_path == '':
        borrar_modelo = True
        out_path = "{}.pt".format(os.getpid())
    # Guardar modelo modificado
    torch.save(model, out_path)
    # Cargar el modelo modificado
    tipo = tipo.lowe()
    if tipo == 'lemma':
        nlp_pipe = stanza_pipeline('es', lemma_model_path=out_path)
    elif tipo == 'pos':
        nlp_pipe = stanza_pipeline('es', pos_model_path=out_path)
    elif tipo == 'ner':
        nlp_pipe = stanza_pipeline('es', ner_model_path=out_path)
    # Si no se especificó una ubicación para el modelo resultante, este se
    # borra
    if borrar_modelo:
        os.remove(out_path)
    # Devolver modelo modificado
    return nlp_pipe
