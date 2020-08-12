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

def jaccard_vectores(vector1, vector2):
    return 1 - pairwise_distances(vector1, vector2, metric='jaccard')


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

    def similitud_coseno(textos, denso=True):
        if isinstance(textos, str) or len(textos) < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        vectores = self.vectorizador.vectorizar(textos)
        if len(vectores) == 2:
            return cosine_similarity(vectores[None,0], vectores[None,1], dense_output=denso)
        else:
            return cosine_similarity(vectores, dense_output=denso)

    def similitud_jaccard(textos, vectorizar=False):
        n_textos = len(textos)
        if isinstance(textos, str) or n_textos < 2:
            print ('Debe ingresar una lista de por lo menos dos textos para hacer la comparación.')
            return None
        if n_textos == 2:
            return jaccard_textos(textos[0], textos[1])
        else:
            similitudes = np.zeros((n_textos, n_textos))
            if vectorizar:
                vectores = self.vectorizador.vectorizar(textos)
                for i in range(n_textos):
                    for j in range(n_textos):
                        similitudes[i, j] = jaccard_vectores(vectores[None,i], vectores[None,j])
            else:
                for i in range(n_textos):
                    for j in range(n_textos):
                        similitudes[i, j] = jaccard_textos(textos[i], textos[j])
        return similitudes
        


def jaccard_vectores(vector1, vector2):


jaccard_similarity('hola este es un texto de prueba', 'es bueno hacer otra prueba')

set('hola este es un texto de prueba'.split())


import numpy as np
a = np.array([1,2,1,4,1]).reshape(1,-1)
b = np.array([1,1,1,3,1]).reshape(1,-1)

c = np.vstack([a,b])
inter = np.min(c, axis=0)
tot = np.max(c, axis=0)
inter/tot


from sklearn.metrics import jaccard_similarity_score
jaccard_similarity_score(a,b)




a = np.array([0,1,1,1,4]).reshape(1,-1)
b = np.array([0,0,1,0.1,2]).reshape(1,-1)







c = cosine_similarity(a)

np.expand_dims(a,0).shape
a.shape

a[None,0,:].shape

c = cosine_similarity(a, b)
c.shape

Anorm = A / np.linalg.norm(A, axis=-1)[:, np.newaxis]
return np.dot(Anorm, Anorm.T)

cos_sim = np.inner(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
vectores_prueba = v_hash.vectorizar(textos_prueba)
vectores_prueba.shape
len(vectores_prueba)