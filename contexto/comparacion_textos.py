from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from lenguajes import definir_lenguaje
from vectorizacion_texto import VectorizadorWord2Vec
from utils.auxiliares import cargar_objeto

class DistanciaCaracteres():
    def __init__(self):
        pass

class DistanciaFonemas():
    def __init__(self):
        pass

# Función auxiliar
def jaccard_textos(texto1, texto2):
    if type(texto1) == str:
        texto1 = texto1.split()
    if type(texto2) == str:
        texto2 = texto2.split()
    intersection = set(texto1).intersection(set(texto2))
    union = set(texto1).union(set(texto2))
    return np.array([[len(intersection)/len(union)]])

class Similitud():
    def __init__(self, lenguaje='es', vectorizador=None):
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

    def similitud_coseno(self, textos):
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

    def similitud_jaccard(self, textos, vectorizar=False):
        n_textos = len(textos)
        if isinstance(textos, str) or n_textos < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        if n_textos == 2:
            if isinstance(textos[0], str):
                return jaccard_textos(textos[0], textos[1])
            else:
                textos = self.vectorizador.vectorizar(textos)
                return 1 - pairwise_distances(textos[None,0], textos[None,1], metric='jaccard')
        else:
            similitudes = np.zeros((n_textos, n_textos))
            if isinstance(textos[0], str):
                if vectorizar:
                    vectores = self.vectorizador.vectorizar(textos)
                    similitudes = 1 - pairwise_distances(vectores, metric='jaccard')
                else:
                    for i in range(n_textos):
                        for j in range(n_textos):
                            similitudes[i, j] = jaccard_textos(textos[i], textos[j])
            else:
                similitudes = 1 - pairwise_distances(textos, metric='jaccard')
        return similitudes
        
class Distancia():
    def __init__(self, lenguaje='es', vectorizador=None):
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

    def distancia_pares(self, textos, tipo_distancia):
        if isinstance(textos, str) or len(textos) < 2:
                    print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
                    return None
        # Si se ingresan textos, estos se pasan por el vectorizador
        if isinstance(textos[0], str):
            textos = self.vectorizador.vectorizar(textos)
        if len(textos) == 2:
            return pairwise_distances(textos[None,0], textos[None,1], metric=tipo_distancia)
        else:
            return pairwise_distances(textos, metric=tipo_distancia)

    def L1(self, textos):
        if isinstance(textos, str) or len(textos) < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        vectores = self.vectorizador.vectorizar(textos)
        if len(vectores) == 2:
            return pairwise_distances(vectores[None,0], vectores[None,1], dense_output=denso)
        else:
            return pairwise_distances(vectores, dense_output=denso)    

