'''
Script para probar distinas funciones que permitan hacer las imágenes de entrada más aptas para el OCR.

Algunas de estas funciones de preprocesamiento fueron inspiradas o adaptadas del blog de PyImageSearch,
en especial de este artículo: https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from PIL import Image

# Función auxiliar para graficar las imágenes

def graficar_img(img, titulo='', dims=(15, 10)):
    """ Función que grafica y muestra una imagen con Pyplot de Matplotlib.

    :param img: (numpy array). Imagen que se desea graficar
    :param titulo: (string). Título de la gráfica
    :param dims: (tuple). Tamaño (figsize) del gráfico de Pyplot
    """
    plt.figure(figsize=dims)
    plt.title(titulo)
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray')
    else:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
    plt.show()

# Funciones para procesar la imagen ----

# Applicar median blurring ('borrosidad') para remover ruido


def blur_img(img):
    """ Función que aplica blurring o 'borrosidad' a una imagen con el fin de \
        eliminar ruido y facilitar la extracción de texto.
        
    :param img: (numpy array). Imagen sobre la cual se aplica blurring.
    :return: (numpy array). Imagen con blurring.
    """
    return cv2.medianBlur(img, 5)

# Aplicar 'thresholding' (umbral para decidir valores)

def umbral_otsu(img):
    """ Función que aplica el umbral de OTSU sobre una imagen, con el fin de \
    facilitar la extracción del texto.

    :param img: (numpy array). Imagen sobre la cual se desea aplicar el umbral de OTSU.
    :return: (numpy array). Imagen después de aplicar el umbral OTSU.
    """
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


def umbral_adaptivo(img, tipo='gaussian'):
    """ Función que aplica el umbral adaptativo sobre una imagen, con el fin de \
        facilitar la extracción del texto. Suele aplicarse cuando la iluminación es 
        desigual a lo largo de la imagen.

    :param img: (numpy array). Imagen sobre la cual se desea aplicar el umbral adaptativo.
    :param tipo: (string) {'gaussian', None}. En caso de ser 'gaussian', el valor \
        del umbral es igual a la suma ponderada gaussiana de los valores vecinos \
        menos una constante. En caso de ser None, el valor del umbral es igual \
        al promedio de los valores vecino menos una constante.
    return: (numpy array). Imagen después de aplicar el umbral adaptativo.
    """
    if tipo == 'gaussian':
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 75, 15)
    else:
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 75, 15)

def corregir_giro(img):
    """ Función que corrige el alineamiento del texto dentro de una imagen. Función adaptada \
        de https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/

    :param img: (numpy array). Imagen sobre la cual se desea aplicar la corrección de alineamiento.
    return: (numpy array). Imagen con alineamiento del texto corregido.
    """
    invertida = cv2.bitwise_not(img)
    coords = np.column_stack(np.where(invertida > 0))
    angulo = cv2.minAreaRect(coords)[-1]
    if angulo < -45:
        angulo = -(90 + angulo)
    else:
        angulo = -angulo
    (h, w) = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    rotada = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotada


def procesar_img_1(img):
    """ Primera función de preprocesamiento. Se encarga de convertir una imagen a escala de grises
    :param img: (numpy array). Imagen sobre la cual se desea aplicar el preprocesamiento.
    return: (numpy array). Imagen en escala de grises.
    """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gris


def procesar_img_2(img):
    """ Segunda función de preprocesamiento. Se encarga de convertir una imagen a escala de grises \
        y aplicar blurring ('borrosidad').

    :param img: (numpy array). Imagen sobre la cual se desea aplicar el preprocesamiento.
    return: (numpy array). Imagen en escala de grises y después de aplicar blurring.
    """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    borrosa = blur_img(gris)
    return borrosa


def procesar_img_3(img):
    """ Tercera función de preprocesamiento. Se encarga de convertir una imagen a escala de grises \
        y aplicar el umbral de imagen con el método OTSU.
    :param img: (numpy array). Imagen sobre la cual se desea aplicar el preprocesamiento.
    return: (numpy array). Imagen en escala de grises y después de aplicar umbral de OTSU.
    """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = umbral_otsu(gris)
    return gris


def procesar_img_4(img, enderezar=True):
    """ Cuarta función de preprocesamiento. Se encarga de convertir una imagen a escala de grises, \
        aplicar blurring ('borrosidad') y umbral adaptativo. Adicionalmente, permite enderezar el 
        texto de la imagen.
    :param img: (numpy array). Imagen sobre la cual se desea aplicar el preprocesamiento.
    :param enderezar: (bool) {True, False}. Valor por defecto: True. Permite enderezar el texto \
        de la imagen para obtener mejores resultados durante el proceso de extracción de texto.
    return: (numpy array). Imagen en escala de grises, despues de aplicar umbral adaptativo y, si \
        enderezar=True, con el alineamiento del texto corregido.
    """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    borrosa = blur_img(gris)
    salida = umbral_adaptivo(borrosa)
    if enderezar:
        salida = corregir_giro(salida)
    return salida


def procesar_img_5(img, enderezar=True):
    """ Quinta función de preprocesamiento. Se encarga de convertir una imagen a escala de grises, \
    aplicar blurring ('borrosidad') y, umbral de OTSU y umbral adaptativo. Adicionalmente, permite enderezar el 
    texto de la imagen.

    :param img: (numpy array). Imagen sobre la cual se desea aplicar el preprocesamiento.
    :param enderezar: (bool) {True, False}. Valor por defecto: True. Permite enderezar el texto \
        de la imagen para obtener mejores resultados durante el proceso de extracción de texto.
    return: (numpy array). Imagen en escala de grises luego de aplicar umbral de OTSU, blurring, umbral \
        adaptativo y, si enderezar=True, con el alineamiento del texto corregido.
    """
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = umbral_otsu(gris)
    salida = blur_img(gris)
    salida = umbral_adaptivo(salida)
    if enderezar:
        salida = corregir_giro(salida)
    return salida
