import os
import re
import sys
from pprint import pprint

# Añadir la ubiación del paquete al path actual, para poder hacer las
# importaciones
scripts_path = os.path.abspath(os.path.join('../Contexto'))
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from contexto.lectura import Lector, leer_texto
from contexto.escritura import Escritor, escribir_texto

archivo_docx = 'in/prueba_in.docx'
archivo_pdf = 'in/prueba_in.pdf'
archivo_pdf_ocr = 'in/prueba_in_ocr.pdf'
archivo_txt = 'in/prueba_in.txt'
archivo_rtf = 'in/prueba_in.rtf'
archivo_img = 'in/prueba_in.png'

archivos_in = [archivo_docx, archivo_pdf, archivo_pdf_ocr,
               archivo_txt, archivo_rtf, archivo_img]
archivos_out = [re.sub('in', 'out', i) for i in archivos_in]

for i, archivo in enumerate(archivos_in):
    aplicar_ocr = True if 'ocr' in archivo else False
    print('\n------------')
    print(archivo)
    texto = leer_texto(archivo, por_paginas=True, ocr=aplicar_ocr, preprocesamiento=3)
    escribir_texto(archivos_out[i], texto)

# Utilizando las clases lector y escritor
lector = Lector(archivo_img)
texto = lector.archivo_a_texto(ocr=True)
print(texto)

escritor = Escritor('out/test.txt', texto)
escritor.escribir_txt()

# Probar lectura por páginas
word_pags = leer_texto(archivo_docx, por_paginas=True)
escribir_texto('out/word_paginas.txt', word_pags)