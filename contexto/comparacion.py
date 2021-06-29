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


# Clase Similitud ---------------------------------------------------


class Similitud:
    def __init__(self, vectorizador=None, lenguaje="es"):
        """
        Constructor de la clase Similitud.\
        Permite calcular la similitud coseno y de Jaccard entre textos \
        y/o vectores.

        :param vectorizador: Objeto de tipo `vectorizador`, o `string` con la \
            ubicación del archivo que lo contiene. Vectorizador que va a ser \
            utilizado para generar representaciones vectoriales de los \
            textos. Si no se especifica un vectorizador, se utilizará uno de \
            tipo `Word2Vec`. Si se pasa un vectorizador al objeto de clase \
            `Similitud`, este ya debe estar ajustado. Valor por defecto `None`
        :type vectorizador: str/None/Vectorizador, opcional
        :param lenguaje: Indica el lenguaje que utilizará el vectorizador. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se \
            pasa un vectorizador ya ajustado, este parámetro no será \
            utilizado. Valor por defecto "es".
        :type lenguaje: str, opcional
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
        Establece el lenguaje del objeto Similitud.\

        :param lenguaje: Indica el lenguaje que utilizará el \
            `vectorizador`. Para mayor información, consultar la \
            sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se \
            pasa un vectorizado ajustado, este parámetro no será usado.
        :type lenguaje: str
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador=None):
        """
        Establece el `vectorizador` del objeto Similitud.\

        :param vectorizador: Objeto de tipo `vectorizador`, o `string` con la \
            ubicación del archivo que lo contiene. Vectorizador que va a ser \
            utilizado para generar representaciones vectoriales de los \
            textos. Si se pasa un vectorizador al objeto de clase Similitud, \
            este ya debe estar ajustado.
        :type vectorizador: vectorizador, opcional
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
        Calcula la similitud coseno entre uno o dos grupos de textos o \
        vectores de entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de similitud. También es posible ingresar directamente \
            los vectores pre-calculados de los textos en un arreglo de numpy \
            o una matriz dispersa.
        :type lista1: list, str
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calculará la similitud entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            También es posible ingresar directamente los vectores \
            pre-calculados de los textos en un arreglo de numpy o una matriz \
            dispersa. Valor por defecto [].
        :type lista2: list, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las similitudes \
            coseno entre los textos/vectores de entrada. Si solo se utilizó \
            el parámetro `lista1` con `n` textos/vectores, devolverá una \
            matriz de `n x n` simétrica, con las similitudes coseno entre \
            todos los elementos de `lista1`. Si se utilizan los parámetros \
            `lista1` y `lista2` con `n_1` y `n_2` textos respectivamente, \
            devolverá una matriz de `n_ 1 x n_2`, con las similitudes coseno \
            entre los textos/vectores de `lista1` y los elementos de `lista2`.
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

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de similitud. También es posible ingresar directamente \
            los vectores pre-calculados de los textos en un arreglo de \
            `numpy`, utilizando vectorizadores basados en frecuencias (`BOW`, \
            `TF-IDF`, `Hashing`).
        :type lista1: list, str
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calculará la similitud entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            También es posible ingresar directamente los vectores \
            pre-calculados de los textos en un arreglo de numpy, utilizando \
            vectorizadores basados en frecuencias (`BOW`, `TF-IDF`, \
            `Hashing`). Valor por defecto `[]`.
        :type lista2: list, str, optional
        :param vectorizar: Indica si se desean vectorizar los textos \
            de entrada pertenecientes a `lista1` y a `lista2.` \
            Si `vectorizar=False`, se calculará la similitud de Jaccard de \
            cada par de textos directamente, sin obtener sus representaciones \
            vectoriales. Valor por defecto `False`.
        :type vectorizar: bool, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las similitudes \
            de Jaccard entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las similitudes de Jaccard \
            entre todos los elementos de `lista1`. Si se utilizan los \
            parámetros `lista1` y `lista2` con `n_1` y `n_2` textos \
            respectivamente, devolverá una matriz de `n_1 x n_2`, con las \
            similitudes de Jaccard entre los elementos de `lista1` y los \
            elementos de `lista2`.
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
        Permite calcular las diferentes medidas de distancia entre textos y/o \
        vectores.

        :param vectorizador:  Objeto de tipo `vectorizador`, o `string` con \
            la ubicación del archivo que lo contiene. Vectorizador que va a \
            ser utilizado para generar representaciones vectoriales de los \
            textos. Si no se especifica un vectorizador, se utilizará uno de \
            tipo `Word2Vec`. Si se pasa un vectorizador al objeto de clase \
            `Distancia`, este ya debe estar ajustado. Valor por defecto \
            `None`.
            :type vectorizador: vectorizador, str, opcional
        :param lenguaje: Indica el lenguaje que utilizará el `vectorizador`. \
            Para mayor información, consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se \
            pasa un vectorizador ya ajustado, este parámetro no será \
            utilizado. Valor por defecto `"es"`.
        :type lenguaje: str
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
        Establece el lenguaje del objeto `Distancia`.

        :param lenguaje: Indica el lenguaje que utilizará el \
            vectorizador. Para mayor información, consultar la \
            sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. Si se \
            pasa un vectorizador ya ajustado, este parámetro no será utilizado.
        :type lenguaje: str
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def establecer_vectorizador(self, vectorizador):
        """
        Establece el `vectorizador` del objeto `Distancia`.

        :param vectorizador: Objeto de tipo vectorizador, o `string` con la \
            ubicación del archivo que lo contiene. Vectorizador que va a ser \
            utilizado para generar representaciones vectoriales de los \
            textos. Si no se especifica un `vectorizador`, se utilizará uno \
            de tipo `Word2Vec`. Si se pasa un `vectorizador` al objeto de \
            clase `Distancia`, este ya debe estar ajustado.
        :type vectorizador: vectorizador, str
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
        Permite calcular diferentes métricas de distancias entre uno o dos \
        grupos de textos y/o vectores de entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: list, str, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calculará la distancia entre cada uno \
            de los textos/vectores de `lista1` con cada uno de los elementos \
            de `lista2`. También es posible ingresar directamente los \
            vectores pre-calculados de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: list, str, numpy.array, opcional
        :param tipo_distancia: Métrica de \
            distancia que se desea calcular.Para una lista de todas las \
            distancias que se pueden calcular por medio de esta función, \
            se puede consultar la documentación de scikit-learn y scipy: \
            https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
            Valor por defecto `l2`.
        :type tipo_distancia: str, opcional
        :param kwargs: Parámetros opcionales que pueden ser ajustables, \
            dependiendo de la métrica de distancia elegida.
        :type kwargs: dict, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y lista2 con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n_1 x n_2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
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
        Calcula la distancia `L1`, también conocida como la distancia \
        Manhattan, entre uno o dos grupos de textos y/o vectores de \
        entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: str, list, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calcularán la distancias entre cada \
            uno de los textos/vectores de `lista1` con cada uno de los \
            elementos de `lista2`. También es posible ingresar directamente \
            los vectores pre-calculaos de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: str, list, numpy.array, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            `L1` calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias `L1` entre \
            todos los elementos de `lista1`. Si se utilizan los parámetros \
            `lista1` y lista2 con `n1` y `n2` textos/vectores \
            respectivamente, devolverá una matriz de `n_1 x n_2`, con las \
            distancias entre los elementos de `lista1` y los elementos de \
            `lista2`.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="l1")

    def l2(self, lista1, lista2=[]):
        """
        Calcula la distancia `L2`, también conocida como la distancia \
        euclidiana, entre uno o dos grupos de textos y/o vectores de entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: str, list, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calcularán la distancias entre cada \
            uno de los textos/vectores de `lista1` con cada uno de los \
            elementos de `lista2`. También es posible ingresar directamente \
            los vectores pre-calculaos de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: str, list, numpy.array, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            `L2` calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias `L2` entre \
            todos los elementos de `lista1`. Si se utilizan los parámetros \
            `lista1` y `lista2` con `n_1` y `n_2` textos/vectores \
            respectivamente, devolverá una matriz de `n_1 x n_2`, con las \
            distancias entre los elementos de `lista1` y los elementos de \
            `lista2`.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="l2")

    def minkowski(self, lista1, lista2=[], p=2):
        """
        Calcula la distancia de Minkowski entre uno o dos grupos de textos \
        y/o vectores de entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: str, list, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calcularán la distancias entre cada \
            uno de los textos/vectores de `lista1` con cada uno de los \
            elementos de `lista2`. También es posible ingresar directamente \
            los vectores pre-calculaos de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: str, list, numpy.array, opcional
        :param p: Orden o grado de la distancia \
            de Minkowski que se desea calcular. Si `p = 1`, la distancia \
            calculada es equivalente a la distancia de Manhattan (L1) y \
            cuando `p=2` la distancia calculada es equivalente a la distancia \
            euclidiana (L2). Valor por defecto `2`.
        :type p: int
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
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

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: str, list, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calcularán la distancias entre cada \
            uno de los textos/vectores de `lista1` con cada uno de los \
            elementos de `lista2`. También es posible ingresar directamente \
            los vectores pre-calculaos de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: str, list, numpy.array, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="jaccard")

    def hamming(self, lista1, lista2=[]):
        """
        Calcula la distancia de Hamming entre uno o dos grupos de textos y/o \
        vectores de entrada.

        :param lista1: Texto o lista de textos de interés para \
            el cálculo de las distancias. También es posible ingresar \
            directamente los vectores pre-calculados de los textos en un \
            arreglo de numpy o una matriz dispersa.
        :type lista1: str, list, numpy.array
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se calcularán la distancias entre cada \
            uno de los textos/vectores de `lista1` con cada uno de los \
            elementos de `lista2`. También es posible ingresar directamente \
            los vectores pre-calculaos de los textos en un arreglo de numpy o \
            una matriz dispersa. Valor por defecto `[]`.
        :type lista2: str, list, numpy.array, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.distancia_pares(lista1, lista2, tipo_distancia="hamming")


# Clase DiferenciaStrings ----------------------------------------------------


class DiferenciaStrings:
    """
    Esta clase se recomienda para comparaciones de strings relativamente \
    cortos, como nombres, direcciones y otras cadenas de caracteres \
    similares. Para textos más extensos, se recomiendan las clases \
    :py:meth:`comparacion.Similitud` o :py:meth:`comparacion.Distancia`.
    """

    def comparacion_pares(self, texto1, texto2, tipo="levenshtein", norm=None):
        """
        Permite hacer comparaciones entre dos textos de entrada, de acuerdo a \
        un tipo de distancia o similitud determinado.

        :param texto1: Primer texto de interés a comparar.
        :type texto1: str
        :param texto2: Segundo texto de interés a comparar.
        :type texto2: str
        :param tipo: Criterio de comparación a utilizar entre los textos. \
            Valor por defecto `'levenshtein'`.
        :type tipo: {'damerau_levenshtein', 'levenshtein', 'hamming', \
            'jaro_winkler', 'jaro'}, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (float) Valor resultado de la comparación entre `texto1` y \
            `texto2`.
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
        Permite hacer comparaciones entre una o dos listas de textos de \
        entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param tipo: Criterio de comparación a utilizar entre los textos. \
            Valor por defecto `'levenshtein'`.
        :type tipo: {'damerau_levenshtein', 'levenshtein', 'hamming', \
            'jaro_winkler', 'jaro'}, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
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
        Permite calcular la distancia de Levenshtein entre una o dos listas \
        de textos de entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.comparacion_lista(lista1, lista2, "levenshtein", norm)

    def distancia_damerau_levenshtein(self, lista1, lista2=[], norm=None):
        """
        Permite calcular la distancia de Damerau-Levenshtein entre una o dos \
        listas de textos de entrada.

        Permite calcular la distancia de Levenshtein entre una o dos listas \
        de textos de entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.comparacion_lista(
            lista1, lista2, "damerau_levenshtein", norm
        )

    def distancia_hamming(self, lista1, lista2=[], norm=None):
        """
        Permite calcular la distancia de Hamming entre una o dos listas de \
        textos de entrada.

        Permite calcular la distancia de Levenshtein entre una o dos listas \
        de textos de entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.comparacion_lista(lista1, lista2, "hamming", norm)

    def similitud_jaro(self, lista1, lista2=[]):
        """
        Permite calcular la similitud de Jaro entre una o dos listas de \
        textos de entrada.

        Permite calcular la distancia de Levenshtein entre una o dos listas \
        de textos de entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.comparacion_lista(lista1, lista2, "jaro")

    def similitud_jaro_winkler(self, lista1, lista2=[]):
        """
        Permite calcular la similitud de Jaro-Winkler entre una o dos listas \
        de textos de entrada.

        Permite calcular la distancia de Levenshtein entre una o dos listas \
        de textos de entrada.

        :param lista1: Texto o lista de textos de interés para \
            realizar las comparaciones.
        :type lista1: str, list
        :param lista2: Texto o lista de textos para comparar. Si se \
            utiliza este parámetro, se harán las comparaciones entre cada uno \
            de los textos de `lista1` con cada uno de los textos de `lista2`. \
            Valor por defecto `[]`.
        :type lista2: str, list, opcional
        :param norm: Permite normalizar los resultados en función de la \
            longitud de los textos. Si `norm = 1` se normaliza en función al \
            texto más corto, si `norm = 2` se normaliza en función al texto \
            de mayor extensión.
        :type norm: {1,2}, opcional
        :return: (numpy.array) Matriz de dos dimensiones con las distancias \
            calculadas entre los textos/vectores de entrada. Si solo se \
            utilizó el parámetro `lista1` con `n` textos/vectores, devolverá \
            una matriz de `n x n` simétrica, con las distancias entre todos \
            los elementos de `lista1`. Si se utilizan los parámetros `lista1` \
            y `lista2` con `n_1` y `n_2` textos/vectores respectivamente, \
            devolverá una matriz de `n1 x n2`, con las distancias entre los \
            elementos de `lista1` y los elementos de `lista2`.
        """
        return self.comparacion_lista(lista1, lista2, "jaro_winkler")
