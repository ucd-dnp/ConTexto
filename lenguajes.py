from langid.langid import LanguageIdentifier, model
from googletrans import Translator

def detectar_lenguaje(texto, devolver_proba=False):
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    if devolver_proba:
        return identifier.classify(texto)
    else:
        return identifier.classify(texto)[0]

def traducir_texto(texto,lenguaje_destino):
    traductor = Translator()
    out = traductor.translate(texto, dest=lenguaje_destino)
    if type(texto) == str:
        return out.text
    else:
        return [i.text for i in out]
