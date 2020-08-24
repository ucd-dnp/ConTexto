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
        """

        :param lenguaje:
        :param modelo:
        :return:
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)
        
    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje:
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):        
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def coseno(self, textos):
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
        """

        :param lenguaje:
        :param modelo:
        :return:
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)
        
    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje:
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):        
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def distancia_pares(self, textos, tipo_distancia, **kwds):
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
        return self.distancia_pares(textos, tipo_distancia='l1')   

    def l2(self, textos):
        return self.distancia_pares(textos, tipo_distancia='l2')
    
    def minkowski(self, textos, p):
        if p == 1:
            return self.distancia_pares(textos, tipo_distancia='l1')
        elif p == 2:
            return self.distancia_pares(textos, tipo_distancia='l2')
        else:
            return self.distancia_pares(textos, tipo_distancia='minkowski', p=p)

    def jaccard(self, textos):
        return self.distancia_pares(textos, tipo_distancia='jaccard')

    def hamming(self, textos):
        return self.distancia_pares(textos, tipo_distancia='hamming')

### Clase DiferenciaStrings ----------------------------------------------------

class DiferenciaStrings():
    def comparacion_pares(self, texto1, texto2, tipo='levenshtein', norm=None):
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
        return self.comparacion_lista(textos, 'levenshtein', norm)

    def distancia_damerau_levenshtein(self, textos, norm=None):
        return self.comparacion_lista(textos, 'damerau_levenshtein', norm)        

    def distancia_hamming(self, textos, norm=None):
        return self.comparacion_lista(textos, 'hamming', norm)

    def similitud_jaro(self, textos):
        return self.comparacion_lista(textos, 'jaro')

    def similitud_jaro_winkler(self, textos):
        return self.comparacion_lista(textos, 'jaro_winkler')
