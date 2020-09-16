import os
import sys
from datetime import datetime as dt

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.correccion import Corrector, corregir_texto

# textos de prueba
texto = 'ojala halya un buen hasado de polllo para poder comer delizioso plainventadaext'
texto_ingles = 'this is a tets writting to estudy if thes functions are performing guell'
textos = [
    "Esta es una pirmera entrada en le grupo de testos",
    "El Pive Valderrama empeso a deztacar jugando fútvol desde chikitin",
    "De los pajaros del monnte yo quixiera ser canarrio",
    "Finalisando esta lizta, se inclulle una última frace un pokito más larga ke las amteriores."
]

### 1. Correción ###
texto_corregido = corregir_texto(texto)

# 1.1 Prueba en otro lenguaje
corregido_ingles = corregir_texto(texto_ingles, 'en')

# Si se deja el parámetro lenguaje en "auto", la función identificará
# que lenguaje es el predominante. Esto hará que la corrección sea un
# poco más demorada
corregido_ingles = corregir_texto(texto_ingles, lenguaje='auto')

# 1.2 Detectar palabras conocidas y desconocidas en el texto
corrector = Corrector(lenguaje='es')
corrector.palabras_conocidas(texto)
corrector.palabras_desconocidas(texto)

# 1.3 Palabras candidatas para corregir una palabra mal escrita
corrector.palabras_candidatas('hasado')

### 2. Modificar diccionario para incluir, priorizar o quitar palabras ###
corrector = Corrector(lenguaje='es')
corrector.palabras_desconocidas(texto)

# 2.1 Añadir una palabra al diccionario
corrector.agregar_palabras('plainventadaext')
corrector.palabras_desconocidas(texto)

# 2.2 Quitar una palabra del diccionario
t = 'Head y house son palabras en inglés. En español deberían ser marcadas como desconocidas.'

corrector.palabras_desconocidas(t) 
corrector.quitar_palabras(['head', 'house'])
corrector.palabras_desconocidas(t)

# 2.3 Modificar la frecuencia de una palabra, para que tenga prioridad en
# correcciones
'''
En el texto original queremos que "hasado" se corrija por "asado". Sin embargo, la palabra
"pasado" tiene mayor frecuencia en el diccionario, por lo que se toma como la más probable.

Esto lo podemos modificar por medio del diccionario, para obtener el resultado deseado
(esto puede tener efectos adversos, utilizar con cuidado).
'''
for p in corrector.palabras_candidatas('hasado'):
    freq = corrector.frecuencia_palabra(p)
    print(f'{p}: {freq}')

dict_asado = {'asado': corrector.frecuencia_palabra('pasado') + 1}
corrector.actualizar_diccionario(dict_asado)

for p in corrector.palabras_candidatas('hasado'):
    freq = corrector.frecuencia_palabra(p)
    print(f'{p}: {freq}')

texto_corregido = corrector.correccion_ortografia(texto)

# Las frecuencias de palabras también se pueden modificar con un archivo json que contenga
# el diccionario
ubicacion_dict = 'in/dict_ortografia.json'
corrector.actualizar_diccionario(ubicacion_dict)
corrector.frecuencia_palabra('asado')
corrector.frecuencia_palabra('plainventadaext')

### 3 Corrección de varios textos con un solo objeto (para mayor rapidez) ###

# Opción 1: se inicializa el corrector en cada texto
tic = dt.now()
for t in textos:
    print(corregir_texto(t))

tiempo_1 = (dt.now() - tic).total_seconds()

# Opción 2: se utiliza solo un corrector para todos los textos
tic = dt.now()
corrector = Corrector('spanish')
for t in textos:
    print(corregir_texto(t, corrector=corrector))

tiempo_2 = (dt.now() - tic).total_seconds()

print('\n***************\n')
print(f'Tiempo con opción 1: {tiempo_1} segundos\n')
print(f'Tiempo con opción 2: {tiempo_2} segundos\n')
