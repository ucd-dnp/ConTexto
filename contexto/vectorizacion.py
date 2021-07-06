import numpy as np
import pandas as pd
from gensim.models import doc2vec
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from lenguajes import definir_lenguaje
from utils.auxiliares import cargar_objeto, guardar_objeto


# BOW / TF-IDF  #########
class VectorizadorFrecuencias:
    def __init__(
        self,
        tipo="bow",
        rango_ngramas=(1, 1),
        max_elementos=None,
        idf=True,
        archivo_modelo=None,
        **kwargs,
    ):
        """
        Constructor de la clase `VectorizadorFrecuencias`. \
        Permite hacer vectorizaciones usando Bag of Words (BOW) o TF-IDF.

        :param tipo: Determina el tipo de vectorizador a inicializar. \
            Valor por defecto `'bow'`.
        :type tipo: {'bow', 'tfidf'}, opcional
        :param rango_ngramas: Límite inferior y superior del rango de \
            valores `n` para los diferentes n-gramas que se van a extraer. \
            Por ejemplo, un `rango_ngramas` de `(1, 1)` significa solo \
            unigramas, `(1, 2)` significa unigramas y bigramas, y `(2, 2)` \
            significa solo bigramas. Valor por defecto `(1, 1)`.
        :type rango_ngramas: tuple (int, int), opcional
        :param max_elementos: Número máximo de términos a ser tenidos en \
            cuenta, se escogen los  términos más frecuentes. \
            Si `max_elementos = None`, se escogen todos los terminos. \
            Valor por defecto `None`.
        :type max_elementos: int, opcional
        :param idf: Habilita la reponderación de pesos de los términos usando \
            IDF. Si `idf = False`, se calcula solo la parte TF del \
            vectorizador. Valor por defecto `True`.
        :type idf: bool, opcional
        :param archivo_modelo: Ruta de ubicación del archivo vectorizador en \
            formato pickle. Permite cargar un vectorizador generado \
            previamente, los demás parámetros de inicialización no serán \
            tenidos en cuenta, pues se tomarán del vectorizador cargado. \
            Valor por defecto `None`.
        :type archivo_modelo: str, opcional
        :param kwargs: Parámetros adicionales que aceptan las clases \
            `CountVectorizer` y `TfidfVectorizer` de la librería \
            `scikit-learn`. Para mayor información sobre estas clases, y los \
            párametros adicionales que se pueden configurar, consultar su \
            documentacion en: \
            https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_extraction.text.
        """
        tipo = tipo.lower()
        if archivo_modelo is not None:
            self.vectorizador = cargar_objeto(archivo_modelo)
        elif tipo == "bow":
            self.tipo = tipo
            self.vectorizador = CountVectorizer(
                ngram_range=rango_ngramas, max_features=max_elementos, **kwargs
            )
        elif tipo in ["tfidf", "tf-idf", "tf_idf", "tf idf"]:
            self.tipo = "tfidf"
            self.vectorizador = TfidfVectorizer(
                ngram_range=rango_ngramas,
                max_features=max_elementos,
                use_idf=idf,
                **kwargs,
            )
        else:
            print(
                "Por favor seleccionar un tipo de modelo válido (bow o tfidf)"
            )
            return None

    def ajustar(self, textos, archivo_salida=None):
        """
        Permite ajustar el vocabulario  del vectorizador de acuerdo con \
        los textos de entrada.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser procesados por el vectorizador.
        :type textos: like-Array, iterable
        :param archivo_salida: Ruta donde desea exportar el vectorizador \
            ajustado en formato pickle. Si `archivo_salida = None` no se \
            guarda el vectorizador ajustado. Valor por defecto `None`.
        :type archivo_salida: str, opcional
        """
        self.vectorizador.fit(textos)
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta
        # ubicación
        if archivo_salida is not None:
            guardar_objeto(self.vectorizador, archivo_salida)

    # Para mantener "nomenclatura sklearn"
    def fit(self, textos, archivo_salida=None):
        """
        Permite al vectorizador aprender el vocabulario de acuerdo con \
        los textos de entrada. **Llama la función ajustar**.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser procesados por el vectorizador.
        :type textos: like-Array, iterable
        :param archivo_salida: Ruta donde desea exportar el vectorizador \
            ajustado en formato pickle. Si `archivo_salida = None` no se \
            guarda el vectorizador ajustado. Valor por defecto `None`.
        :type archivo_salida: str, opcional
        """
        self.ajustar(textos, archivo_salida)

    def vectorizar(self, textos, disperso=False):
        """
        Vectoriza los textos utilizando el vectorizador. \
        Transformando los textos en una matriz documentos-términos.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: array-like, iterable
        :param disperso: Si es `True` retorna los resultados como una matriz \
            dispersa (csr_matrix). Si es `False` retorna los resultados como \
            un numpy.array. Valor por defecto `False`.
        :type disperso: bool, opcional
        :return: (scipy.csr_matrix o numpy.ndarray) Vectores \
            documentos-términos de la vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = self.vectorizador.transform(textos)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    # Para mantener "nomenclatura sklearn"
    def transform(self, x, disperso=False):
        """
        Vectoriza los textos utilizando el vectorizador. \
        Transformando los textos en una matriz documento-términos. \
        **Llama la función vectorizar**.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: like-Array, iterable
        :param disperso: Si es `True` retorna los resultados como una matriz \
            dispersa (csr_matrix). Si es `False` retorna los resultados como \
            un numpy.array. Valor por defecto `False`.
        :type disperso: bool, opcional
        :return: (scipy.csr_matrix o numpy.ndarray) Vectores \
            documentos-términos de la vectorización de los textos.
        """
        return self.vectorizar(x, disperso)

    def vocabulario(self):
        """
        Retorna el vocabulario del vectorizador entrenado.

        :return: (pandas.DataFrame) Vocabulario del vectorizador.
        """
        try:
            vocab = self.vectorizador.vocabulary_
            vocab = pd.DataFrame.from_dict(
                vocab, orient="index", columns=["posición"]
            )
            vocab = vocab.sort_values("posición")
            vocab["palabra"] = vocab.index
            vocab.index = range(len(vocab))
            return vocab
        except BaseException:
            print(
                (
                    "Debe ajustar primero el vectorizador"
                    "para que exista un vocabulario."
                )
            )
            return None

    def inversa(self, x):
        """
        A partir de un vector o grupo de vectores, devuelve los términos \
        con frecuencia mayor a 0 en el documento.

        :param x: Vector o grupo de vectores correspondientes a la \
            vectorización de textos generada por un vectorizador.
        :type x: array-like
        :return: (list) Lista de arrays con los términos más frecuentes \
            correspondientes a los vectores de cada texto/documento.
        """
        return self.vectorizador.inverse_transform(x)


# Hashing ########
class VectorizadorHash:
    def __init__(self, n_elementos=100, rango_ngramas=(1, 1), **kwargs):
        """
        Constructor de la clase `VectorizadorHash`. \
        Permite hacer vectorizaciones usando hashing.

        :param n_elementos: Hace referencia al número de elementos o  \
            características (columnas) en las matrices de salida. \
            Valor por defecto `100`.
        :type n_elementos: int, opcional
        :param rango_ngramas: Límite inferior y superior del rango de \
            valores `n` para los diferentes n-gramas que se van a extraer. \
            Por ejemplo, un `rango_ngramas` de `(1, 1)` significa solo \
            unigramas, `(1, 2)` significa unigramas y bigramas, y `(2, 2)` \
            significa solo bigramas. Valor por defecto `(1, 1)`.
        :type rango_ngramas: tuple (int, int), opcional
        :param kwargs: Parámetros adicionales que acepta la clase \
            `HashingVectorizer` de la librería scikit-learn. Para mayor \
            información sobre esta clase, y los párametros adicionales que se \
            pueden configurar, consultar su documentacion: \
            https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_extraction.text.
        """
        self.model = HashingVectorizer(
            n_features=n_elementos, ngram_range=rango_ngramas, **kwargs
        )

    def vectorizar(self, textos, disperso=False):
        """
        Vectoriza los textos utilizando el vectorizador. \
        Transformando los textos en una matriz documentos-términos.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: array-like, iterable
        :param disperso: Si es `True` retorna los resultados como una matriz \
            dispersa (csr_matrix). Si es `False` retorna los resultados como \
            un numpy.array. Valor por defecto `False`.
        :type disperso: bool, opcional
        :return: (scipy.csr_matrix o numpy.ndarray) Vectores \
            documentos-términos de la vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = self.model.transform(textos)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    # Para mantener "nomenclatura sklearn"
    def transform(self, textos, disperso=False):
        """
        Vectoriza los textos utilizando el vectorizador. \
        Transformando los textos en una matriz documento-términos. \
        **Llama la función `vectorizar`**.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: array-like, iterable
        :param disperso: Si es `True` retorna los resultados como una matriz \
            dispersa (csr_matrix). Si es `False` retorna los resultados como \
            un numpy.array. Valor por defecto `False`.
        :type disperso: bool, opcional
        :return: (scipy.csr_matrix o numpy.ndarray) Vectores \
            documentos-términos de la vectorización de los textos.
        """
        return self.vectorizar(textos, disperso)


# Word2Vec con spacy #########
class VectorizadorWord2Vec:
    def __init__(self, lenguaje="es", dim_modelo="md", maxima_longitud=None):
        """
        Constructor de la clase `VectorizadorWord2Vec`. \
        Permite hacer vectorizaciones utilizando `Word2Vec`. \
        Utiliza un modelo pre-entrenado.

        :param lenguaje: Define el lenguaje del corpus utilizado \
            al pre-entrenar el vectorizador, el lenguaje debe corresponder \
            al idioma del texto de entrada. Para mayor información, \
            consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`. \
            Valor por defecto `'es'`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}, opcional
        :param dim_modelo: Tamaño del modelo para pre-entrenar el \
            vectorizador. 'lg' es grande (large), 'md' es \
            mediano (medium) y 'sm' es pequeño (small). Los modelos más \
            grandes usualmente obtienen mejores resultados, pero requieren \
            mayor tiempo de carga. Valor por defecto `'md'`.
        :type dim_modelo: {'lg', 'md', 'sm'}, opcional
        :param maxima_longitud: Establecer la máxima longitud (número de \
            caracteres) que acepta el vectorizador en un texto de entrada. Si \
            `maxima_longitud = None`, se utilizará la máxima longitud que \
            trae Spacy por defecto (1 millón de caracteres). \
            Valor por defecto `None`.
        :type maxima_longitud: int, opcional
        """
        # Definir lenguaje del vectorizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar vectorizador
        self.iniciar_vectorizador(dim_modelo, maxima_longitud)

    def establecer_lenguaje(self, lenguaje):
        """
        Permite establecer el lenguaje a ser utilizado por el vectorizador.

        :param lenguaje: Define el lenguaje del corpus utilizado \
            al pre-entrenar el vectorizador, el lenguaje debe corresponder \
            al idioma del texto de entrada. Para mayor información, \
            consultar la sección de \
            :ref:`Lenguajes soportados <seccion_lenguajes_soportados>`.
        :type lenguaje: {'es', 'en', 'fr', 'ge'}
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_vectorizador(self, dim_modelo, maxima_longitud):
        """
        Permite cargar el modelo de vectorizador a utilizar.

        :param dim_modelo: Tamaño del modelo para pre-entrenar el \
            vectorizador. 'lg' es grande (large), 'md' es \
            mediano (medium) y 'sm' es pequeño (small). Los modelos más \
            grandes usualmente obtienen mejores resultados, pero requieren \
            mayor tiempo de carga.
        :type dim_modelo: {'lg', 'md', 'sm'}
        :param maxima_longitud: Establecer la máxima longitud (número de \
            caracteres) que acepta el vectorizador en un texto de entrada. Si \
            `maxima_longitud = None`, se utilizará la máxima longitud que \
            trae Spacy por defecto (1 millón de caracteres).
        :type maxima_longitud: int
        """
        self.vectorizador = None
        if self.lenguaje is not None:
            from utils.spacy_funcs import cargar_modelo

            self.vectorizador = cargar_modelo(
                dim_modelo, self.lenguaje, maxima_longitud
            )

    def vectorizar_texto(self, texto, quitar_desconocidas=False):
        """
        Vectoriza el texto utilizando el vectorizador. \
        Transformando el texto en un vector documento-términos.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: array-like, iterable
        :param quitar_desconocidas: Cuando este argumento es `False`, para \
            cada palabra desconocida se incluirá un vector de solo ceros, lo \
            que afectará el vector promedio resultante. Si es `True` hará \
            que la función sea ligeramente más demorada, pero quizás más \
            precisa, al no tener en cuenta palabras que no están incluídas \
            en el modelo. Valor por defecto `False`.
        :type quitar_desconocidas: bool, opcional
        :return: (numpy.ndarray) Vector documento-términos de la \
            vectorización del texto.
        """
        # Aplicar el modelo al texto
        tokens = self.vectorizador(
            texto, disable=["ner", "parser", "tagger", "lemmatizer"]
        )
        vector_doc = tokens.vector
        if quitar_desconocidas:
            # Crear lista con todos los vectores de palabras reconocidas
            vectores = []
            for token in tokens:
                if token.has_vector:
                    vectores.append(token.vector)
            # Convertir lista en un array, y sacar el vector promedio
            if len(vectores) > 0:
                vectores = np.array(vectores)
                vector_doc = np.mean(vectores, axis=0)
        # Devolver vector del texto
        return vector_doc

    def vectorizar(self, textos, quitar_desconocidas: bool = False):
        """
        Vectoriza los textos utilizando el vectorizador. \
        Transformando los textos en una matriz documentos-términos. \
        **Llama la función `vectorizar_texto`**.

        :param textos: Objeto iterable con textos, unicode u archivos de \
            texto de interés para ser vectorizados.
        :type textos: array-like, iterable
        :param quitar_desconocidas: Cuando este argumento es `False`, para \
            cada palabra desconocida se incluirá un vector de solo ceros, lo \
            que afectará el vector promedio resultante. Si es `True` hará \
            que la función sea ligeramente más demorada, pero quizás más \
            precisa, al no tener en cuenta palabras que no están incluídas \
            en el modelo. Valor por defecto `False`.
        :type quitar_desconocidas: bool, opcional
        :return: (numpy.ndarray) Vector documento-términos de la \
            vectorización del texto.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [
            self.vectorizar_texto(t, quitar_desconocidas) for t in textos
        ]
        return np.array(vectores)

    def vectores_palabras(self, texto, tipo="diccionario"):
        """
        Retorna las palabras y vectores que pertenecen a un texto.

        :param texto: Texto de interés a ser procesado.
        :type texto: str
        :param tipo: Si `tipo = 'diccionario'` retorna los resultados como \
            un objeto tipo diccionario, si es `tipo = 'dataframe'`, retorna \
            los resultados como un objeto tipo pandas.DataFrame. Valor por \
            defecto `'diccionario'`.
        :type tipo: {'diccionario', 'dataframe'}, opcional
        :return: (dict o dataframe) Palabras y vectores del texto.
        """
        # Aplicar el modelo al texto
        tokens = self.vectorizador(texto)
        # Iniciar el diccionario y empezar a llenarlo
        vectores = {}
        for token in tokens:
            if token not in vectores.keys():
                vectores[token] = token.vector
        # Retornar el objeto, de acuerdo a su tipo
        if tipo.lower() in ["diccionario", "dict"]:
            return vectores
        elif tipo.lower() in ["tabla", "dataframe", "df"]:
            vectores = pd.DataFrame(vectores).T
            vectores.reset_index(level=0, inplace=True)
            vectores.columns = ["palabra"] + [
                f"x_{i}" for i in range(1, vectores.shape[1])
            ]
            return vectores
        else:
            print(
                "Debe escoger una estructura válida (diccionario o dataframe)"
            )
            return None

    def similitud_textos(self, t1, t2):
        """
        Calcula la similitud coseno entre 2 palabras o textos.

        :param t1: Primer texto de interés para el cálculo de similitud.
        :type t1: str
        :param t2: Segundo texto de interés para el cálculo de similitud.
        :type t2: str
        :return: (float) Valor entre 0 y 1, donde 1 representa que los textos \
            son iguales.
        """
        # Aplicar vectorizador a ambos textos de entrada
        to1 = self.vectorizador(t1)
        to2 = self.vectorizador(t2)
        # Retornar la similitud entre textos
        return to1.similarity(to2)


# Doc2Vec con gensim #########
class VectorizadorDoc2Vec:
    def __init__(
        self,
        n_elementos=100,
        minima_cuenta=5,
        epocas=20,
        semilla=1,
        archivo_modelo=None,
    ):
        """
        Constructor de la clase `VectorizadorDoc2Vec`. \
        Permite hacer vectorizaciones usando `Doc2Vec`.

        :param n_elementos: Hace referencia al número de elementos o  \
            características (columnas) en las matrices de salida. \
            Valor por defecto `100`.
        :type n_elementos: int, opcional
        :param minima_cuenta: Frecuencia mínima que debe tener cada término \
            para ser tenido en cuenta en el modelo. Valor por defecto `5`.
        :type minima_cuenta: int, opcional
        :param epocas: Número de iteraciones que realiza la red neuronal al \
            entrenar el modelo. Valor por defecto `20`.
        :type epocas: int, opcional
        :param semilla: El modelo tiene un componente aleatorio. Se \
            establece una semilla para poder replicar los resultados. \
            Valor por defecto `1`.
        :type semilla: int, opcional
        :param archivo_modelo: Ruta de archivo de vectorizador en formato \
            pickle. Permite cargar un vectorizador generado previamente, \
            los demás parámetros de inicialización no serán tenidos en \
            cuenta, pues se tomarán del vectorizador cargado. Valor por \
            defecto `None`.
        :type archivo_modelo: str, opcional
        """
        # Si se proporciona un modelo pre-entrenado, este se carga
        if archivo_modelo is not None:
            self.vectorizador = cargar_objeto(archivo_modelo)
        else:
            # Inicializar modelo
            self.vectorizador = doc2vec.Doc2Vec(
                vector_size=n_elementos,
                min_count=minima_cuenta,
                epochs=epocas,
                seed=semilla,
            )

    # Función para procesar una lista de textos y dejarla lista para el modelo
    def __preparar_textos(self, lista_textos):
        """
        Convierte una lista de textos a una lista de tokens luego de
        aplicar un preprocesamiento, para luego ser utilizados \
        por el modelo.

        :param lista_textos: Texto u objeto iterable con textos \
            de interés para ser preprocesados.
        :type lista_textos: str, array-like
        :return: Objeto tipo generador de los textos preprocesados
        """
        if isinstance(lista_textos, str):
            lista_textos = [lista_textos]
        # Generador que va proporcionando los textos pre procesados
        # a medida que se piden
        for i, linea in enumerate(lista_textos):
            linea = simple_preprocess(linea)
            yield doc2vec.TaggedDocument(linea, [i])

    # Función para entrenar un modelo a partir de un corpus de entrenamiento
    def entrenar_modelo(
        self, corpus_entrenamiento, actualizar=False, archivo_salida=None
    ):
        """
        Permite entrenar un modelo a partir de un corpus de entrenamiento.

        :param corpus_entrenamiento: Lista de textos de interes para \
            entrenar el modelo.
        :type corpus_entrenamiento: list, array-like
        :param actualizar: Si `actualizar = True`, las nuevas palabras en \
            los documentos se agregarán al vocabulario del modelo. \
            Valor por defecto `False`.
        :type actualizar: bool, opcional
        :param archivo_salida: Ruta donde desea exportar el vectorizador \
            ajustado en formato pickle. Si `archivo_salida = None` no se \
            guarda el vectorizador ajustado. Valor por defecto `None`.
        :type archivo_salida: str, opcional
        """
        # Pre procesar los textos de entrenamiento
        corpus_entrenamiento = list(
            self.__preparar_textos(corpus_entrenamiento)
        )
        # Construir vocabulario del modelo
        self.vectorizador.build_vocab(corpus_entrenamiento, update=actualizar)
        # Entrenar modelo
        self.vectorizador.train(
            corpus_entrenamiento,
            total_examples=self.vectorizador.corpus_count,
            epochs=self.vectorizador.epochs,
        )
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta
        # ubicación
        if archivo_salida is not None:
            guardar_objeto(self.vectorizador, archivo_salida)

    # Función para vectorizar un texto con un modelo entrenado
    def vectorizar_texto(self, texto, alpha=0.025, num_pasos=50, semilla=13):
        """
        Vectoriza el texto utilizando el vectorizador entrenado. \
        Transformando el texto en un vector documento-términos.

        :param texto: Texto o textos de interés para ser vectorizado(s).
        :type texto: str, list, array-like
        :param alpha:  Tasa de aprendizaje del modelo. Valor por \
            defecto `0.025`.
        :type alpha: float, opcional
        :param num_pasos: Número de iteraciones usadas para entrenar el \
            nuevo documento. Los valores más grandes toman más tiempo, pero \
            pueden mejorar la calidad y la estabilidad \
            de ejecución a ejecución de los vectores inferidos. Si no se \
            especifica, se reutilizará el valor de épocas de la \
            inicialización del modelo. Valor por defecto `50`.
        :type num_pasos: int, opcional
        :param semilla: El modelo tiene un componente aleatorio. Se \
            establece una semilla para poder replicar los resultados. \
            Valor por defecto `13`.
        :type semilla: int, opcional
        :return: (numpy.ndarray) Vectores documentos-términos de la \
            vectorización de los textos.
        """
        # Vectorizar el texto de entrada
        texto_tokenizado = simple_preprocess(texto)
        # La vectorización tiene un componente aleatorio.
        # Se establece una semilla
        # para que la función siempre devuelva el mismo vector para el mismo
        # texto
        self.vectorizador.random.seed(semilla)
        # Se devuelve el vector
        return self.vectorizador.infer_vector(
            texto_tokenizado, alpha=alpha, steps=num_pasos
        )

    # Función para vectorizar una lista de textos
    def vectorizar(self, textos, alpha=0.025, num_pasos=50, semilla=13):
        """
        Vectoriza los textos utilizando el vectorizador entrenado. \
        Transformando los textos en una matriz documentos-términos. \
        **Llama la función vectorizar_texto**.

        :param texto: Texto o textos de interés para ser vectorizado(s).
        :type texto: str, list, array-like
        :param alpha:  Tasa de aprendizaje del modelo. Valor por \
            defecto `0.025`.
        :type alpha: float, opcional
        :param num_pasos: Número de iteraciones usadas para entrenar el \
            nuevo documento. Los valores más grandes toman más tiempo, pero \
            pueden mejorar la calidad y la estabilidad \
            de ejecución a ejecución de los vectores inferidos. Si no se \
            especifica, se reutilizará el valor de épocas de la \
            inicialización del modelo. Valor por defecto `50`.
        :type num_pasos: int, opcional
        :param semilla: El modelo tiene un componente aleatorio. Se \
            establece una semilla para poder replicar los resultados. \
            Valor por defecto `13`.
        :type semilla: int, opcional
        :return: (numpy.ndarray) Vectores documentos-términos de la \
            vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [
            self.vectorizar_texto(t, alpha, num_pasos, semilla) for t in textos
        ]
        return np.array(vectores)
