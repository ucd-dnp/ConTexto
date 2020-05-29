# import the necessary packages
from pdf2image import convert_from_path
from helper import verify_create_dir
from PIL import Image
from glob import glob
from pre_ocr import procesar_img_1, procesar_img_2, procesar_img_3, procesar_img_4, procesar_img_5
import os
import cv2
import shutil
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR():
    def __init__(self, preprocess, lang, oem, psm, folder_dir='temp_pags/'):
        self.preprocess = preprocess
        self.folder_dir = folder_dir
        self.lang = lang
        self.oem = oem
        self.psm = psm

    def set_preprocess(self, preprocess):
        self.preprocess = preprocess

    def set_lang(self, lang):
        self.lang = lang

    def set_oem(self, oem):
        self.oem = oem

    def set_psm(self, psm):
        self.psm = psm

    def image2text(self, image_path):
        # load the example image and convert it to grayscale
        image = cv2.imread(image_path)
        # check to see if we should apply preprocessing to the image
        if 0 < self.preprocess < 6:
            image = eval('procesar_img_{}(image)'.format(str(self.preprocess)))
        # write the grayscale image to disk as a temporary file so we can apply
        # OCR to it
        file_name = "{}.png".format(os.getpid())
        cv2.imwrite(file_name, image)
        # load the image as a PIL/Pillow image, apply OCR, and then delete the
        # temporary file
        config = ("-l {} --oem {} --psm {}".format(self.lang, self.oem, self.psm))
        texto = pytesseract.image_to_string(
            Image.open(file_name), config=config)
        # texto = pytesseract.image_to_string(Image.open(file_name))
        os.remove(file_name)
        return str(texto)

    def pdf_to_image(self, pdf_path):
        tempo_dir = self.folder_dir + '/tempo/'
        verify_create_dir(self.folder_dir)
        verify_create_dir(tempo_dir)
        paginas = convert_from_path(
            pdf_path, thread_count=8, output_folder=tempo_dir)
        # Counter to store images of each page of PDF to image
        image_counter = 0
        for pagina in paginas:
            image_counter += 1
            filename = self.folder_dir + "/pagina_" + \
                str(image_counter).zfill(7) + ".jpg"
            pagina.save(filename, 'JPEG')
        # Borrar folder temporal
        shutil.rmtree(tempo_dir)

    def pdf2text(self, pdf_path, borrar_folder=True):
        self.pdf_to_image(pdf_path)
        imagenes = glob(self.folder_dir + '/*.jpg')
        paginas = []
        for imagen in imagenes:
            pagina = self.image2text(imagen)
            paginas.append(pagina)
        if borrar_folder:
            shutil.rmtree(self.folder_dir)
        return paginas
