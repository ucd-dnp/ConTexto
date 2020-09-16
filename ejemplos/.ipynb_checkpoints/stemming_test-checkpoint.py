import os
import sys
from datetime import datetime as dt

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.stemming import Stemmer, stem_texto

# textos de prueba
texto = 'Esta es una prueba para ver si las funciones son correctas y funcionan bien. Perritos y gatos van a la casita'
texto_ingles = 'This is a test writing to study if these functions are performing well.'
textos = [
    "Esta es una primera entrada en el grupo de textos",
    "El Pibe Valderrama empezó a destacar jugando fútbol desde chiquitin",
    "De los pájaros del monte yo quisiera ser canario",
    "Finalizando esta listica, se incluye una última frase un poquito más larga que las anteriores."
]

### 1. Stemming ###
texto_stem = stem_texto(texto, 'auto')

# 1.1 Prueba en otro lenguaje
stem_english = stem_texto(texto_ingles, 'inglés')

# 1.2 Stemming de varios textos con un solo objeto (para mayor rapidez)

# Opción 1: se inicializa el lematizador en cada texto
tic = dt.now()
for t in textos:
    print(stem_texto(t))

tiempo_1 = (dt.now() - tic).total_seconds()

# Opción 2: se utiliza solo un lematizador para todos los textos
tic = dt.now()
stemmer = Stemmer(lenguaje='español')
for t in textos:
    print(stem_texto(t, stemmer=stemmer))

tiempo_2 = (dt.now() - tic).total_seconds()

print('\n***************\n')
print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
print(f'Tiempo con opción 2: {tiempo_2} segundos\n')
