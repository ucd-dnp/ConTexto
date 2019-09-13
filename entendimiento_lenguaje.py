if self.leng == 'es':
    try:
        self.lematizador = spacy.load('es_core_news_md')
    except:
        try:
            os.system('python -m spacy download es_core_news_md')
            self.lematizador = spacy.load('es_core_news_md')
        except:
            self.lematizador = spacy.blank(self.leng)
else:
    self.lematizador = spacy.blank(self.leng)


import spacy
nlp = spacy.blank('es')
nlp = spacy.load('es_core_news_md')
# nlp = spacy.load('en_core_web_sm')
doc = nlp(texto)

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
