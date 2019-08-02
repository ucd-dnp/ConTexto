# Función para generar n-gramas
def get_ngrams(text, n ):
    n_grams = ngrams(text.split(' '), n)
    return [ ' '.join(grams) for grams in n_grams]


lista_uni = []
lista_bi = []
lista_tri = []
lista_cuatri = []

for texto in base_filtrada.texto_limpio:
    lista_uni += get_ngrams(texto,1)
    lista_bi += get_ngrams(texto,2)
    lista_tri += get_ngrams(texto,3)
    lista_cuatri += get_ngrams(texto,4)
    
import numpy as np
x, y = np.ogrid[:600, :600]
mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
mask = 255 * mask.astype(int)

for lista in ['lista_uni','lista_bi','lista_tri','lista_cuatri']:
    print('\n ------------- {} ----------'.format(lista))
    cont = Counter(eval(lista))
    dictu = dict(cont.most_common(200))
    wordcl = WordCloud(background_color = 'white',prefer_horizontal=0.6, mask=mask)
    exec(lista + '_cloud = wordcl.generate_from_frequencies(dictu)')
    
    print(cont.most_common(20))