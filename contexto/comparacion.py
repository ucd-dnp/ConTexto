import jellyfish
import numpy as np
from scipy.sparse import issparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from lenguajes import definir_lenguaje
from vectorizacion import VectorizadorWord2Vec
from utils.auxiliares import cargar_objeto

# Para que no se muestre la warning de "DataConversionWarning"
import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action="ignore", category=DataConversionWarning)


# Clase Similitud ----------------------------------------------------


class Similitud:
    def __init__(self, vectorizador=None, lenguaje="es"):
        """
        Constructor de la clase Similitud. Permite calcular la similitud cose\
        no y de Jaccard entre textos y/o vectores.

        :param vectorizador: Valor por defecto: None. Objeto de tipo vectoriz\
            ador, o *string* con la ubicación del archivo que lo contiene. Ve\
            ctorizador que va a ser utilizado para generar representaciones v\
            ectoriales de los textos. Si no se especifica un vectorizador, se\
             utilizará uno de tipo Word2Vec. Si se pasa un vectorizador al ob\
            jeto de clase Similitud, este ya debe estar ajustado.
        :param lenguaje: (str) Valor por defecto: 'es'. Indica el lenguaje qu\
            e utilizará el vectorizador. Para mayor información, consultar la\
             sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se\
             pasa un vectorizador ya ajustado, este parámetro no será utiliza\
            do.
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)

    # Función auxiliar
    def __jaccard_textos(self, texto1, texto2):
        if type(texto1) == str:
            texto1 = texto1.split()
        if type(texto2) == str:
            texto2 = texto2.split()
        interseccion = set(texto1).intersection(set(texto2))
        union = set(texto1).union(set(texto2))
        return np.array([[len(interseccion) / len(union)]])

    def establecer_lenguaje(self, lenguaje):
        """
        Establece el lenguaje del objeto Similitud.

        :param lenguaje: (str) Indica el lenguaje que utilizará el vectorizad\
            or. Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se\
             pasa un vectorizado ajustado, este parámetro no será usado.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):
        """
        Establece el vectorizador del objeto Similitud.

        :param vectorizador: Objeto de tipo vectorizador, o *string* con la u\
            bicación del archivo que lo contiene. Vectorizador que va a ser u\
            tilizado para generar representaciones vectoriales de los textos.\
             Si se pasa un vectorizador al objeto de clase Similitud, este ya\
             debe estar ajustado.
        """
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def coseno(self, lista1, lista2=[]):
        """
        Calcula la similitud coseno entre uno o dos grupos de textos o vector\
        es de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de similitud. También es posible ingresar directamente \
            los vectores pre-calculados de los textos en un arreglo de numpy \
            o una matriz dispersa.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calculará la similitud entre cada uno de l\
            os textos de lista1 con cada uno de los textos de lista2. También\
             es posible ingresar directamente los vectores pre-calculados de \
            los textos en un arreglo de numpy o una matriz dispersa.
        :return: (numpy array) Matriz de dos dimensiones con las similitudes \
            coseno entre los textos/vectores de entrada. Sí solo se utilizó e\
            l parámetro lista1 con *n* textos/vectores, devolverá una matriz \
            de *nxn* simétrica, con las similitudes coseno entre todos los el\
            ementos de lista1. Si se utilizan los parámetros lista1 y lista2 \
            con *n1* y *n2* textos respectivamente, devolverá una matriz de \
            *n1xn2*, con las similitudes coseno entre los textos/vectores de \
            lista1 y los elementos de lista2.
        """
        if isinstance(lista1, str):
            lista1 = [lista1]
        if isinstance(lista2, str):
            lista2 = [lista2]
        # Cantidad de elementos en lista2
        n2 = len(lista2) if not issparse(lista2) else lista2.shape[0]
        # Si se ingresan textos, estos se pasan por el vectorizador
        if isinstance(lista1[0], str):
            try:
                lista1 = self.vectorizador.vectorizar(lista1, disperso=True)
            except Exception:
                lista1 = self.vectorizador.vectorizar(lista1)
        if n2 > 0 and isinstance(lista2[0], str):
            try:
                lista2 = self.vectorizador.vectorizar(lista2, disperso=True)
            except Exception:
                lista2 = self.vectorizador.vectorizar(lista2)
        if n2 < 1:
            return cosine_similarity(lista1)
        else:
            return cosine_similarity(lista1, lista2)

    def jaccard(self, lista1, lista2=[], vectorizar=False):
        """
        Calcula la similitud de Jaccard entre uno o dos grupos de textos o \
        vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de similitud. También es posible ingresar directamente \
            los vectores pre-calculados de los textos en un arreglo de numpy,\
             utilizando vectorizadores basados en frecuencias (BOW, TF-IDF, \
            Hashing).
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calculará la similitud entre cada uno de l\
            os textos de lista1 con cada uno de los textos de lista2. También\
             es posible ingresar directamente los vectores pre-calculados de \
            los textos en un arreglo de numpy, utilizando vectorizadores basa\
            dos en frecuencias (BOW, TF-IDF, Hashing).
        :param vectorizar: (bool) {True, False} Valor por defecto: False. Par\
            ámetro opcional que indica si se desean vectorizar los textos de \
            entrada pertenecientes a lista1 y (opcionalmente) a lista2. Si ve\
            ctorizar=False, se calculará la similitud de Jaccard de cada par \
            de textos directamente, sin obtener sus representaciones vectoria\
            les.
        :return: (numpy array) Matriz de dos dimensiones con las similitudes \
            de Jaccard entre los textos/vectores de entrada. Sí solo se utili\
            zó el parámetro lista1 con *n* textos/vectores, devolverá una ma\
            triz de *nxn* simétrica, con las similitudes de Jaccard entre to\
            dos los elementos de lista1. Si se utilizan los   parámetros lis\
            ta1 y lista2 con *n1* y *n2* textos respectivamente, devolverá u\
            na matriz de *n1xn2*, con las similitudes de Jaccard entre los e\
            lementos de lista1 y los elementos de lista2.
        """
        if isinstance(lista1, str):
            lista1 = [lista1]
        if isinstance(lista2, str):
            lista2 = [lista2]
        # Esta función no acepta matrices dispersas, por lo que
        # se pasan a numpy array
        if issparse(lista1):
            lista1 = lista1.toarray()
        if issparse(lista2):
            lista2 = lista2.toarray()
        # Cantidad de elementos en cada lista
        n1, n2 = len(lista1), len(lista2)
        # Si se indicó, se calculan los vectores de las listas
        # de textos de entrada
        if vectorizar:
            if isinstance(lista1[0], str):
                lista1 = self.vectorizador.vectorizar(lista1)
            if n2 > 0 and isinstance(lista2[0], str):
                lista2 = self.vectorizador.vectorizar(lista2)
        if n2 < 1:
            if isinstance(lista1[0], str):
                similitudes = np.zeros((n1, n1))
                for i in range(n1):
                    for j in range(i, n1):
                        similitudes[i, j] = self.__jaccard_textos(
                            lista1[i], lista1[j]
                        )
                # Para que la matriz de similitudes quede simétrica
                similitudes += similitudes.T - np.diag(np.diag(similitudes))
            else:
                similitudes = 1 - pairwise_distances(lista1, metric="jaccard")
        else:
            if isinstance(lista1[0], str) and isinstance(lista2[0], str):
                similitudes = np.zeros((n1, n2))
                for i in range(n1):
                    for j in range(n2):
                        similitudes[i, j] = self.__jaccard_textos(
                            lista1[i], lista2[j]
                        )
            else:
                similitudes = 1 - pairwise_distances(
                    lista1, lista2, metric="jaccard"
                )
        # Devolver matriz de similitudes
        return similitudes


# Clase Distancia ----------------------------------------------------


class Distancia:
    def __init__(self, vectorizador=None, lenguaje="es"):
        """
        Constructor de la clase Distacia.
        Permite calcular la diferentes medidas de distancia entre textos y/o \
        vectores.

        :param vectorizador: Valor por defecto: None. Objeto de tipo vectori\
            zador, o *string* con la ubicación del archivo que lo contiene. \
            Vectorizador que va a ser utilizado para generar representaciones\
             vectoriales de los textos. Si no se especifica un vectorizador, \
            se utilizará uno de tipo Word2Vec. Si se pasa un vectorizador al \
            objeto de clase Distancia, este ya debe estar ajustado.
        :param lenguaje: (str) Valor por defecto: 'es'. Indica el lenguaje \
            que utilizará el vectorizador. Para mayor información, consultar \
            la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se\
             pasa un vectorizador ya ajustado, este parámetro no será utiliza\
            do.
        """
        # Definir lenguaje del vectorizador y vectorizador a utilizar
        self.establecer_lenguaje(lenguaje)
        self.establecer_vectorizador(vectorizador)
        # Distancias de sklearn que aceptan matrices dispersas
        self.aceptan_dispersas = [
            "cityblock",
            "cosine",
            "euclidean",
            "l1",
            "l2",
            "manhattan",
        ]

    def establecer_lenguaje(self, lenguaje):
        """
        Establece el lenguaje del objeto Distancia.

        :param lenguaje: (str) Indica el lenguaje que utilizará el vectorizad\
            or. Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se\
             pasa un vectorizador ya ajustado, este parámetro no será utiliza\
            do.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):
        """
        Establece el vectorizador del objeto Distancia.

        :param vectorizador: Objeto de tipo vectorizador, o *string* con la u\
            bicación del archivo que lo contiene. Vectorizador que va a ser u\
            tilizado para generar representaciones vectoriales de los textos.\
             Si no se especifica un vectorizador, se utilizará uno de tipo Wo\
            rd2Vec. Si se pasa un vectorizador al objeto de clase Distancia, \
            este ya debe estar ajustado.
        """
        # Definir modelo para vectorizar
        if vectorizador is None:
            # vectorizador por defecto
            self.vectorizador = VectorizadorWord2Vec(self.lenguaje)
        elif isinstance(vectorizador, str):
            self.vectorizador = cargar_objeto(vectorizador)
        else:
            self.vectorizador = vectorizador

    def distancia_pares(
        self, lista1, lista2=[], tipo_distancia="l2", **kwargs
    ):
        """
        Permite calcular diferentes métricas de distancias entre uno o dos gr\
        upos de textos y/o vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de las distancias. También es posible ingresar directam\
            ente los vectores pre-calculados de los textos en un arreglo de n\
            umpy o una matriz dispersa.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calculará la distancia entre cada uno de l\
            os textos/vectores de lista1 con cada uno de los elementos de lis\
            ta2. También es posible ingresar directamente los vectores pre-ca\
            lculados de los textos en un arreglo de numpy o una matriz disper\
            sa.
        :param tipo_distancia: (str) Valor por defecto: 'l2'. Métrica de dist\
            ancia que se desea calcular.Para una lista de todas las distancia\
            s que se pueden calcular por medio de esta función, se puede cons\
            ultar la documentación de scikit-learn y scipy: \
            https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
        :param kwargs: Parámetros opcionales que pueden ser ajustables, depen\
            diendo de la métrica de distancia elegida.
        :return: (numpy array) Matriz de dos dimensiones con las distancias c\
            alculadas entre los textos/vectores de entrada. Sí solo se utiliz\
            ó el parámetro lista1 con *n* textos/vectores, devolverá una matr\
            iz de *nxn* simétrica, con las distancias entre todos los element\
            os de lista1. Si se utilizan los parámetros lista1 y lista2 con \
            *n1* y *n2* textos/vectores respectivamente, devolverá una matriz\
             de *n1xn2*, con las distancias entre los elementos de lista1 y l\
            os elementos de lista2.
        """
        if isinstance(lista1, str):
            lista1 = [lista1]
        if isinstance(lista2, str):
            lista2 = [lista2]
        # Cantidad de elementos en lista2
        n2 = len(lista2) if not issparse(lista2) else lista2.shape[0]
        # Si se ingresan textos, estos se pasan por el vectorizador
        if isinstance(lista1[0], str):
            try:
                lista1 = self.vectorizador.vectorizar(lista1, disperso=True)
            except Exception:
                lista1 = self.vectorizador.vectorizar(lista1)
        if n2 > 0 and isinstance(lista2[0], str):
            try:
                lista2 = self.vectorizador.vectorizar(lista2, disperso=True)
            except Exception:
                lista2 = self.vectorizador.vectorizar(lista2)
        # Si la distancia a calcular no soporta matrices dispersas,
        # se asegura de que no hayan
        if tipo_distancia not in self.aceptan_dispersas:
            if issparse(lista1):
                lista1 = lista1.toarray()
            if issparse(lista2):
                lista2 = lista2.toarray()
        if n2 < 1:
            return pairwise_distances(lista1, metric=tipo_distancia, **kwargs)
        else:
            return pairwise_distances(
                lista1, lista2, metric=tipo_distancia, **kwargs
            )

    def l1(self, lista1, lista2=[]):
        """
        Calcula la distancia L1, también conocida como la distancia Manhattan\
        , entre uno o dos grupos de textos y/o vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
        l cálculo de las distancias. También es posible ingresar directamente\
         los vectores pre-calculados de los textos en un arreglo de numpy o u\
        na matriz dispersa.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calcularán la distancias entre cada uno de\
             los textos/vectores de lista1 con cada uno de los elementos de l\
            ista2. También es posible ingresar directamente los vectores pre-\
            calculados de los textos en un arreglo de numpy o una matriz disp\
            ersa.
        :return: (numpy array) Matriz de dos dimensiones con las distancias L\
            1 calculadas entre los textos/vectores de entrada. Sí solo se uti\
            lizó el parámetro lista1 con *n* textos/vectores, devolverá una m\
            atriz de *nxn* simétrica, con las distancias L1 entre todos los e\
            lementos de lista1. Si se utilizan los parámetros lista1 y lista2\
             con *n1* y *n2* textos/vectores respectivamente, devolverá una m\
            atriz de *n1xn2*, con las distancias entre los elementos de lista\
            1 y los elementos de lista2.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="l1")

    def l2(self, lista1, lista2=[]):
        """
        Calcula la distancia L2, también conocida como la distancia euclidian\
        a, entre uno o dos grupos de textos y/o vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de las distancias. También es posible ingresar directam\
            ente los vectores pre-calculados de los textos en un arreglo de n\
            umpy o una matriz dispersa.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calcularán la distancias entre cada uno de\
             los textos/vectores de lista1 con cada uno de los textos de list\
            a2. También es posible ingresar directamente los vectores pre-cal\
            culados de los textos en un arreglo de numpy o una matriz dispersa
        :return: (numpy array) Matriz de dos dimensiones con las distancias L\
            2 calculadas entre los textos/vectores de entrada. Sí solo se uti\
            lizó el parámetro lista1 con *n* textos/vectores, devolverá una m\
            atriz de *nxn* simétrica, con las distancias L2 entre todos los e\
            lementos de lista1. Si se utilizan los parámetros lista1 y lista2\
             con *n1* y *n2* textos/vectores respectivamente, devolverá una m\
            atriz de *n1xn2*, con las distancias entre los elementos de lista\
            1 y los elementos de lista2.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="l2")

    def minkowski(self, lista1, lista2=[], p=2):
        """
        Calcula la distancia de Minkowski entre uno o dos grupos de textos y/\
        o vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de las distancias. También es posible ingresar directam\
            ente los vectores pre-calculados de los textos. También es posibl\
            e ingresar directamente los vectores pre-calculados de los textos\
             en un arreglo de numpy o una matriz dispersa.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calcularán la distancias entre cada uno de\
             los textos/vectores de lista1 con cada uno de los textos de list\
            a2. También es posible ingresar directamente los vectores pre-cal\
            culados de los textos en un arreglo de numpy o una matriz dispersa
        :param p: (int) Valor por defecto: 2. Orden o grado de la distancia d\
            e Minkowski que se desea calcular. Si p=1, la distancia calculada\
             es equivalente a la distancia de Manhattan (L1) y cuando p=2 la \
            distancia calculada es equivalente a la distancia euclidiana (L2).
        :return: (numpy array) Matriz de dos dimensiones con las distancias c\
            alculadas entre los textos/vectores de entrada. Sí solo se utiliz\
            ó el parámetro lista1 con *n* textos/vectores, devolverá una matr\
            iz de *nxn* simétrica, con las distancias entre todos los element\
            os de lista1. Si se utilizan los parámetros lista1 y lista2 con \
            *n1* y *n2* textos/vectores respectivamente, devolverá una matriz\
             de *n1xn2*, con las distancias entre los elementos de lista1 y l\
            os elementos de lista2.
        """
        if p == 1:
            return self.distancia_pares(lista1, lista2, tipo_distancia="l1")
        elif p == 2:
            return self.distancia_pares(lista1, lista2, tipo_distancia="l2")
        else:
            return self.distancia_pares(
                lista1, lista2, tipo_distancia="minkowski", p=p
            )

    def jaccard(self, lista1, lista2=[]):
        """
        Calcula la distancia de Jaccard entre uno o dos grupos de textos y/o \
        vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de las distancias. También es posible ingresar directam\
            ente los vectores pre-calculados de los textos.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se calcularán la distancias entre cada uno de\
             los textos/vectores de lista1 con cada uno de los textos de list\
            a2. También es posible ingresar directamente los vectores pre-cal\
            culados de los textos.
        :return: (numpy array) Matriz de dos dimensiones con las distancias c\
            alculadas entre los textos/vectores de entrada. Sí solo se utiliz\
            ó el parámetro lista1 con *n* textos, devolverá una matriz de \
            *nxn* simétrica, con las distancias entre todos los elementos de \
            lista1. Si se utilizan los parámetros lista1 y lista2 con *n1* y \
            *n2* textos/vectores respectivamente, devolverá una matriz de \
            *n1xn2*, con las distancias entre los elementos de lista1 y los e\
            lementos de lista2.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="jaccard")

    def hamming(self, lista1, lista2=[]):
        """
        Calcula la distancia de Hamming entre uno o dos grupos de textos y/o \
        vectores de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para e\
            l cálculo de las distancias. También es posible ingresar directam\
            ente los vectores pre-calculados de los textos.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
         con un segundo texto o lista de textos para comparar. Si se utiliza \
        este parámetro, se calcularán la distancias entre cada uno de los tex\
        tos/vectores de lista1 con cada uno de los textos de lista2. También \
        es posible ingresar directamente los vectores pre-calculados de los t\
        extos.
        :return: (numpy array) Matriz de dos dimensiones con las distancias c\
            alculadas entre los textos/vectores de entrada. Sí solo se utiliz\
            ó el parámetro lista1 con *n* textos/vectores, devolverá una matr\
            iz de *nxn* simétrica, con las distancias entre todos los element\
            os de lista1. Si se utilizan los parámetros lista1 y lista2 con \
            *n1* y *n2* textos/vectores respectivamente, devolverá una matriz\
             de *n1xn2*, con las distancias entre los elementos de lista1 y l\
            os elementos de lista2.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="hamming")


# Clase DiferenciaStrings ----------------------------------------------------


class DiferenciaStrings:
    """
    Esta clase se recomienda para comparaciones de strings relativamente cort\
    os, como nombres, direcciones y otras cadenas de caracteres similares. Pa\
    ra textos más extensos, se recomiendan las clases \
    :py:meth:`comparacion.Similitud` o :py:meth:`comparacion.Distancia`.
    """

    def comparacion_pares(self, texto1, texto2, tipo="levenshtein", norm=None):
        """
        Permite hacer comparaciones entre dos textos de entrada, de acuerdo a\
         un tipo de distancia o similitud determinado.

        :param texto1: (str) Primer texto de interés a comparar.
        :param texto2: (str) Segundo texto de interés a comparar.
        :param tipo: (str) {'damerau_levenshtein', 'levenshtein', 'hamming', \
            'jaro_winkler', 'jaro'} Valor por defecto: 'levenshtein'. Criteri\
            o de comparación a utilizar entre los textos.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm=\
            1 se normaliza en función al texto más corto, si norm=2 se normal\
            iza en función al texto de mayor extensión.
        :return: (float o int) Valor resultado de la comparación.
        """
        tipo = tipo.lower()
        if "damerau" in tipo:
            salida = jellyfish.damerau_levenshtein_distance(texto1, texto2)
        elif "levenshtein" in tipo:
            salida = jellyfish.levenshtein_distance(texto1, texto2)
        elif "hamming" in tipo:
            salida = jellyfish.hamming_distance(texto1, texto2)
        elif "winkler" in tipo:
            salida = jellyfish.jaro_winkler_similarity(texto1, texto2)
        elif "jaro" in tipo:
            salida = jellyfish.jaro_similarity(texto1, texto2)
        else:
            print(
                (
                    "Por favor seleccione un criterio válido "
                    "para comparar los strings."
                )
            )
            return None
        if norm in [1, 2] and "jaro" not in tipo:
            if norm == 1:
                salida /= min(len(texto1), len(texto2))
            else:
                salida /= max(len(texto1), len(texto2))
        return salida

    def comparacion_lista(
        self, lista1, lista2=[], tipo="levenshtein", norm=None
    ):
        """
        Permite hacer comparaciones entre una o dos listas de textos de entra\
        da.

        :param lista1: (str o list) Texto o lista de textos de interés para r\
            ealizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param tipo: (str) {'damerau_levenshtein', 'levenshtein', 'hamming', \
            'jaro_winkler', 'jaro'} Valor por defecto: 'levenshtein'. Criteri\
            o de comparación a utilizar entre los textos.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm=\
            1 se normaliza en función al texto más corto, si norm=2 se normal\
            iza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con los valores de c\
            omparación (similitud o distancia) calculados entre los textos de\
             entrada. Sí solo se utilizó el parámetro lista1 con *n* textos, \
            devolverá una matriz de *nxn* simétrica, con las comparaciones en\
            tre todos los elementos de lista1. Si se utilizan los parámetros \
            lista1 y lista2 con *n1* y *n2* textos respectivamente, devolverá\
             una matriz de *n1xn2*, con las comparaciones entre los elementos\
             de lista1 y los elementos de lista2.
        """
        if isinstance(lista1, str):
            lista1 = [lista1]
        if isinstance(lista2, str):
            lista2 = [lista2]
        n1, n2 = len(lista1), len(lista2)
        if n2 < 1:
            diferencias = np.zeros((n1, n1))
            for i in range(n1):
                for j in range(i, n1):
                    diferencias[i, j] = self.comparacion_pares(
                        lista1[i], lista1[j], tipo, norm
                    )
            # Para que la matriz quede simétrica
            diferencias += diferencias.T - np.diag(np.diag(diferencias))
        else:
            diferencias = np.zeros((n1, n2))
            for i in range(n1):
                for j in range(n2):
                    diferencias[i, j] = self.comparacion_pares(
                        lista1[i], lista2[j], tipo, norm
                    )
        return diferencias

    def distancia_levenshtein(self, lista1, lista2=[], norm=None):
        """
        Permite calcular la distancia de Levenshtein entre una o dos listas d\
        e textos de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para r\
            ealizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm \
            = 1 se normaliza en función al texto más corto, si norm = 2 se no\
            rmaliza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con las distancias e\
            ntre los textos de entrada. Sí solo se utilizó el parámetro lista\
            1 con *n* textos, devolverá una matriz de *nxn* simétrica, con la\
            s distancias entre todos los elementos de lista1. Si se utilizan \
            los parámetros lista1 y lista2 con *n1* y *n2* textos respectivam\
            ente, devolverá una matriz de *n1xn2*, con las distancias entre \
            los elementos de lista1 y los elementos de lista2.
        """
        return self.comparacion_lista(lista1, lista2, "levenshtein", norm)

    def distancia_damerau_levenshtein(self, lista1, lista2=[], norm=None):
        """
        Permite calcular la distancia de Damerau-Levenshtein entre una o dos \
        listas de textos de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para r\
            ealizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm \
            = 1 se normaliza en función al texto más corto, si norm = 2 se no\
            rmaliza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con las distancias e\
            ntre los textos de entrada. Sí solo se utilizó el parámetro lista\
            1 con *n* textos, devolverá una matriz de *nxn* simétrica, con la\
            s distancias entre todos los elementos de lista1. Si se utilizan \
            los parámetros lista1 y lista2 con *n1* y *n2* textos respectivam\
            ente, devolverá una matriz de *n1xn2*, con las distancias entre l\
            os elementos de lista1 y los elementos de lista2.
        """
        return self.comparacion_lista(
            lista1, lista2, "damerau_levenshtein", norm
        )

    def distancia_hamming(self, lista1, lista2=[], norm=None):
        """
        Permite calcular la distancia de Hamming entre una o dos listas de te\
        xtos de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para r\
            ealizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm \
            = 1 se normaliza en función al texto más corto. Si norm = 2 se no\
            rmaliza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con las distancias e\
            ntre los textos de entrada. Sí solo se utilizó el parámetro lista\
            1 con *n* textos, devolverá una matriz de *nxn* simétrica, con la\
            s distancias entre todos los elementos de lista1. Si se utilizan \
            los parámetros lista1 y lista2 con *n1* y *n2* textos respectivam\
            ente, devolverá una matriz de *n1xn2*, con las distancias entre l\
            os elementos de lista1 y los elementos de lista2.
        """
        return self.comparacion_lista(lista1, lista2, "hamming", norm)

    def similitud_jaro(self, lista1, lista2=[]):
        """
        Permite calcular la similitud de Jaro entre una o dos listas de texto\
        s de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para r\
            ealizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm \
            = 1 se normaliza en función al texto más corto, si norm=2 se norm\
            aliza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con las similitudes \
            entre los textos de entrada. Sí solo se utilizó el parámetro list\
            a1 con *n* textos, devolverá una matriz de *nxn* simétrica, con l\
            as similitudes entre todos los elementos de lista1. Si se utiliza\
            n los parámetros lista1 y lista2 con *n1* y *n2* textos respectiv\
            amente, devolverá una matriz de *n1xn2*, con las similitudes entr\
            e los elementos de lista1 y los elementos de lista2.
        """
        return self.comparacion_lista(lista1, lista2, "jaro")

    def similitud_jaro_winkler(self, lista1, lista2=[]):
        """
        Permite calcular la similitud de Jaro-Winkler entre una o dos listas \
        de textos de entrada.

        :param lista1: (str o list) Texto o lista de textos de interés para \
            realizar las comparaciones.
        :param lista2: (str o list) Valor por defecto: []. Parámetro opcional\
             con un segundo texto o lista de textos para comparar. Si se util\
            iza este parámetro, se harán las comparaciones entre cada uno de \
            los textos de lista1 con cada uno de los textos de lista2.
        :param norm: (int) {1, 2} Valor por defecto: None. Permite normalizar\
             los resultados en función de la longitud de los textos. Si norm \
            = 1 se normaliza en función al texto más corto, si norm = 2 se no\
            rmaliza en función al texto de mayor extensión.
        :return: (numpy array) Matriz de dos dimensiones con las similitudes \
            entre los textos de entrada. Sí solo se utilizó el parámetro list\
            a1 con *n* textos, devolverá una matriz de *nxn* simétrica, con \
            las similitudes entre todos los elementos de lista1. Si se utiliz\
            an los parámetros lista1 y lista2 con *n1* y *n2* textos respecti\
            vamente, devolverá una matriz de *n1xn2*, con las similitudes ent\
            re los elementos de lista1 y los elementos de lista2.
        """
        return self.comparacion_lista(lista1, lista2, "jaro_winkler")
