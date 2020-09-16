import os
import sys
from datetime import datetime as dt

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.lematizacion import LematizadorSpacy, LematizadorStanza
from contexto.lematizacion import lematizar_texto

# textos de prueba
texto = 'esta es una prueba para ver si las funciones son correctas y funcionan bien. Perritos y gatos van a la casita'
texto_ingles = 'this is a test writing to study if these functions are performing well'
textos = [
    "Esta es una primera entrada en el grupo de textos",
    "El Pibe Valderrama empezó a destacar jugando fútbol desde chiquitin",
    "De los pájaros del monte yo quisiera ser canario",
    "Finalizando esta listica, se incluye una última frase un poquito más larga que las anteriores."
]

### 1. Lematización con librería Spacy ###
texto_lematizado = lematizar_texto(texto)

## 1.1 Prueba en otro lenguaje
lemma_english = lematizar_texto(texto_ingles, 'auto', dim_modelo='small')

## 1.2 Agregar lemmas personalizados

# 1.2.1 Desde archivo
archivo_lemmas = 'in/dict_lemas.json'
texto_lematizado_v2 = lematizar_texto(texto, dict_lemmas=archivo_lemmas)

# 1.2.2 Desde diccionario
segundo_dict = {
    "casita": "casa",
    "casitas": "casa",
    "para": "para",
    "perrito": "perro",
    "perritos": "perro",
    "gatos": "gato"
}
texto_lematizado_v3 = lematizar_texto(texto, dict_lemmas=segundo_dict)

## 1.3 Lematizar varios textos con un solo objeto (para mayor rapidez)

# Opción 1: se inicializa el lematizador en cada texto
tic = dt.now()
for t in textos:
    print(lematizar_texto(t))

tiempo_1 = (dt.now() - tic).total_seconds()

# Opción 2: se utiliza solo un lematizador para todos los textos
tic = dt.now()
lematizador = LematizadorSpacy('es')
for t in textos:
    print(lematizar_texto(t, lematizador=lematizador))

tiempo_2 = (dt.now() - tic).total_seconds()

print('\n***************\n')
print('Tiempo con opción 1: {} segundos\n'.format(tiempo_1))
print('Tiempo con opción 2: {} segundos\n'.format(tiempo_2))


### 2. Lematización con librería Stanza ###
texto_lematizado = lematizar_texto(texto, libreria='stanza')

## 2.1 Prueba en otro lenguaje
'''
Cuando se corre por primera vez la lematización en un idioma, se descargarán
los modelos de ese idioma. Este proceso puede demorar varios minutos, dependiendo
de la calidad de la conexión a internet disponible.
'''
lemma_english = lematizar_texto(texto_ingles, 'auto', libreria='stanza')

## 2.2 Agregar lemmas personalizados
'''
Si se quiere guardar el modelo modificado (para usarlo luego o para seguirlo modificando),
es necesario utilizar los argumentos 'modelo_lemas' y 'archivo_salida'.
De lo contrario, siempre se va a cargar el modelo default
'''

# 2.2.1 Desde archivo
archivo_lemmas = 'in/dict_lemas.json'
texto_lematizado_v2 = lematizar_texto(texto,libreria='stanza',dict_lemmas=archivo_lemmas)

# 2.2.2 Desde diccionario
segundo_dict = {
    "chiquitin": "chico",
    'valderrama': 'valderrama',
    'listica': 'lista'
}

lematizador = LematizadorStanza('es')
print(lematizador.lematizar(textos[1]))
lematizador.modificar_lemmas(dict_lemmas=segundo_dict, archivo_salida='out/modelo_lemas_stanza.pt')
print(lematizador.lematizar(textos[1]))

## 2.3 Lematizar varios textos con un solo objeto (para mayor rapidez)
'''
Dependiendo de los modelos utilizados, lematizar con Stanza es 
más lento que hacerlo con Spacy (el uso de GPU, cuando sea posible, 
puede mejorar esto), pero permite obtener mejores resultados.
'''

# Opción 1: se inicializa el lematizador en cada texto
tic = dt.now()
for t in textos:
    print(lematizar_texto(t, libreria='stanza', modelo_lemas='out/modelo_lemas_stanza.pt'))

tiempo_1 = (dt.now() - tic).total_seconds()

# Opción 2: se utiliza solo un lematizador para todos los textos
tic = dt.now()
lematizador = LematizadorStanza('es', modelo_lemas='out/modelo_lemas_stanza.pt')
for t in textos:
    print(lematizar_texto(t, lematizador=lematizador))

tiempo_2 = (dt.now() - tic).total_seconds()

print('\n***************\n')
print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
print(f'Tiempo con opción 2: {tiempo_2} segundos\n')
