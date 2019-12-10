import pandas as pd
import gensim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


####### BOW / TF-IDF  #########
class VectorizadorFrecuencias():
    def __init__(self, tipo='bow', ngram_range=(1,1),max_feat=None,idf=True):
        if tipo.lower() == 'bow':
            self.tipo = tipo.lower()
            self.model = CountVectorizer(ngram_range=ngram_range,max_features=max_feat)
        elif tipo.lower() == 'tfidf':
            self.tipo = tipo.lower()
            self.model = TfidfVectorizer(ngram_range=ngram_range,max_features=max_feat,use_idf=idf)
        else:
            print('Por favor seleccionar un tipo de modelo válido (bow o tfidf)')
            return None

    def entrenar(self, x):
        self.model.fit(x)

    def vectorizar(self, x, disperso=True):
        vectores = self.model.transform(x)
        if not disperso:
            vectores = vectores.toarray()
        return vectores

    def vocabulario(self):
        vocab = self.model.vocabulary_
        vocab = pd.DataFrame.from_dict(vocab, orient='index', columns=['valor'])
        vocab = vocab.sort_values('valor')
        vocab['palabra'] = vocab.index
        vocab.index = range(len(vocab))
        return vocab

    # A partir de un vector o grupo de vectores, devuelve los términos con frecuencia mayor a 0 
    # en el documento (Solo disponible para TF-IDF)
    def inversa(self, x):
        if self.tipo == 'tfidf':
            return self.model.inverse_transform(x)
        else:
            pass

####### Hashing #########
class VectorizadorHash():
    def __init__(self, n_features=100):
        self.model = HashingVectorizer(n_features=n_features)

# create the transform
vectorizer = HashingVectorizer(n_features=200)
# encode document
X_hash = vectorizer.transform(base_filtrada.texto_limpio)
# .todense() vuelve la matriz dispersa en matriz "normal"? - averiguar

  
# ####### Definición de funciones para vectorizar textos utilizando Doc2Vec  #########
    
# # Función para procesar una lista de textos
# def read_list(lista):
#     for i, line in enumerate(lista):
#         line = gensim.utils.simple_preprocess(line)
#         yield gensim.models.doc2vec.TaggedDocument(line, [i])
        
# # Función para entrenar un modelo a partir de un corpus de entrenamiento
# def entrenar_modelo_doc2vec(train_corpus,long_vector=100,minima_cuenta=5,epocas=20, semilla=1):
#     # Inicializar modelo
#     model = gensim.models.doc2vec.Doc2Vec(vector_size=long_vector, min_count=minima_cuenta, epochs=epocas, seed=semilla)
#     # Construir vocabulario
#     model.build_vocab(train_corpus)
#     # Entrenar modelo
#     model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
#     return model

# # Función que aplica un determinado modelo a un documento para vectorizarlo
# def vectorizar_texto(texto,model):
#     tokenizado = gensim.utils.simple_preprocess(texto)
#     model.random.seed(13)  # Esto se hace para que siempre devuelva el mismo vector
#     return model.infer_vector(tokenizado,alpha=0.025,steps=60)


# # (Ejemplo de uso)
# semilla = 30

# # Definir corpus de entrenamiento para el texto
# clean_corpus = list(read_list(base_filtrada['texto_limpio']))

# # Entrenar modelos
# clean_model = entrenar_modelo_doc2vec(clean_corpus,tamaño_vector=150)

# # Crear data frame para el texto, con los vectores extraídos

# clean_vec = [vectorizar_texto(i,clean_model) for i in base_filtrada['texto_limpio']]
# X_doc2vec = np.array(clean_vec)    
