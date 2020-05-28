import json
import nltk.stem
import spacy
from limpieza_texto import remover_acentos
from lenguajes import detectar_lenguaje
from lenguajes import dict_lenguajes, dict_lenguajes_simplificado

### Definir clases para el lematizador y el stemmer ###


class Lematizador():
    def __init__(self, lenguaje, dict_lemmas=None):
        # Definir lenguaje del lematizador
        self.definir_lenguaje(lenguaje)
        # Inicializar lematizador
        self.iniciar_lematizador()
        # Si se introdujo un diccionario personalizado, se utiliza
        if isinstance(dict_lemmas, dict):
            self.modificar_lemmas(dict_lemmas)
        # Si es la ubicación del archivo, primero se carga
        elif isinstance(dict_lemmas, str):
            dict_lemmas = json.load(open(dict_lemmas))
            self.modificar_lemmas(dict_lemmas)

    def definir_lenguaje(self, lenguaje):
        leng = remover_acentos(lenguaje)
        leng = leng.lower()
        self.leng = leng

    def iniciar_lematizador(self, modelo=''):
        if self.leng in dict_lenguajes.keys():
            self.leng = dict_lenguajes[self.leng]
            self.leng = dict_lenguajes_simplificado[self.leng]
            if modelo != '':
                pass
            else:
                self.lematizador = spacy.blank(self.leng)
        else:
            self.lematizador = None

    def modificar_lemmas(self, dict_lemmas):
        dict_lemmas = dict_lemmas

        def cambiar_propiedades_lemma(doc):
            for token in doc:
                if(token.text in dict_lemmas):
                    token.lemma_ = dict_lemmas[token.text]
            return doc
        if (self.lematizador is not None) and (self.lematizador != -1):
            self.lematizador.add_pipe(cambiar_propiedades_lemma, first=True)

    def lematizar(self, texto):
        texto = texto.lower()
        return ' '.join([token.lemma_ for token in self.lematizador(texto)])


class Stemmer():
    def __init__(self, lenguaje):
        # Definir lenguaje del stemmer
        self.definir_lenguaje(lenguaje)
        # Inicializar stemmer
        self.iniciar_stemmer()

    def definir_lenguaje(self, lenguaje):
        leng = remover_acentos(lenguaje)
        leng = leng.lower()
        self.leng = leng

    def iniciar_stemmer(self):
        if self.leng in dict_lenguajes.keys():
            self.leng = dict_lenguajes[self.leng]
            self.stemmer = nltk.stem.SnowballStemmer(self.leng)
        else:
            self.stemmer = None

    def stemming(self, texto):
        return ' '.join([self.stemmer.stem(palabra)
                         for palabra in texto.split(" ")])


### Definir funciones que envuelvan la funcionalidad básica de las clases ###

def lematizar_texto(texto, lenguaje='es', lematizador=None, dict_lemmas=None):
    # Si no se provee un lematizador, este debe ser inicializado
    if lematizador is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        lematizador = Lematizador(lenguaje, dict_lemmas)

    if lematizador.lematizador is None:
        print('Lenguaje no válido.')
        return None

    return lematizador.lematizar(texto)


def stem_texto(texto, lenguaje='es', stemmer=None):
    # Si no se provee un stemmer, este debe ser inicializado
    if stemmer is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        stemmer = Stemmer(lenguaje)

    if stemmer.stemmer is None:
        print('Lenguaje no válido.')
        return None

    return stemmer.stemming(texto)
