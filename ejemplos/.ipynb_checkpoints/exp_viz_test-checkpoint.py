import os
import sys

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.lectura import leer_texto
from contexto.limpieza import limpieza_texto, lista_stopwords, remover_stopwords
from contexto.exploracion import grafica_barchart_frecuencias
from contexto.exploracion import matriz_coocurrencias, graficar_coocurrencias
from contexto.exploracion import obtener_ngramas, nube_palabras, par_nubes

# Cargar y limpiar texto de prueba
ruta_cuento = 'in/garcia_marquez_soledad.txt'

# en este caso es necesario cambiar el parámetro "encoding" para una 
# lectura correcta del documento
texto_prueba = leer_texto(ruta_cuento,encoding='latin-1')
texto = limpieza_texto(texto_prueba, quitar_numeros=False,
                       n_min=3, lista_palabras=lista_stopwords())
# Se quita el titulo y autor, que en este caso salen en todas las páginas
texto = remover_stopwords(texto, lista_expresiones=[
                          "gabriel garcía márquez", "cien años soledad"])

# Obtener listas de palabras y bigramas más frecuentes
unigramas = obtener_ngramas(texto, 1)
bigramas = obtener_ngramas(texto, 2)

# Graficar y guardar nubes de palabras y bigramas
nube_palabras(texto, n_grama=1, ubicacion_archivo='out/nube_uni.jpg', semilla=130)
nube_palabras(texto, n_grama=2, ubicacion_archivo='out/nube_bi.jpg')
par_nubes(texto, n1=1, n2=2, ubicacion_archivo='out/nube_uni_bi.jpg')

# Gráficas de barras con las frecuencias
grafica_barchart_frecuencias(
    texto, ubicacion_archivo='out/barras_palabras.jpg', titulo='Frecuencias de palabras')
grafica_barchart_frecuencias(
    texto, ubicacion_archivo='out/barras_bigramas.jpg', n_grama=2, ascendente=False)

# Obtener matriz de co-ocurrencias
mat_doc = matriz_coocurrencias(texto, max_num=60)
mat_ven = matriz_coocurrencias(texto, max_num=60, modo='ventana', ventana=5)

# Graficar co-ocurrencias de palabras en el texto
graficar_coocurrencias(mat_doc, ubicacion_archivo='out/grafo_doc_full.jpg')
graficar_coocurrencias(mat_doc, prop_fuera=80, ubicacion_archivo='out/grafo_doc_top20.jpg')

graficar_coocurrencias(mat_ven, ubicacion_archivo='out/grafo_ven_full.jpg')
graficar_coocurrencias(mat_ven, prop_fuera=80, ubicacion_archivo='out/grafo_ven_top20.jpg')

# Ejemplo con un grupo de textos

textos = [
    'el perro está en la casa',
    'un perro y un gato están en el carro',
    'el carro entro a la casa',
    'el gato salió de la casa para entrar al carro',
    'el carro casi atropella al perro']

textos = [limpieza_texto(t, lista_palabras=lista_stopwords()) for t in textos]

mat_doc = matriz_coocurrencias(textos)
mat_ven = matriz_coocurrencias(textos, modo='ventana', ventana=2)

graficar_coocurrencias(mat_doc)
graficar_coocurrencias(mat_ven)
