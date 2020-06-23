import nltk.stem
from limpieza_texto import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje

### Definir clase para el stemmer ###


class Stemmer():
    def __init__(self, lenguaje):
        # Definir lenguaje del stemmer
        self.definir_lenguaje(lenguaje)
        # Inicializar stemmer
        self.iniciar_stemmer()

    def definir_lenguaje(self, lenguaje):
        self.leng = definir_lenguaje(lenguaje, simplificado=False)

    def iniciar_stemmer(self):
        if self.leng is not None:
            self.stemmer = nltk.stem.SnowballStemmer(self.leng)
        else:
            self.stemmer = None

    def stemming(self, texto, limpiar=True):
        if limpiar:
            texto = limpieza_basica(texto)
        return ' '.join([self.stemmer.stem(palabra)
                         for palabra in texto.split(" ")])


### Definir función que envuelva la funcionalidad básica de la clase ###

def stem_texto(texto, lenguaje='es', limpiar=True, stemmer=None):
    # Si no se provee un stemmer, este debe ser inicializado
    if stemmer is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        stemmer = Stemmer(lenguaje)

    if stemmer.stemmer is None:
        print('Lenguaje no válido.')
        return None

    return stemmer.stemming(texto, limpiar)
