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
        """Constructor de la clase VectorizadorFrecuencias.  \ 
        	Permite hacer vectorizaciones usando Bag of Words (BOW) o TF-IDF.

        :param tipo: (str) {'bow', 'tfidf'}, valor por defecto: 'bow'. \ 
        	Determina el tipo de vectorizador a inicializar. 
        :param rango_ngramas: (tupla) (int, int) valor por defecto: (1, 1). \ 
			Límite inferior y superior del rango de valores n para los \ 
			diferentes n-gramas que se van a extraer. Por ejemplo, \ 
			un rango_ngramas de (1, 1) significa solo unigramas, (1, 2) \ 
			significa unigramas y bigramas, y (2, 2) significa solo bigramas.
        :param max_elementos: (int) valor por defecto: None. Número máximo \ 
        	de términos a ser tenidos en cuenta, se ecogen los max_elementos  \ 
        	términos más frecuentes.
        :param idf: (bool) {True, False} valor por defecto: True. Habilita la \ 
        	reponderación de pesos de los términos usando IDF.
        :param archivo_modelo: (str) valor por defecto: vacío. Ruta de archivo \ 
        	de un vectorizador en formato pickle (pk). Permite cargar un \ 
        	vectorizador generado previamente, los demás parámetros de \ 
        	inicialización no serán tenidos en cuenta, pues se tomarán del \ 
        	vectorizador cargado.
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
        """ Permite al vectorizador aprender el vocabulario de acuerdo a \ 
        los textos de entrada.

        :param x: objeto iterable con textos (str), unicode u archivos de \ 
        	texto de interés para ser procesados por el vectorizador.
        :param archivo_salida: (str) valor por defecto: vacío. Ruta donde \ 
        	desea exportar el vectorizador ajustado. Usar formato pickle (pk)
        """
        self.vectorizador.fit(x)
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta ubicación
        if archivo_salida != '':
            guardar_objeto(self.vectorizador, archivo_salida)

    # Para mantener "nomenclatura sklearn"
    def fit(self, x, archivo_salida=''):
        """ Permite al vectorizador aprender el vocabulario de acuerdo a \ 
        los textos de entrada. **Llama la función ajustar**.

        :param x: objeto iterable con textos (str), unicode u archivos de \ 
        	texto de interés para ser procesados por el vectorizador.
        :param archivo_salida: (str) valor por defecto: vacío. Ruta donde \ 
        	desea exportar el vectorizador ajustado. Usar formato pickle (pk)        
        """
        self.ajustar(x, archivo_salida)

    def vectorizar(self, textos, disperso=False):
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documentos-términos

        :param textos: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param disperso: (bool) {True, False} valor por defecto: False. \ 
			Si es True retorna los resultados como una matriz dispersa \ 
			(csr_matrix). Si es False retorna los resultados como un numpy array
        :return: vectores documentos-términos de la vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = self.vectorizador.transform(textos)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    # Para mantener "nomenclatura sklearn"
    def transform(self, x, disperso=False):
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documento-términos. \ 
        **Llama la función vectorizar**.

        :param x: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param disperso: (bool) {True, False} valor por defecto: False. \ 
			Si es True retorna los resultados como una matriz dispersa \ 
			(csr_matrix). Si es False retorna los resultados como un numpy array
        :return: vectores documentos-términos de la vectorización de los textos.
        """
        return self.vectorizar(x, disperso)

    def vocabulario(self):
        """ Retorna el vocabulario del vectorizador entrenado.

        :return: dataframe con el vocabulario del vectorizador.
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
    
    def inversa(self, x):
        """ A partir de un vector o grupo de vectores, devuelve los términos \ 
        con frecuencia mayor a 0 en el documento.

        :param x: vector o grupo de vectores correspondientes a la \ 
        	vectorización de textos generada por un vectorizador.
        :return: (list) lista de arrays con los términos más frecuentes \ 
        	correspondientes a los vectores de cada texto/documento.
        """
        return self.vectorizador.inverse_transform(x)


####### Hashing #########


class VectorizadorHash():
    def __init__(self, n_elementos=100, rango_ngramas=(1, 1)):
        """Constructor de la clase VectorizadorHash.  \ 
        	Permite hacer vectorizaciones usando hashing.

        :param n_elementos: (int) Hace referencia al número de elementos o  \ 
        	características (columnas) en las matrices de salida.
        :param rango_ngramas: (tupla) (int, int) valor por defecto: (1, 1). \ 
			Límite inferior y superior del rango de valores n para los \ 
			diferentes n-gramas que se van a extraer. Por ejemplo, \ 
			un rango_ngramas de (1, 1) significa solo unigramas, (1, 2) \ 
			significa unigramas y bigramas, y (2, 2) significa solo bigramas.
        """
        self.model = HashingVectorizer(
            n_features=n_elementos, ngram_range=rango_ngramas)

    def vectorizar(self, textos, disperso=False):
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documentos-términos

        :param textos: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param disperso: (bool) {True, False} valor por defecto: False. \ 
			Si es True retorna los resultados como una matriz dispersa \ 
			(csr_matrix). Si es False retorna los resultados como un numpy array
        :return: vectores documentos-términos de la vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = self.model.transform(textos)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    # Para mantener "nomenclatura sklearn"
    def transform(self, x, disperso=False):
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documento-términos. \ 
        **Llama la función vectorizar**.

        :param x: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param disperso: (bool) {True, False} valor por defecto: False. \ 
			Si es True retorna los resultados como una matriz dispersa \ 
			(csr_matrix).Si es False retorna los resultados como un numpy array.
        :return: vectores documentos-términos de la vectorización de los textos.
        """
        return self.vectorizar(x, disperso)
	
	
####### Word2Vec con spacy #########


class VectorizadorWord2Vec():
    def __init__(self, lenguaje='es', dim_modelo='md'):
        """Constructor de la clase VectorizadorWord2Vec. \ 
        	Permite hacer vectorizaciones utilizando Word2Vec. \ 
        	Utiliza un modelo pre entrenado.

        :param lenguaje: (string) {“es”, “en”, “fr”, “it”} Define el \ 
        	lenguaje del corpus utilizado al pre entrenar el vectorizador, \ 
        	el lenguaje debe corresponder al idioma del texto a ser analizado. \ 
        	Los lenguajes posibles son español (“es”), inglés (“en”),  \ 
        	francés (“fr”), italiano (“it”) y otros.
        :param dim_modelo: (str) {'sm', 'md', 'lg'}, valor por defecto: 'md'. \ 
        	Define el tamaño del corpus utilizado al pre entrenar \ 
        	el vectorizador. Siendo sm - pequeño, md - mediano, lg - grande.
        """
        # Definir lenguaje del vectorizador
        self.establecer_lenguaje(lenguaje)
        # Inicializar vectorizador
        self.iniciar_vectorizador(dim_modelo)

    def establecer_lenguaje(self, lenguaje):
        """Permite establecer el lenguaje a ser utilizado por el vectorizador.

        :param lenguaje: (string) {“es”, “en”, “fr”, “it”} Define el \ 
        	lenguaje del corpus utilizado al pre entrenar el vectorizador, \ 
        	el lenguaje debe corresponder al idioma del texto a ser analizado. \ 
        	Los lenguajes posibles son español (“es”), inglés (“en”),  \ 
        	francés (“fr”), italiano (“it”) y otros.
        """
        self.lenguaje = definir_lenguaje(lenguaje)

    def iniciar_vectorizador(self, dim_modelo):
        """Permite cargar el modelo de vectorizador a utilizar.

        :param dim_modelo: (str) {'sm', 'md', 'lg'}, valor por defecto: 'md'. \ 
        	Define el tamaño del corpus utilizado al pre entrenar \ 
        	el vectorizador. Siendo sm - pequeño, md - mediano, lg - grande.
        """
        self.vectorizador = None
        if self.lenguaje is not None:
            from utils.spacy_funcs import cargar_modelo
            self.vectorizador = cargar_modelo(dim_modelo, self.lenguaje)

    def vectorizar_texto(self, texto, quitar_desconocidas: bool=False):
        """ Vectoriza el texto utilizando el vectorizador. \ 
        Transformando el texto en un vector documento-términos.

        :param texto: string de interés para ser vectorizado.
        :param quitar_desconocidas: (bool) {True, False} valor por defecto: False. \ 
             Cuando este argumento es False, para cada palabra desconocida \ 
             se incluirá un vector de solo ceros, lo que afectará el vector \ 
             promedio resultante. Si es True hará que la función sea \ 
             ligeramente más demorada, pero quizás más precisa, al no tener \ 
             en cuenta palabras que no están incluídas en el modelo.
        :return: vector (numpy.ndarray) documento-términos de la \ 
            vectorización del texto.
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
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documentos-términos. \ 
        **Llama la función vectorizar_texto**.

        :param textos: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param quitar_desconocidas: (bool) {True, False} valor por defecto: False. \ 
             Cuando este argumento es False, para cada palabra desconocida \ 
             se incluirá un vector de solo ceros, lo que afectará el vector \ 
             promedio resultante. Si es True hará que la función sea \ 
             ligeramente más demorada, pero quizás más precisa, al no tener \ 
             en cuenta palabras que no están incluídas en el modelo.
        :return: vectores (numpy.ndarray) documentos-términos de la \ 
            vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [self.vectorizar_texto(t, quitar_desconocidas) for t in textos]
        return np.array(vectores)

    def vectores_palabras(self, texto, tipo='diccionario'):
        """ Retorna las palabras y vectores que pertenecen a un texto.

        :param texto: (str) texto de interés a ser procesado.
        :param tipo: (str) {'diccionario', 'dataframe'}, valor por defecto: \ 
            'diccionario'. Si es 'diccionario' retorna los resultados como \ 
            un objeto tipo diccionario, si es 'dataframe', retorna los \ 
            resultados como un objeto tipo dataframe.
        :return: palabras y vectores del texto.
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
        """Calcula la similitud coseno entre 2 palabras o textos.

        :param t1: (str) primer texto de interés para el cálculo de similitud.
        :param t2: (str) segundo texto de interés para el cálculo de similitud.
        :return: (float) valor entre 0 y 1, donde 1 representa que los textos \ 
            son iguales.
        """
        # Aplicar vectorizador a ambos textos de entrada
        to1 = self.vectorizador(t1)
        to2 = self.vectorizador(t2)
        # Retornar la similitud entre textos
        return to1.similarity(to2)


####### Doc2Vec con gensim #########


class VectorizadorDoc2Vec():
    def __init__(self, n_elementos=100, minima_cuenta=5, epocas=20, semilla=1, archivo_modelo=''):
        """Constructor de la clase VectorizadorDoc2Vec.  \ 
            Permite hacer vectorizaciones usando Doc2Vec.

        :param n_elementos: (int) valor por defecto: 100. Número de términos \ 
            a ser tenidos en cuenta en la vectorización.
        :param minima_cuenta: (int) valor por defecto: 5. Frecuencia \ 
            mínima que debe tener cada término para ser tenido en cuenta \ 
            en el modelo.
        :param epocas: (int) valor por defecto: 20. Número de iteraciones \ 
            que realiza la red neuronal para entrenar el modelo.
        :param semilla: (int) valor por defecto: 1. El modelo tiene un \ 
            componente aleatorio. Se establece una semilla para poder \ 
            replicar los resultados.
        :param archivo_modelo: (str) valor por defecto: vacío. Ruta de archivo \ 
            de un vectorizador en formato pickle (pk). Permite cargar un \ 
            vectorizador generado previamente, los demás parámetros de \ 
            inicialización no serán tenidos en cuenta, pues se tomarán del \ 
            vectorizador cargado.
        """
        # Si se proporciona un modelo pre-entrenado, este se carga
        if archivo_modelo != '':
            self.vectorizador = cargar_objeto(archivo_modelo)
        else:
            # Inicializar modelo
            self.vectorizador = doc2vec.Doc2Vec(vector_size=n_elementos, min_count=minima_cuenta, epochs=epocas, seed=semilla)

    # Función para procesar una lista de textos y dejarla lista para el modelo
    def __preparar_textos(self, lista_textos):
        """ Convierte una lista de textos a una lista de tokens luego de
            aplicar un preprocesamiento, para luego ser utilizados \ 
            por el modelo.

        :param lista_textos: string u objeto iterable con textos (str) \ 
            de interés para ser preprocesados.
        :return: objeto tipo generador de los textos preprocesados
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
        """ Permite entrenar un modelo a partir de un corpus de entrenamiento.

        :param corpus_entrenamiento: (list) lista de textos de interes para \ 
            entrenar el modelo.        
        :param actualizar: (bool) {True, False} valor por defecto: False. \ 
            Si True, las nuevas palabras en los documentos se agregarán al \ 
            vocabulario del modelo.
        :param archivo_salida: (str) valor por defecto: vacío. Ruta donde \ 
            desea exportar el vectorizador ajustado. Usar formato pickle (pk)
        :return:
        """
        # Pre procesar los textos de entrenamiento
        corpus_entrenamiento = list(self.__preparar_textos(corpus_entrenamiento))
        # Construir vocabulario del modelo
        self.vectorizador.build_vocab(corpus_entrenamiento, update=actualizar)
        # Entrenar modelo
        self.vectorizador.train(corpus_entrenamiento, total_examples=self.vectorizador.corpus_count, epochs=self.vectorizador.epochs)
        # Si se proporcionó un archivo, se guarda el modelo entrenado en esta ubicación
        if archivo_salida != '':
            guardar_objeto(self.vectorizador, archivo_salida)

    # Función para vectorizar un texto con un modelo entrenado
    def vectorizar_texto(self, texto, alpha=0.025, num_pasos=50, semilla=13):
        """ Vectoriza el texto utilizando el vectorizador. \ 
        Transformando el texto en un vector documento-términos.

        :param texto: string de interés para ser vectorizado.
        :param alpha: (float) valor por defecto: 0.025. \ 
            Tasa de aprendizaje del modelo.
        :param num_pasos: (int) valor por defecto: 50. Número de iteraciones \ 
            usadas para entrenar el nuevo documento. Los valores más grandes \ 
            toman más tiempo, pero pueden mejorar la calidad y la estabilidad \ 
            de ejecución a ejecución de los vectores inferidos. Si no se \ 
            especifica, se reutilizará el valor de épocas de la \ 
            inicialización del modelo.
        :param semilla: (int) valor por defecto: 13. El vectorizador tiene un \ 
            componente aleatorio. Se establece una semilla para poder \ 
            replicar los resultados.
        :return: vectores (numpy.ndarray) documentos-términos de la \ 
            vectorización de los textos.
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
        """ Vectoriza los textos utilizando el vectorizador. \ 
        Transformando los textos en una matriz documentos-términos. \ 
        **Llama la función vectorizar_texto**.

        :param textos: string (str) o lista (list) con textos de interés \ 
            para ser vectorizados.
        :param alpha: (float) valor por defecto: 0.025. \ 
            Tasa de aprendizaje del modelo.
        :param num_pasos: (int) valor por defecto: 50. Número de iteraciones \ 
            usadas para entrenar el nuevo documento. Los valores más grandes \ 
            toman más tiempo, pero pueden mejorar la calidad y la estabilidad \ 
            de ejecución a ejecución de los vectores inferidos. Si no se \ 
            especifica, se reutilizará el valor de épocas de la \ 
            inicialización del modelo.
        :param semilla: (int) valor por defecto: 13. El vectorizador tiene un \ 
            componente aleatorio. Se establece una semilla para poder \ 
            replicar los resultados.
        :return: vectores (numpy.ndarray) documentos-términos de la \ 
            vectorización de los textos.
        """
        if isinstance(textos, str):
            textos = [textos]
        vectores = [self.vectorizar_texto(t, alpha, num_pasos, semilla) for t in textos]
        return np.array(vectores)