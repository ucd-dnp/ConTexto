# import the necessary packages
from pdf2image import convert_from_path
from auxiliares import verificar_crear_dir
from PIL import Image
from glob import glob
from pre_ocr import procesar_img_1, procesar_img_2, procesar_img_3, procesar_img_4, procesar_img_5
import os
import cv2
import shutil
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR():
    def __init__(self, preprocesamiento, lenguaje, oem, psm, dir_temporal='temp_pags/'):
        self.preprocesamiento = preprocesamiento
        self.dir_temporal = dir_temporal
        self.lenguaje = lenguaje
        self.oem = oem
        self.psm = psm

    def definir_preprocesamiento(self, preprocesamiento):
        self.preprocesamiento = preprocesamiento

    def definir_lenguaje(self, lenguaje):
        self.lenguaje = lenguaje

    def definir_oem(self, oem):
        self.oem = oem

    def definir_psm(self, psm):
        self.psm = psm

    def imagen_a_texto(self, ubicacion_imagen):
        # load the example image and convert it to grayscale
        imagen = cv2.imread(ubicacion_imagen)
        # check to see if we should apply preprocessing to the image
        if 0 < self.preprocesamiento < 6:
            imagen = eval('procesar_img_{}(imagen)'.format(str(self.preprocesamiento)))
        # write the grayscale image to disk as a temporary file so we can apply
        # OCR to it
        nombre_archivo = "{}.png".format(os.getpid())
        cv2.imwrite(nombre_archivo, imagen)
        # load the image as a PIL/Pillow image, apply OCR, and then delete the
        # temporary file
        config = ("-l {} --oem {} --psm {}".format(self.lenguaje, self.oem, self.psm))
        texto = pytesseract.image_to_string(
            Image.open(nombre_archivo), config=config)
        # Borrar el archivo de imagen preprocesada
        os.remove(nombre_archivo)
        return str(texto)

    def pdf_a_imagen(self, ubicacion_pdf):
        tempo_dir = self.dir_temporal + '/tempo/'
        verificar_crear_dir(self.dir_temporal)
        verificar_crear_dir(tempo_dir)
        paginas = convert_from_path(
            ubicacion_pdf, thread_count=8, output_folder=tempo_dir)
        # Counter to store images of each page of PDF to image
        countador_img = 0
        for pagina in paginas:
            countador_img += 1
            archivo = self.dir_temporal + "/pagina_" + \
                str(countador_img).zfill(7) + ".jpg"
            pagina.save(archivo, 'JPEG')
        # Borrar folder temporal
        shutil.rmtree(tempo_dir)

    def pdf_a_texto(self, ubicacion_pdf, borrar_folder=True):
        self.pdf_a_imagen(ubicacion_pdf)
        imagenes = glob(self.dir_temporal + '/*.jpg')
        paginas = []
        for imagen in imagenes:
            pagina = self.imagen_a_texto(imagen)
            paginas.append(pagina)
        if borrar_folder:
            shutil.rmtree(self.dir_temporal)
        return paginas
