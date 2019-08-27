from collections import Counter
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt

# Función para generar n-gramas a partir de un texto
def obtener_ngramas(texto, n=1, devolver_lista=True):
    lista = texto.split(' ')
    n_gramas = (' '.join(lista[i:i+n]) for i in range(len(lista)) if i + n <= len(lista))
    if devolver_lista:
        n_gramas = list(n_gramas)
    return n_gramas


def nube_palabras(lista, n_palabras=100, plot=True, figsize=(10,10), titulo='Términos más frecuentes'):
    x, y = np.ogrid[:600, :600]
    mask = (x - 300) ** 2 + (y - 300) ** 2 > 260 ** 2
    mask = 255 * mask.astype(int)
    cont = Counter(lista)
    dictu = dict(cont.most_common(n_palabras))
    wordcl = WordCloud(background_color = 'white',prefer_horizontal=0.6, mask=mask)
    figura = wordcl.generate_from_frequencies(dictu)

    if plot:
        # Graficar la imagen generada
        graficar_nube(figura, figsize, titulo)
    
    return figura

def graficar_nube(nube, figsize=(10,10), titulo='Términos más frecuentes'):
    plt.figure(figsize=figsize)
    plt.imshow(nube, interpolation='bilinear')
    plt.title(titulo)
    plt.axis("off")
    plt.show()

    
