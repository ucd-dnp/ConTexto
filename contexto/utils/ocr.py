import cv2
import os
import pytesseract
import shutil
from glob import glob
from pdf2image.exceptions import PDFInfoNotInstalledError
from pdf2image import convert_from_path
from PIL import Image
from auxiliares import verificar_crear_dir
from pre_ocr import procesar_img_1, procesar_img_2, procesar_img_3, procesar_img_4, procesar_img_5

from pytesseract import TesseractNotFoundError, get_tesseract_version

#TODO: corregir mensaje mostrado en consola
try:
    TESSERACT_VERSION = tuple(get_tesseract_version().version)
except TesseractNotFoundError as e:
    print("Tesseract no está en el path, para mayor información revisar XXXXXXXXX")
    exit(1)

class OCR():
    def __init__(self, preprocesamiento, lenguaje, oem, psm, dir_temporal='temp_pags/'):

        """ Constructor por defecto de la clase OCR. Esta clase se encarga de extraer \
        con la metodología de reconocimiento óptico de caracteres (OCR, en inglés)

        :param preprocesamiento: (int) {1,2,3,4,5}. Especifica el nivel de preprocesamiento \
            que se lleva a cabo antes de extraer el texto del archivo. Aplica cuando se utiliza \
            reconocimiento óptico de caracteres (parámetro ocr es True). Las opciones son las siguientes: \
            1: se convierte la imagen a escala de grises
            2: se convierte la imagen a escala de grises y se aplica blurring
            3: se convierte la imagen a escala de grises y se aplica el umbral de imagen con el \
                 método de OTSU
            4: se endereza el texto, se convierte la imagen a escala de grises y se aplica umbral \
                adaptativo
            5: se endereza el texto, se convierte la imagen a escala de grises, se aplica umbral \
                de imagen con el método de OTSU, blurring y umbral adaptativo             
        :param lenguaje: (string). {'es', 'en'}  Se define el \
            lenguaje del texto que se desea extraer. Aplica cuando se utilia reconocimiento \
            óptico de caracteres (el parámetro ocr es True). Tiene las opciones de español \
            ('es') e inglés ('en')
        :param oem: (int) {0, 1, 2, 3}. OEM hace referencia al modo del motor OCR (OCR engine mode \
            en inglés). Tesseract tiene 2 motores, Legacy Tesseract y LSTM, y los parámetros de 'oem' \
            permiten escoger cada uno de estos motores por separado, ambos al tiempo o \
            automáticamente: 
            0: utilizar únicamente el motor Legacy
            1: utilizar únicamente el motor de redes neuronales LSTM  
            2: utilizar los motores Legacy y LSTM
            3: escoger el motor según lo que hay disponible
        :param psm: (int) {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}. PSM hace referencia a \
            los modos de segmentación de las páginas (page segmentation modes, en inglés) de la \
            librería Pytesseract. Cada número hace referencia a un modo de segmentación: \
            0: orientation y detección de script (OSD) únicamente
            1: segmentación automática de páginas con OSD
            2: segmentación automática de págpinas sin OSD ni OCR
            3: segmentación completamente automática de páginas sin OSD
            4: supone una única columna de texto de tamaños variables
            5: supone un único bloque uniforme de texto alineado de forma vertical
            6: asume un único bloque uniforme de texto
            7: trata la imagen como una única línea de texto
            8: trata la imagen como una única palabra
            9: trata la imagen como una única palabra dentro de un círculo
            10: trata la imagen como un único carácter
            11: Buscador de texto disperso. Encontrar la mayor cantidad de texto posible sin un orden en particular
            12: Buscador de texto disperso con OSD
            13: trata el texto como una única línea, sin utilizar métodos específicos de Tesseract
        :param dir_temporal: (string). Ruta donde se guardan páginas temporales de apoyo como imágenes \
            durante el proceso de extracción de texto
        """
        self.preprocesamiento = preprocesamiento
        self.dir_temporal = dir_temporal
        self.lenguaje = lenguaje
        self.oem = oem
        self.psm = psm

    def imagen_a_texto(self, ubicacion_imagen):
        """ Se encarga de leer el texto de archivos de tipo imagen, con extensión 'png', 'jpg' o 'jpeg', \
            luego de aplicar el preprocesamiento definido al iniciar la clase OCR
        :param ubicacion_imagen: (string). Ruta de la imagen que se desea leer
        :return: (string). Texto del archivo tipo imagen leído con la clase OCR
        """
        # Cargar la imagen de entrada        
        imagen = cv2.imread(ubicacion_imagen)
        # Se define el preprocesamiento a aplicar 
        # (si el número está fuera de rango, no se aplica ningún preprocesmiento)
        if 0 < self.preprocesamiento < 6:
            imagen = eval('procesar_img_{}(imagen)'.format(str(self.preprocesamiento)))
        # Se guarda la imagen en un archivo temporal
        nombre_archivo = "{}.png".format(os.getpid())
        cv2.imwrite(nombre_archivo, imagen)
        # Se establecen las opciones para el OCR
        config = ("-l {} --oem {} --psm {}".format(self.lenguaje, self.oem, self.psm))
        # Se carga la imagen como un objeto PIL/Pillow image y se aplica el OCR
        texto = pytesseract.image_to_string(
            Image.open(nombre_archivo), config=config)
        # Borrar el archivo de imagen preprocesada
        os.remove(nombre_archivo)
        return str(texto)

    def pdf_a_imagen(self, ubicacion_pdf):
        """ Se encarga de transformar archivos PDF a imagen
        :param ubicacion_imagen: (string). Ruta del archivo PDF
        """
        tempo_dir = self.dir_temporal + '/tempo/'
        verificar_crear_dir(self.dir_temporal)
        verificar_crear_dir(tempo_dir)
        #TODO: corregir mensaje  mostrado en consola
        try:
            paginas = convert_from_path(
                ubicacion_pdf, thread_count=8, output_folder=tempo_dir)
        except PDFInfoNotInstalledError as e:
            print("Poppler no está instalado o no está en el path del sistema, para mas información consulte XXXX")
            exit(1)
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
        """ Se encarga de leer el texto de archivos PDF ('.pdf'), \
            luego de aplicar el preprocesamiento definido al iniciar la clase OCR
        :param ubicacion_imagen: (string). Ruta deL archivo PDF que se desea leer
        :return: (string). Texto del archivo tipo PDF leído con la clase OCR
        """
        self.pdf_a_imagen(ubicacion_pdf)
        imagenes = glob(self.dir_temporal + '/*.jpg')
        paginas = []
        for imagen in imagenes:
            pagina = self.imagen_a_texto(imagen)
            paginas.append(pagina)
        if borrar_folder:
            shutil.rmtree(self.dir_temporal)
        return paginas
