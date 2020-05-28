import json
from spellchecker import SpellChecker
from limpieza_texto import remover_acentos, limpieza_basica
from lenguajes import detectar_lenguaje
from lenguajes import dict_lenguajes, dict_lenguajes_simplificado

### Definir clase para el corrector ortográfico ###

class Corrector():
    def __init__(self, lenguaje, diccionario=None, distancia=2):
        # Definir lenguaje del corrector ortográfico
        self.definir_lenguaje(lenguaje)
        # Inicializar corrector
        self.iniciar_corrector(diccionario)
        self.establecer_distancia(distancia)

    def definir_lenguaje(self, lenguaje):
        leng = remover_acentos(lenguaje)
        leng = leng.lower()
        self.leng = leng

    def iniciar_corrector(self, diccionario):
        if self.leng in dict_lenguajes.keys():
            self.leng = dict_lenguajes[self.leng]
            self.leng = dict_lenguajes_simplificado[self.leng]
            if type(diccionario) == str:
                self.corrector = SpellChecker(local_dictionary=diccionario)
            elif type(diccionario) in [dict, list]:
                self.corrector = SpellChecker(language=self.leng)
                self.actualizar_diccionario(diccionario)
            else:
                self.corrector = SpellChecker(language=self.leng)
        else:
            self.corrector = None
 
    def establecer_distancia(self, distancia):
        self.corrector.distance = distancia

    def actualizar_diccionario(self, diccionario):
        if type(diccionario) == str:
            diccionario = json.load(open(diccionario))
        if type(diccionario) == list:
            diccionario = [palabra.lower() for palabra in diccionario]
            self.corrector.word_frequency.load_words(diccionario)
        elif type(diccionario) == dict:
            self.quitar_palabras(list(diccionario.keys()))
            for key in diccionario.keys():
                self.corrector.word_frequency.load_words([key.lower()]*diccionario[key])
        else:
            pass

    def quitar_palabras(self, palabras):
        if type(palabras) == str:
            palabras = [palabras]
        # Quitar de la lista palabras que no estén en el diccionario
        palabras = [p for p in palabras if self.frecuencia_palabra(p)>0]
        if len(palabras) > 0:
            self.corrector.word_frequency.remove_words(palabras)
        
    def agregar_palabras(self, palabras):
        if type(palabras) == str:
            palabras = [palabras]
        self.actualizar_diccionario(palabras)

    def palabras_conocidas(self, texto):
        return self.corrector.known(texto.split())

    def palabras_desconocidas(self, texto):
        return self.corrector.unknown(texto.split())

    def palabras_candidatas(self, palabra):
        return self.corrector.candidates(palabra)

    def frecuencia_palabra(self, palabra):
        return self.corrector[palabra]

    def probabilidad_palabra(self, palabra):
        return self.corrector.word_probability(palabra)

    def correccion_ortografia(self, texto):
        # Limpieza básica del texto para que no afecte la corrección
        texto = limpieza_basica(texto,quitar_numeros=False)
        lista_palabras = texto.split()
        desconocidas = self.corrector.unknown(lista_palabras)
        texto_corregido = [self.corrector.correction(palabra) if palabra in desconocidas 
                          else palabra for palabra in lista_palabras]
        return ' '.join(texto_corregido)


### Definir función que envuelva la funcionalidad básica de la clase ###

def corregir_texto(texto, lenguaje='es', corrector=None, diccionario=None, distancia=2):
    # Si no se provee un lematizador, este debe ser inicializado
    if corrector is None:
        if lenguaje=='auto':
            lenguaje = detectar_lenguaje(texto)
        corrector = Corrector(lenguaje, diccionario, distancia)
    
    if corrector.corrector is None:
        print('Lenguaje no válido.')
        return None

    return corrector.correccion_ortografia(texto)

