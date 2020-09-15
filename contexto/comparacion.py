import jellyfish
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from lenguajes import definir_lenguaje
from vectorizacion import VectorizadorWord2Vec
from utils.auxiliares import cargar_objeto

# Para que no se muestre la warning de "DataConversionWarning"
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

# Función auxiliar
def jaccard_textos(texto1, texto2):
    if type(texto1) == str:
        texto1 = texto1.split()
    if type(texto2) == str:
        texto2 = texto2.split()
    intersection = set(texto1).intersection(set(texto2))
    union = set(texto1).union(set(texto2))
    return np.array([[len(intersection)/len(union)]])

### Clase Similitud ----------------------------------------------------

class Similitud():
    def __init__(self, vectorizador=None, lenguaje='es'):
        """Constructor de la clase Similitud. \ 
            Permite calcular la similitud coseno y jaccard entre textos.

        :param vectorizador: objeto tipo vectorizador. \ 
            Valor por defecto: None. \ 
            Carga y establece el vectorizador del objeto Similitud. \ 
            Si no se especifica un \ 
            vectorizador se utilizará uno de tipo Word2Vec. Si se pasa un \ 
            vectorizador al objeto de Similitud, este ya debe estar ajustado.
        :param lenguaje: (str) {'es', 'en', 'de', 'fr'}. \ 
            valor por defecto: 'es'. Indica el lenguaje que utilizará el \ 
            vectorizador, soporta los lenguajes Español(es), Inglés(en), \ 
            Alemán(de) y Francés(fr).        
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)
        
    def establecer_lenguaje(self, lenguaje):
        """Establece el lenguaje del objeto Similitud.

        :param lenguaje: (str) {'es', 'en', 'de', 'fr'}. \ 
            Valor por defecto: 'es'. Indica el lenguaje que utilizará el \ 
            vectorizador, soporta los lenguajes Español(es), Inglés(en), \ 
            Alemán(de) y Francés(fr).
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):
        """Establece el vectorizador del objeto Similitud.

        :param vectorizador: objeto tipo vectorizador. Carga y establece el \ 
            vectorizador del objeto Similitud. Si no se especifica un \ 
            vectorizador se utilizará uno de tipo Word2Vec. Si se pasa un \ 
            vectorizador al objeto de Similitud, este ya debe estar ajustado.
        """
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def coseno(self, textos):
        """Calcula la similitud coseno entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de similitud. También es posible ingresar directamente \ 
            los vectores pre-calculados de los textos.
        :return: array con el valor de similitud entre textos. valor entre  \ 
            0 y 1, donde 1 representa que los textos son iguales.
        """
        if isinstance(textos, str) or len(textos) < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        # Si se ingresan textos, estos se pasan por el vectorizador
        if isinstance(textos[0], str):
            textos = self.vectorizador.vectorizar(textos)
        if len(textos) == 2:
            return cosine_similarity(textos[None,0], textos[None,1])
        else:
            return cosine_similarity(textos)

    def jaccard(self, textos, vectorizar=False):
        """Calcula la similitud de jaccard entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de similitud. También es posible ingresar directamente \ 
            los vectores pre-calculados de los textos utilizando \ 
            vectorizadores basados en frecuencias (BOW, TF-IDF, Hashing).
        :param vectorizar: (bool) {True, False} valor por defecto: False. \ 
            Si el parámetro *textos* corresponde a una lista de textos, \ 
            el parámentro vectorizar debe ser True, de lo contrario False.
        :return: array con el valor de similitud entre textos. valor entre  \ 
            0 y 1, donde 1 representa que los textos son iguales.
        """
        n_textos = len(textos)
        if isinstance(textos, str) or n_textos < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        elif n_textos == 2:
            if isinstance(textos[0], str):
                if vectorizar:
                    textos = self.vectorizador.vectorizar(textos)
                    return 1 - pairwise_distances(textos[None,0], textos[None,1], metric='jaccard')
                else:
                    return jaccard_textos(textos[0], textos[1])
            else:
                return 1 - pairwise_distances(textos[None,0], textos[None,1], metric='jaccard')
        else:
            if isinstance(textos[0], str):
                if vectorizar:
                    vectores = self.vectorizador.vectorizar(textos)
                    similitudes = 1 - pairwise_distances(vectores, metric='jaccard')
                else:
                    similitudes = np.zeros((n_textos, n_textos))
                    for i in range(n_textos):
                        for j in range(i, n_textos):
                            similitudes[i, j] = jaccard_textos(textos[i], textos[j])
                    # Para que la matriz de similitudes quede simétrica
                    similitudes += similitudes.T - np.diag(np.diag(similitudes))
            else:
                similitudes = 1 - pairwise_distances(textos, metric='jaccard')
        return similitudes
        
### Clase Distancia ----------------------------------------------------

class Distancia():
    def __init__(self, vectorizador=None, lenguaje='es'):
        """Constructor de la clase Distacia. \ 
            Permite calcular la diferentes tipos de distancias entre textos.

        :param vectorizador: objeto tipo vectorizador. \ 
            Valor por defecto: None. \ 
            Carga y establece el vectorizador del objeto Distancia. \ 
            Si no se especifica un \ 
            vectorizador se utilizará uno de tipo Word2Vec. Si se pasa un \ 
            vectorizador al objeto de Distancia, este ya debe estar ajustado.
        :param lenguaje: (str) {'es', 'en', 'de', 'fr'}. \ 
            valor por defecto: 'es'. Indica el lenguaje que utilizará el \ 
            vectorizador, soporta los lenguajes Español(es), Inglés(en), \ 
            Alemán(de) y Francés(fr).
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)
        
    def establecer_lenguaje(self, lenguaje):
        """Establece el lenguaje del objeto Distancia.

        :param lenguaje: (str) {'es', 'en', 'de', 'fr'}. \ 
            Valor por defecto: 'es'. Indica el lenguaje que utilizará el \ 
            vectorizador, soporta los lenguajes Español(es), Inglés(en), \ 
            Alemán(de) y Francés(fr).
        """        
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):
        """Establece el vectorizador del objeto Distancia.

        :param vectorizador: objeto tipo vectorizador. Carga y establece el \ 
            vectorizador del objeto Distancia. Si no se especifica un \ 
            vectorizador se utilizará uno de tipo Word2Vec. Si se pasa un \ 
            vectorizador al objeto de Distancia, este ya debe estar ajustado.
        """
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def distancia_pares(self, textos, tipo_distancia, **kwds):
        """Permite calcular diferentes tipos de distancias entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia.
        :param tipo_distancia: (str) {'l1', 'l2', 'minkowski', 'jaccard', \ 
            'hamming', 'chebyshev', 'rogerstanimoto', 'braycurtis'}. \ 
            Hace referencia al tipo de distancia a calcular.
        :param kwds: otros parámetros opcionales.
        :return: array con el valor de distancia entre textos.
        """
        # Para tipo_distancia se puede utilizar cualquiera de las soportadas acá:
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
        if isinstance(textos, str) or len(textos) < 2:
            print ('Debe ingresar una lista de por lo menos dos textos o vectores para hacer la comparación.')
            return None
        # Si se ingresan textos, estos se pasan por el vectorizador
        if isinstance(textos[0], str):
            textos = self.vectorizador.vectorizar(textos)
        if len(textos) == 2:
            return pairwise_distances(textos[None,0], textos[None,1], metric=tipo_distancia, **kwds)
        else:
            return pairwise_distances(textos, metric=tipo_distancia, **kwds)

    def l1(self, textos):
        """Calcula la distancia L1 entre textos. También conocida como la \ 
        la distancia Manhattan.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia.
        :return: array con el valor de distancia entre textos.
        """
        return self.distancia_pares(textos, tipo_distancia='l1')   

    def l2(self, textos):        
        """Calcula la distancia L2 entre textos. También conocida como la \ 
        la distancia Euclidiana.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia
        :return: array con el valor de distancia entre textos.
        """
        return self.distancia_pares(textos, tipo_distancia='l2')
    
    def minkowski(self, textos, p):
        """Calcula la distancia minkowski entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia.
        :param p: (int) orden con el que se calcula la distancia.  \ 
            Cuando p=1 es equivalente a la distancia de Manhattan  \ 
            y cuando p=2 es equivalente a la distancia euclidiana.
        :return: array con el valor de distancia entre textos.
        """
        if p == 1:
            return self.distancia_pares(textos, tipo_distancia='l1')
        elif p == 2:
            return self.distancia_pares(textos, tipo_distancia='l2')
        else:
            return self.distancia_pares(textos, tipo_distancia='minkowski', p=p)

    def jaccard(self, textos):
        """Calcula la distancia jaccard entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia
        :return: array con el valor de distancia entre textos.
        """
        return self.distancia_pares(textos, tipo_distancia='jaccard')

    def hamming(self, textos):
        """Calcula la distancia hamming entre textos.

        :param textos: (list) lista de textos (str) de interés para el \ 
            cálculo de distancia
        :return: array con el valor de distancia entre textos.
        """
        return self.distancia_pares(textos, tipo_distancia='hamming')

### Clase DiferenciaStrings ----------------------------------------------------

class DiferenciaStrings():
    """ Esta clase se recomienda para comparaciones de strings \ 
        relativamente cortos, como nombres, direcciones y otras cadenas \ 
        de caracteres similares. Para textos más extensos, se recomiendan las \ 
        clases :py:meth:`comparacion.Similitud` o \ 
        :py:meth:`comparacion.Distancia`
    """
    def comparacion_pares(self, texto1, texto2, tipo='levenshtein', norm=None):
        """ Permite hacer comparaciones entre dos textos.

        :param texto1: (str) primer texto de interés a comparar.
        :param texto2: (str) segundo texto de interés a comparar.
        :param tipo: (str) {'damerau_levenshtein', 'levenshtein', 'hamming', \ 
            'jaro_winkler', 'jaro'} valor por defecto: 'levenshtein'. \ 
            Criterio de comparación a utilizar entre los textos.
        :param norm: (int) {1, 2} valor por defecto: None. Permite normalizar \ 
            los resultados en función de la longitud de los textos. \ 
            Si norm=1 se normaliza en función al texto más corto, \ 
            si nomr=2 se normaliza en función al texto de mayor extensión.
        :return: valor (float) o (int) resultado de la comparación.
        """
        tipo = tipo.lower()
        if 'damerau' in tipo:
            salida = jellyfish.damerau_levenshtein_distance(texto1, texto2)
        elif 'levenshtein' in tipo:
            salida = jellyfish.levenshtein_distance(texto1, texto2)
        elif 'hamming' in tipo:
            salida = jellyfish.hamming_distance(texto1, texto2)
        elif 'winkler' in tipo:
            salida = jellyfish.jaro_winkler_similarity(texto1, texto2)
        elif 'jaro' in tipo:
            salida = jellyfish.jaro_similarity(texto1, texto2)
        else:
            print('Por favor seleccione un criterio válido para comparar los strings.')
            return None
        if norm in [1, 2] and 'jaro' not in tipo:
            if norm == 1:
                salida /= min(len(texto1), len(texto2))
            else:
                salida /= max(len(texto1), len(texto2))
        return salida

    def comparacion_lista(self, textos, tipo='levenshtein', norm=None):
        """ Permite hacer comparaciones entre una lista de textos.

        :param textos: (list) lista de textos (str) de interés para realizar \ 
            la comparación.
        :param tipo: (str) {'damerau', 'levenshtein', 'hamming', 'winkler', \ 
            'jaro'} valor por defecto: 'levenshtein'. Criterio de comparación \ 
            a utilizar entre los textos.
        :param norm: (int) {1, 2} valor por defecto: None. Permite normalizar \ 
            los resultados en función de la longitud de los textos. \ 
            Si norm=1 se normaliza en función al texto más corto, \ 
            si norm=2 se normaliza en función al texto de mayor extensión.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        n_textos = len(textos)
        if isinstance(textos, str) or n_textos < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        elif n_textos == 2:
            salida = self.comparacion_pares(textos[0], textos[1], tipo, norm)
            return np.array([[salida]])
        else:
            diferencias = np.zeros((n_textos, n_textos))
            for i in range(n_textos):
                for j in range(i, n_textos):
                    diferencias[i, j] = self.comparacion_pares(textos[i], textos[j], tipo, norm)

            # Para que la matriz quede simétrica
            diferencias += diferencias.T - np.diag(np.diag(diferencias))
            return diferencias

    def distancia_levenshtein(self, textos, norm=None):
        """ Permite calcular la distancia levenshtein entre textos.

        :param textos: (list) lista de textos (str) de interés para realizar \ 
            el cálculo de distancia.
        :param norm: (int) {1, 2} valor por defecto: None. Permite normalizar \ 
            los resultados en función de la longitud de los textos. \ 
            Si norm=1 se normaliza en función al texto más corto, \ 
            si nomr=2 se normaliza en función al texto de mayor extensión.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        return self.comparacion_lista(textos, 'levenshtein', norm)

    def distancia_damerau_levenshtein(self, textos, norm=None):
        """ Permite calcular la distancia damerau levenshtein entre textos.

        :param textos: (list) lista de textos (str) de interés para realizar \ 
            el cálculo de distancia.
        :param norm: (int) {1, 2} valor por defecto: None. Permite normalizar \ 
            los resultados en función de la longitud de los textos. \ 
            Si norm=1 se normaliza en función al texto más corto, \ 
            si nomr=2 se normaliza en función al texto de mayor extensión.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        return self.comparacion_lista(textos, 'damerau_levenshtein', norm)        

    def distancia_hamming(self, textos, norm=None):
        """ Permite calcular la distancia hamming entre textos.

        :param textos: (list) lista de textos (str) de interés para realizar \ 
            el cálculo de distancia.
        :param norm: (int) {1, 2} valor por defecto: None. Permite normalizar \ 
            los resultados en función de la longitud de los textos. \ 
            Si norm=1 se normaliza en función al texto más corto, \ 
            si nomr=2 se normaliza en función al texto de mayor extensión.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        return self.comparacion_lista(textos, 'hamming', norm)

    def similitud_jaro(self, textos):
        """ Permite calcular la similitiud jaro entre textos.

        :param textos: (list) lista de textos (str) de interés para realizar \ 
            el cálculo de similitud.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        return self.comparacion_lista(textos, 'jaro')

    def similitud_jaro_winkler(self, textos):
        """ Permite calcular la similitiud jaro entre textos.
        
        :param textos: (list) lista de textos (str) de interés para realizar \ 
            el cálculo de similitud.
        :return: array con el valor resultante de la comparación entre los \ 
            textos.
        """
        return self.comparacion_lista(textos, 'jaro_winkler')
