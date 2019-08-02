# import the necessary packages
import cv2
import shutil
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import os

from pre_ocr import procesar_imagen
from glob import glob
from pdf2image import convert_from_path 
from PIL import Image
from utils import verify_create_dir

class OCR():
	def __init__(self, preprocess=True, folder_dir='temp_pags/', lang='spa', oem=2, psm=3):
		self.preprocess = preprocess
		self.folder_dir = folder_dir
		self.lang = lang
		self.oem = oem
		self.psm = psm
	def image2text(self, image_path):
		# load the example image and convert it to grayscale
		image = cv2.imread(image_path)
		# check to see if we should apply preprocessing to the image
		if self.preprocess:
    			image = procesar_imagen(image)
		# write the grayscale image to disk as a temporary file so we can apply OCR to it
		file_name = "{}.png".format(os.getpid())
		cv2.imwrite(file_name, image)
		# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
		config = ("-l {} --oem {} --psm {}".format(self.lang, self.oem, self.psm))
		texto = pytesseract.image_to_string(Image.open(file_name),config=config)
		# texto = pytesseract.image_to_string(Image.open(file_name))
		os.remove(file_name)
		return str(texto)
	def pdf2image(self, pdf_path):
		verify_create_dir(self.folder_dir)
		paginas = convert_from_path(pdf_path, 500)
		# Counter to store images of each page of PDF to image 
		image_counter = 0
		for pagina in paginas:
			image_counter += 1
			filename = self.folder_dir + "/pagina_" + str(image_counter) + ".jpg"
			pagina.save(filename, 'JPEG')
	def pdf2text(self, pdf_path,borrar_folder=True):
		self.pdf2image(pdf_path)
		imagenes = glob(self.folder_dir + '/*.jpg')
		paginas = []
		for imagen in imagenes:
			pagina = self.image2text(imagen)
			paginas.append(pagina)
		if borrar_folder:
			shutil.rmtree(self.folder_dir)
		return paginas


