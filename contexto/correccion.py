import json
from spellchecker import SpellChecker
from limpieza import limpieza_basica
from lenguajes import detectar_lenguaje, definir_lenguaje

### Definir clase para el corrector ortográfico ###


class Corrector():
    def __init__(self, lenguaje, diccionario=None, distancia=2):
        """

        :param lenguaje:
        :param diccionario:
        :param distancia:
        """
        # Definir lenguaje del corrector ortográfico
        self.establecer_lenguaje(lenguaje)
        # Inicializar corrector
        self.iniciar_corrector(diccionario)
        self.establecer_distancia(distancia)

    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje:
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_corrector(self, diccionario):
        """

        :param diccionario:
        :return:
        """
        self.corrector = None
        if self.lenguaje is not None:
            if isinstance(diccionario, str):
                self.corrector = SpellChecker(local_dictionary=diccionario)
            elif type(diccionario) in [dict, list]:
                self.corrector = SpellChecker(language=self.lenguaje)
                self.actualizar_diccionario(diccionario)
            else:
                self.corrector = SpellChecker(language=self.lenguaje)

    def establecer_distancia(self, distancia):
        """

        :param distancia:
        :return:
        """
        if self.corrector is not None:
            self.corrector.distance = distancia

    def actualizar_diccionario(self, diccionario):
        """

        :param diccionario:
        :return:
        """
        if isinstance(diccionario, str):
            diccionario = json.load(open(diccionario))
        if isinstance(diccionario, list):
            diccionario = [palabra.lower() for palabra in diccionario]
            self.corrector.word_frequency.load_words(diccionario)
        elif isinstance(diccionario, dict):
            self.quitar_palabras(list(diccionario.keys()))
            for key in diccionario.keys():
                self.corrector.word_frequency.load_words(
                    [key.lower()] * diccionario[key])
        else:
            pass

    def quitar_palabras(self, palabras):
        """

        :param palabras:
        :return:
        """
        if isinstance(palabras, str):
            palabras = [palabras]
        # Quitar de la lista palabras que no estén en el diccionario
        palabras = [p for p in palabras if self.frecuencia_palabra(p) > 0]
        if len(palabras) > 0:
            self.corrector.word_frequency.remove_words(palabras)

    def agregar_palabras(self, palabras):
        """

        :param palabras:
        :return:
        """
        if isinstance(palabras, str):
            palabras = [palabras]
        self.actualizar_diccionario(palabras)

    def palabras_conocidas(self, texto):
        """

        :param texto:
        :return:
        """
        return self.corrector.known(texto.split())

    def palabras_desconocidas(self, texto):
        """

        :param texto:
        :return:
        """
        return self.corrector.unknown(texto.split())

    def palabras_candidatas(self, palabra):
        """

        :param palabra:
        :return:
        """
        return self.corrector.candidates(palabra)

    def frecuencia_palabra(self, palabra):
        """

        :param palabra:
        :return:
        """
        return self.corrector[palabra]

    def probabilidad_palabra(self, palabra):
        """

        :param palabra:
        :return:
        """
        return self.corrector.word_probability(palabra)

    def correccion_ortografia(self, texto, limpieza=True):
        """

        :param texto:
        :param limpieza:
        :return:
        """
        if limpieza:
            # Limpieza básica del texto para que no afecte la corrección
            texto = limpieza_basica(texto, quitar_numeros=False)
        lista_palabras = texto.split()
        desconocidas = self.corrector.unknown(lista_palabras)
        texto_corregido = [self.corrector.correction(palabra) if palabra in desconocidas
                           else palabra for palabra in lista_palabras]
        return ' '.join(texto_corregido)


# todo: Definir función que envuelva la funcionalidad básica de la clase

def corregir_texto(texto, lenguaje='es', corrector=None, diccionario=None, distancia=2, limpieza=True):
    """ Si no se provee un corrector, este debe ser inicializado

    :param texto:
    :param lenguaje:
    :param corrector:
    :param diccionario:
    :param distancia:
    :param limpieza:
    :return:
    """

    if corrector is None:
        if lenguaje == 'auto':
            lenguaje = detectar_lenguaje(texto)
        corrector = Corrector(lenguaje, diccionario, distancia)

    if corrector.corrector is None:
        print('Lenguaje no válido.')
        return None

    return corrector.correccion_ortografia(texto, limpieza)
