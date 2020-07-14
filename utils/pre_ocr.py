'''
Script para probar distinas funciones que permitan hacer las imágenes de entrada más aptas para el OCR
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from PIL import Image

# Función auxiliar para graficar las imágenes


def graficar_img(img, titulo='', dims=(15, 10)):
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
    return cv2.medianBlur(img, 5)

# Aplicar 'thresholding' (umbral para decidir valores)


def umbral_otsu(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


def umbral_adaptivo(img, tipo='gaussian'):
    if tipo == 'gaussian':
        return cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            75,
            15)
    else:
        return cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            75,
            15)


def corregir_giro(img):
    # Adaptada de
    # https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
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


def procesar_img_1(img, enderezar=True):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gris


def procesar_img_2(img, enderezar=True):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    borrosa = blur_img(gris)
    return borrosa


def procesar_img_3(img, enderezar=True):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = umbral_otsu(gris)
    return gris


def procesar_img_4(img, enderezar=True):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    borrosa = blur_img(gris)
    salida = umbral_adaptivo(borrosa)
    if enderezar:
        salida = corregir_giro(salida)
    return salida


def procesar_img_5(img, enderezar=True):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = umbral_otsu(gris)
    salida = blur_img(gris)
    salida = umbral_adaptivo(salida)
    if enderezar:
        salida = corregir_giro(salida)
    return salida
