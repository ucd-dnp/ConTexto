import nltk.stem
import treetaggerwrapper

####### Definición de funciones para hacer lematización y stemming de textos  #########

# spanish_tagger = treetaggerwrapper.TreeTagger(TAGLANG='es')
spanish_stemmer = nltk.stem.SnowballStemmer('spanish')

def lemmatize_text(text):
    words_lst = text.split()
    a = treetaggerwrapper.make_tags(esp_tagger.tag_text(words_lst))
    words_lst = [item[2] for item in a]
    return ' '.join(words_lst)

def stem_text(text):
    return ' '.join([spanish_stemmer.stem(word) for word in text.split(" ")])