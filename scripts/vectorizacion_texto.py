import numpy as np
import pandas as pd
from gensim.models import doc2vec
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from lenguajes import definir_lenguaje
from utils.auxiliares import cargar_objeto, guardar_objeto

####### BOW / TF-IDF  #########


class VectorizadorFrecuencias():
    def __init__(
            self,
            tipo='bow',
            rango_ngramas=(1, 1),
            max_elementos=None,
            idf=True,
            archivo_modelo=''):
        """

        :param tipo:
        :param rango_ngramas:
        :param max_elementos:
        :param idf:
        :param archivo_modelo:
        """
        tipo = tipo.lower()
        if archivo_modelo != '':
            self.vectorizador = cargar_objeto(archivo_modelo)
        elif tipo == 'bow':
            self.tipo = tipo
            self.vectorizador = CountVectorizer(   
                ngram_range=rango_ngramas, max_features=max_elementos)
        elif tipo in ['tfidf', 'tf-idf', 'tf_idf', 'tf idf']:
            self.tipo = 'tfidf'
            self.vectorizador = TfidfVectorizer(
                ngram_range=rango_ngramas, max_features=max_elementos, use_idf=idf)
        else:
            print('Por favor seleccionar un tipo de modelo válido (bow o tfidf)')
            return None

    def ajustar(self, x, archivo_salida=''):
        """

        :param x:
        :param archivo_salida:
        :return:
        """
        self.vectorizador.fit(x)
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta ubicación
        if archivo_salida != '':
            guardar_objeto(self.vectorizador, archivo_salida)

    # Para mantener "nomenclatura sklearn"
    def fit(self, x, archivo_salida=''):
        """

        :param x:
        :param archivo_salida:
        :return:
        """
        self.ajustar(x, archivo_salida)

    def vectorizar(self, textos, disperso=False):
        """

        :param textos:
        :param disperso:
        :return:
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

        :param x:
        :param disperso:
        :return:
        """
        return self.vectorizar(x, disperso)

    def vocabulario(self):
        """

        :return:
        """
        try:
            vocab = self.vectorizador.vocabulary_
            vocab = pd.DataFrame.from_dict(
                vocab, orient='index', columns=['posición'])
            vocab = vocab.sort_values('posición')
            vocab['palabra'] = vocab.index
            vocab.index = range(len(vocab))
            return vocab
        except BaseException:
            print('Debe ajustar primero el vectorizador para que exista un vocabulario.')
            return None

    # A partir de un vector o grupo de vectores, devuelve los términos con frecuencia mayor a 0
    # en el documento
    def inversa(self, x):
        """

        :param x:
        :return:
        """
        return self.vectorizador.inverse_transform(x)

####### Hashing #########


class VectorizadorHash():
    def __init__(self, n_elementos=100, rango_ngramas=(1, 1)):
        """

        :param n_elementos:
        :param rango_ngramas:
        """
        self.model = HashingVectorizer(
            n_features=n_elementos, ngram_range=rango_ngramas)

    def vectorizar(self, textos, disperso=False):
        """

        :param textos:
        :param disperso:
        :return:
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = self.model.transform(textos)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    # Para mantener "nomenclatura sklearn"
    def transform(self, x, disperso=False):
        """

        :param x:
        :param disperso:
        :return:
        """
        return self.vectorizar(x, disperso)

####### Word2Vec con spacy #########


class VectorizadorWord2Vec():
    def __init__(self, lenguaje='es', dim_modelo='md'):
        """

        :param lenguaje:
        :param dim_modelo:
        """
        # Definir lenguaje del vectorizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar vectorizador
        self.iniciar_vectorizador(dim_modelo)

    def establecer_lenguaje(self, lenguaje):
        """

        :param lenguaje:
        :return:
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_vectorizador(self, dim_modelo):
        """

        :param dim_modelo:
        :return:
        """
        self.vectorizador = None
        if self.lenguaje is not None:
            from utils.spacy_funcs import cargar_modelo
            self.vectorizador = cargar_modelo(dim_modelo, self.lenguaje)

    def vectorizar_texto(self, texto, quitar_desconocidas: bool=False):
        """

        :param texto:
        :param quitar_desconocidas:
        :return:
        """
        # Aplicar el modelo al texto
        tokens = self.vectorizador(texto)
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

    def vectorizar(self, textos, quitar_desconocidas: bool=False):
        """

        :param textos:
        :param quitar_desconocidas:
        :return:
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [self.vectorizar_texto(t, quitar_desconocidas) for t in textos]
        return np.array(vectores)

    def vectores_palabras(self, texto, tipo='diccionario'):
        """

        :param texto:
        :param tipo:
        :return:
        """
        # Aplicar el modelo al texto
        tokens = self.vectorizador(texto)   
        # Iniciar el diccionario y empezar a llenarlo
        vectores = {}
        for token in tokens:
            if token not in vectores.keys():
                vectores[token] = token.vector
        # Retornar el objeto, de acuerdo a su tipo
        if tipo.lower() in ['diccionario', 'dict']:
            return vectores
        elif tipo.lower() in ['tabla', 'dataframe', 'df']:
            vectores = pd.DataFrame(vectores).T
            vectores.reset_index(level=0, inplace=True)
            vectores.columns = ['palabra'] + [f'x_{i}' for i in range(1, vectores.shape[1])]
            return vectores
        else:
            print('Debe escoger una estructura válida (diccionario o dataframe)')
            return None

    def similitud_textos(self, t1, t2):
        """

        :param t1:
        :param t2:
        :return:
        """
        # Aplicar vectorizador a ambos textos de entrada
        to1 = self.vectorizador(t1)
        to2 = self.vectorizador(t2)
        # Retornar la similitud entre textos
        return to1.similarity(to2)

####### Doc2Vec con gensim #########


class VectorizadorDoc2Vec():
    def __init__(self, n_elementos=100, minima_cuenta=5, epocas=20, semilla=1, archivo_modelo=''):
        """

        :param n_elementos:
        :param minima_cuenta:
        :param epocas:
        :param semilla:
        :param archivo_modelo:
        """
        # Si se proporciona un modelo pre-entrenado, este se carga
        if archivo_modelo != '':
            self.vectorizador = cargar_objeto(archivo_modelo)
        else:
            # Inicializar modelo
            self.vectorizador = doc2vec.Doc2Vec(vector_size=n_elementos, min_count=minima_cuenta, epochs=epocas, seed=semilla)

    # Función para procesar una lista de textos y dejarla lista para el modelo
    def preparar_textos(self, lista_textos):
        """

        :param lista_textos:
        :return:
        """
        if type(lista_textos) == str:
            lista_textos = [lista_textos]
        # Generador que va proporcionando los textos pre procesados
        # a medida que se piden
        for i, linea in enumerate(lista_textos):
            linea = simple_preprocess(linea)
            yield doc2vec.TaggedDocument(linea, [i])

    # Función para entrenar un modelo a partir de un corpus de entrenamiento
    def entrenar_modelo(self, corpus_entrenamiento, actualizar=False, archivo_salida=''):
        """

        :param corpus_entrenamiento:
        :param actualizar:
        :param archivo_salida:
        :return:
        """
        # Pre procesar los textos de entrenamiento
        corpus_entrenamiento = list(self.preparar_textos(corpus_entrenamiento))
        # Construir vocabulario del modelo
        self.vectorizador.build_vocab(corpus_entrenamiento, update=actualizar)
        # Entrenar modelo
        self.vectorizador.train(corpus_entrenamiento, total_examples=self.vectorizador.corpus_count, epochs=self.vectorizador.epochs)
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta ubicación
        if archivo_salida != '':
            guardar_objeto(self.vectorizador, archivo_salida)

    # Función para vectorizar un texto con un modelo entrenado
    def vectorizar_texto(self, texto, alpha=0.025, num_pasos=50, semilla=13):
        """

        :param texto:
        :param alpha:
        :param num_pasos:
        :param semilla:
        :return:
        """
        # Vectorizar el texto de entrada
        tokenizado = simple_preprocess(texto)
        # La vectorización tiene un componente aleatorio. Se establece una semilla
        # para que la función siempre devuelva el mismo vector para el mismo texto
        self.vectorizador.random.seed(semilla)
        # Se devuelve el vector
        return self.vectorizador.infer_vector(tokenizado, alpha=alpha, steps=num_pasos)           

    # Función para vectorizar una lista de textos
    def vectorizar(self, textos, alpha=0.025, num_pasos=50, semilla=13):
        """

        :param textos:
        :param alpha:
        :param num_pasos:
        :param semilla:
        :return:
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [self.vectorizar_texto(t, alpha, num_pasos, semilla) for t in textos]
        return np.array(vectores)
