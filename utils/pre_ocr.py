'''
Script para probar distinas funciones que permitan hacer las imágenes de entrada más aptas para el OCR
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from PIL import Image

# Función auxiliar para graficar las imágenes
def plot_img(img, title='', size=(15,10)):
    plt.figure(figsize = size)
    plt.title(title)
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray')
    else:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
    plt.show()

## Funciones para procesar la imagen ----

# Apply median blurring to remove noise
def blur_img(img):
    return cv2.medianBlur(img, 5)

# Apply thresholding
def umbral_otsu(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def umbral_adaptivo(img, tipo='gaussian'):
    if tipo == 'gaussian':
        return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,75,15)
    else:
        return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,75,15)

def corregir_giro(img):
    # Adaptada de https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
    inverted = cv2.bitwise_not(img)
    coords = np.column_stack(np.where(inverted > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
    	angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def procesar_img_1(img, enderezar=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def procesar_img_2(img, enderezar=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = blur_img(gray)
    return blur

def procesar_img_3(img, enderezar=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = umbral_otsu(gray)
    return gray

def procesar_img_4(img, enderezar=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = blur_img(gray)
    out = umbral_adaptivo(blur)
    if enderezar:
        out = corregir_giro(out)
    return out

def procesar_img_5(img, enderezar=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = umbral_otsu(gray)
    out = blur_img(gray)
    out = umbral_adaptivo(out)
    if enderezar:
        out = corregir_giro(out)
    return out



