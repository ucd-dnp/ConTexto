'''
Código, funciones y clases relacionadas a la carga y lectura de
diferentes tipos de archivo (word, txt, rtf, pdf inicialmente).
'''
import os
from utils.auxiliares import verificar_crear_dir, adecuar_xml

# Clase lector


class Lector():
    def __init__(self, ubicacion_archivo):
        """
        Constructor por defecto de la clase Lector. Esta clase se encarga de extraer \
            el texto de archivos de distintos tipos como Word, PDF, CSV, TXT, RTF e \
            imágenes

        :param ubicacion_archivo: (string). Ruta del archivo que se desea leer
        """
        self.establecer_ubicacion(ubicacion_archivo)

    def establecer_ubicacion(self, ubicacion_archivo):
        """ Define la ubicación del archivo que se desea leer

        :param ubicacion_archivo: (string). Ruta del archivo que se desea leer
        """
        self.ubicacion_archivo = ubicacion_archivo

    def leer_txt(self, encoding="utf-8"):
        """ Se lleva a cabo la lectura del texto de archivos con extensión '.txt'

        :param encoding: (string). Valor por defecto: 'utf-8'. Especifica la codificación \
            del texto que se desea leer
        :return: (string). Texto del archivo '.txt' leído con la clase Lector
        """
        salida = []
        with open(self.ubicacion_archivo, encoding=encoding) as fp:
            linea = fp.readline()
            while linea:
                try:
                    salida.append(linea.strip())
                    linea = fp.readline()
                except BaseException:
                    continue
        return '\n'.join(salida)

    def leer_word(self, por_paginas, extraer_medios, dir_medios):
        """ Se lleva a cabo la lectura del texto de archivos con extensión '.docx' o '.doc'

        :param por_paginas: (bool) {True, False}. Especifica si se desea extraer el texto del \
            archivo Word con separador de páginas. Este separador se encuentra como '|**|' \
            dentro del texto extraído.
        :param extraer_medios: (bool) {True, False}. Especifica si se desean extraer las \
            imágenes dentro del archivo de Word para ser guardadas aparte como archivos \
            de imágenes. Funciona únicamente para archivos '.docx' (no '.doc') y si el \
            parámetro 'por_paginas' es False.
        :param dir_medios: (string)- Ruta de la carpeta donde se guardan las imágenes del \
            archivo Word cuyas imágenes se extrajeron (se especificó \
            extraer_medios = True)
        :return: (string). Texto del archivo '.docx' o '.doc' leído con la clase Lector
        """
        if por_paginas:
            from auxiliares import word_a_pdf
            # El atributo 'ubicacion_archivo' se va a cambiar
            # temporalmente, por lo que se guarda el valor original.
            temp = self.ubicacion_archivo
            archivo_pdf = word_a_pdf(self.ubicacion_archivo)
            if archivo_pdf is None:
                print('No se pudo convertir el documento Word a PDF, por lo que se retornará el texto completo y no por páginas.')
            else:
                self.establecer_ubicacion(archivo_pdf)
                paginas = self.leer_pdf(por_paginas, False, 0, '', 0, 0)
                # Volver a establecer la ubicacion de archivo original
                self.establecer_ubicacion(temp)
                # Borrar el archivo PDF creado temporalmente
                os.remove(archivo_pdf)
                return paginas
        import docx2txt
        if extraer_medios is False:
            texto = docx2txt.process(self.ubicacion_archivo)
        else:
            verify_create_dir(dir_medios)
            texto = docx2txt.process(self.ubicacion_archivo, dir_medios)
        return texto

    def leer_pdf(self, por_paginas, ocr, preprocesamiento, lenguaje, oem, psm, password=None):
        """ Se lleva a cabo la lectura del texto de archivos con extensión '.pdf'

        :param por_paginas: (bool) {True, False}. Especifica si se desea extraer el texto del \
            archivo Word con separador de páginas. Este separador se encuentra como '|**|' \
            dentro del texto extraído.
        :param ocr: (bool) {True, False}. Especifica si se desea utilizar reconocimiento \
            óptico de caracteres sobre el archivo cuyo texto se quiere extraer. Se utiliza \
            usualmente cuando el archivo es una imagen o documento escaneado
        :param preprocesamiento: (int) {1,2,3,4,5}. Especifica el nivel de preprocesamiento \
            que se lleva a cabo antes de extraer el texto del archivo. Aplica cuando se utiliza \
            reconocimiento óptico de caracteres (parámetro ocr es True). Las opciones son las siguientes: \
             |ul| 
             |li| 1: se convierte la imagen a escala de grises. |/li| 
             |li| 2: se convierte la imagen a escala de grises y se aplica blurring. |/li| 
             |li| 3: se convierte la imagen a escala de grises y se aplica el umbral de imagen con el \
                 método de OTSU. |/li| 
             |li| 4: se endereza el texto, se convierte la imagen a escala de grises y se aplica umbral \
                adaptativo. |/li| 
             |li| 5: se endereza el texto, se convierte la imagen a escala de grises, se aplica umbral \
                de imagen con el método de OTSU, blurring y umbral adaptativo. |/li| 
             |/ul| 
        :param lenguaje: (string). {'spa', 'eng'}  Se define el \
            lenguaje del texto que se desea extraer. Aplica cuando se utilia reconocimiento \
            óptico de caracteres (el parámetro ocr es True). Tiene las opciones de los lenguajes\
            que se descargan de la página de Tesseract. por ejemplo: español ('spa') e inglés ('eng')
        :param oem: (int) OEM hace referencia al modo del motor OCR (OCR engine mode \
            en inglés). Para mayor información consultar la sección de \ 
            :ref:`OCR <seccion_ocr>`.
        :param psm: (int) PSM hace referencia a los modos de segmentación de las páginas \ 
            (page segmentation modes, en inglés) de la librería Pytesseract. Para mayor \ 
            información consultar la sección de :ref:`OCR <seccion_ocr>`.
        :return: (string). Texto del archivo '.pdf' leído con la clase Lector
            """
        if ocr:
            from utils.ocr import OCR
            recog = OCR(preprocesamiento, lenguaje, oem, psm)
            paginas = recog.pdf_a_texto(self.ubicacion_archivo)
        else:
            try:
                from utils.auxiliares import leer_pdf_slate
                paginas = leer_pdf_slate(self.ubicacion_archivo, password)
            except:
                from utils.auxiliares import leer_pdf_pypdf
                paginas = leer_pdf_pypdf(self.ubicacion_archivo, password)
        # Se define la forma de retornar el texto
        if por_paginas:
            return paginas
        else:
            return ' '.join(paginas)

    def leer_rtf(self):
        """ Se lleva a cabo la lectura del texto de archivos con extensión '.rtf'

        :return: (string). Texto del archivo '.rtf' leído con la clase Lector
        """
        from utils.auxiliares import striprtf
        texto = []
        with open(self.ubicacion_archivo) as fp:
            linea = fp.readline()
            while linea:
                try:
                    texto.append(linea.strip())
                    linea = fp.readline()
                except BaseException:
                    continue
        texto = [striprtf(i) for i in texto]
        texto = ' '.join(texto)
        return texto

    def leer_imagen(self, preprocesamiento, lenguaje, oem, psm):
        """ Se lleva a cabo la lectura del texto de archivos de tipo imagen, con extensión 'png', 'jpg' o 'jpeg'

        :param preprocesamiento: (int) {1,2,3,4,5}. Especifica el nivel de preprocesamiento \
            que se lleva a cabo antes de extraer el texto del archivo. Aplica cuando se utiliza \
            reconocimiento óptico de caracteres (parámetro ocr es True). Las opciones son las siguientes: \
             |ul| 
             |li| 1: se convierte la imagen a escala de grises. |/li| 
             |li| 2: se convierte la imagen a escala de grises y se aplica blurring. |/li| 
             |li| 3: se convierte la imagen a escala de grises y se aplica el umbral de imagen con el método de OTSU. |/li| 
             |li| 4: se endereza el texto, se convierte la imagen a escala de grises y se aplica umbral adaptativo. |/li| 
             |li| 5: se endereza el texto, se convierte la imagen a escala de grises, se aplica umbral de imagen con el método de OTSU, blurring y umbral adaptativo. |/li| 
             |/ul| 
        :param lenguaje: (string). {'spa', 'eng'}  Se define el lenguaje del texto que se desea extraer. \
            Tiene las opciones de los lenguajes que se descargan de la página de Tesseract. por ejemplo: español ('spa') e inglés ('eng')
        :param oem: (int) OEM hace referencia al modo del motor OCR (OCR engine mode \
            en inglés). Para mayor información consultar la sección de :ref:`OCR <seccion_ocr>`.
        :param psm: (int) PSM hace referencia a los modos de segmentación de las páginas \
            (page segmentation modes, en inglés) de la librería Pytesseract. Para mayor \ 
            información consultar la sección de :ref:`OCR <seccion_ocr>`.
        :return: (string). Texto del archivo tipo imagen leído con la clase Lector
        """
        from utils.ocr import OCR
        recog = OCR(preprocesamiento, lenguaje, oem, psm)
        texto = recog.imagen_a_texto(self.ubicacion_archivo)
        return texto

    def archivo_a_texto(
            self,
            tipo='inferir',
            extraer_medios=False,
            dir_medios="temp/img_dir/",
            por_paginas=False,
            encoding="utf-8",
            ocr=False,
            preprocesamiento=3,
            lenguaje='spa',
            oem=2,
            psm=3,
            password=None):

        """ Se lleva a cabo la lectura del texto de un archivo y permite escoger el tipo, si es por páginas, \
            la codificación, si se utiliza OCR, el tipo de preprocesamiento, entre otros. 

        :param tipo: (string) {'inferir', 'txt', 'csv', 'pdf', 'rtf', 'doc', 'docx', 'npg', \
            'jpg', 'jpeg'} Valor por defecto: 'inferir'. Se define el tipo (o extensión) del \
            archivo que se desea leer
        :param extraer_medios: (bool) {True, False}. Valor por defecto: False. Especifica si se desean extraer las \
            imágenes dentro del archivo de Word para ser guardadas aparte como archivos \
            de imágenes. Funciona únicamente para archivos '.docx' (no '.doc') y si el \
            parámetro 'por_paginas' es False.
        :param dir_medios: (string). Valor por defecto: 'temp/img_dir/' Ruta de la carpeta \
            donde se guardan las imágenes del archivo Word cuyas imágenes se extrajeron (se especificó \
            extraer_medios = True)
        :param por_paginas: (bool) {True, False}. Valor por defecto: False. Se define si se \
            desea extraer el texto por páginas. 
        :param encoding: (string). Valor por defecto: 'utf-8'. Especifica la codificación \
            del texto que se desea leer
        :param ocr: (bool) {True, False}. Valor por defecto: False Especifica si se desea utilizar reconocimiento \
            óptico de caracteres sobre el archivo cuyo texto se quiere extraer. Se utiliza \
            usualmente cuando el archivo es una imagen o documento escaneado
        :param preprocesamiento: (int) {1,2,3,4,5}. Valor por defecto: 3 Especifica el nivel de preprocesamiento \
            que se lleva a cabo antes de extraer el texto del archivo. Aplica cuando se utiliza \
            reconocimiento óptico de caracteres (parámetro ocr es True). Las opciones son las siguientes: \
             |ul| 
             |li| 1: se convierte la imagen a escala de grises. |/li| 
             |li| 2: se convierte la imagen a escala de grises y se aplica blurring. |/li| 
             |li| 3: se convierte la imagen a escala de grises y se aplica el umbral de imagen con el método de OTSU. |/li| 
             |li| 4: se endereza el texto, se convierte la imagen a escala de grises y se aplica umbral adaptativo. |/li| 
             |li| 5: se endereza el texto, se convierte la imagen a escala de grises, se aplica umbral de imagen con el método de OTSU, blurring y umbral adaptativo. |/li| 
             |/ul| 
        :param lenguaje: (string). {'spa', 'eng'}. Valor por defecto: 'spa'  Tiene las opciones de los lenguajes que se descargan \
            de la página de Tesseract. por ejemplo: español ('spa') e inglés ('eng'). Aplica cuando se extrae el texto de \
            imágenes o archivos escaneados
        :param oem: (int) Valor por defecto: 2. OEM hace referencia al modo del motor OCR (OCR engine mode \
            en inglés). Para mayor información consultar la sección de :ref:`OCR <seccion_ocr>`.
        :param psm: (int) Valor por defecto: 3 PSM hace referencia a los modos de segmentación \ 
            de las páginas (page segmentation modes, en inglés) de la librería Pytesseract. \ 
            Para mayor información consultar la sección de :ref:`OCR <seccion_ocr>`.
        :param password: (string). Valor por defecto: None. Contraseña del archivo cuyo texto se desea \
            extraer, en caso de requerirlo
        :return: (string). Texto extraído del archivo con la clase Lector            
        """
        tipo = tipo.lower()
        if tipo == 'inferir':
            tipo = self.ubicacion_archivo.split('.')[-1].lower()
        if tipo in ['txt', 'csv']:
            salida = self.leer_txt(encoding)
        elif tipo == 'pdf':
            salida = self.leer_pdf(por_paginas, ocr, preprocesamiento, lenguaje, oem, psm, password)
        elif tipo == 'rtf':
            salida = self.leer_rtf()
        elif tipo in ['doc', 'docx']:
            salida = self.leer_word(por_paginas, extraer_medios, dir_medios)
        elif tipo in ['png', 'jpg', 'jpeg']:
            return self.leer_imagen(preprocesamiento, lenguaje, oem, psm)
        else:
            print(
                'Formato desconocido. Por favor ingrese un archivo en formato adecuado.')
            return None
        # Quitar caracteres extraños de los archivos
        if salida is None:
            return None
        elif isinstance(salida, str):
            return adecuar_xml(salida)
        else:
            return [adecuar_xml(i) for i in salida]

# Función que encapsula el proceso de lectura de archivos de texto

def leer_texto(
        ubicacion_archivo,
        tipo='inferir',
        extraer_medios=False,
        dir_medios="temp/img_dir/",
        por_paginas=False,
        encoding="utf-8",
        ocr=False,
        preprocesamiento=3,
        lenguaje='spa',
        oem=2,
        psm=3, 
        password=None):        
    """ Función que se encarga de extraer el texto de un archivo. Permite especificar la ruta del archivo, \
        escoger el tipo, si es por páginas, la codificación, si se utiliza OCR, el tipo de preprocesamiento, entre otros. 

    :param ubicacion_archivo: (string). Ruta del archivo que se desea leer
    :param tipo: (string) {'inferir', 'txt', 'csv', 'pdf', 'rtf', 'doc', 'docx', 'npg', \
        'jpg', 'jpeg'} Valor por defecto: 'inferir'. Se define el tipo (o extensión) del \
        archivo que se desea leer
    :param extraer_medios: (bool) {True, False}. Valor por defecto: False. Especifica si se desean extraer las \
        imágenes dentro del archivo de Word para ser guardadas aparte como archivos \
        de imágenes. Funciona únicamente para archivos '.docx' (no '.doc') y si el \
        parámetro 'por_paginas' es False.
    :param dir_medios: (string). Valor por defecto: 'temp/img_dir/' Ruta de la carpeta \
        donde se guardan las imágenes del archivo Word cuyas imágenes se extrajeron (se especificó \
        extraer_medios = True)
    :param por_paginas: (bool) {True, False}. Valor por defecto: False. Se define si se \
        desea extraer el texto por páginas. 
    :param encoding: (string). Valor por defecto: 'utf-8'. Especifica la codificación \
        del texto que se desea leer
    :param ocr: (bool) {True, False}. Valor por defecto: False Especifica si se desea utilizar reconocimiento \
        óptico de caracteres sobre el archivo cuyo texto se quiere extraer. Se utiliza \
        usualmente cuando el archivo es una imagen o documento escaneado
    :param preprocesamiento: (int) {1,2,3,4,5}. Valor por defecto: 3 Especifica el nivel de preprocesamiento \
        que se lleva a cabo antes de extraer el texto del archivo. Aplica cuando se utiliza \
        reconocimiento óptico de caracteres (parámetro ocr es True). Las opciones son las siguientes: \
         |ul| 
         |li| 1: se convierte la imagen a escala de grises. |/li| 
         |li| 2: se convierte la imagen a escala de grises y se aplica blurring. |/li| 
         |li| 3: se convierte la imagen a escala de grises y se aplica el umbral de imagen con el método de OTSU. |/li| 
         |li| 4: se endereza el texto, se convierte la imagen a escala de grises y se aplica umbral adaptativo. |/li| 
         |li| 5: se endereza el texto, se convierte la imagen a escala de grises, se aplica umbral de imagen con el método de OTSU, blurring y umbral adaptativo. |/li| 
         |/ul| 
    :param lenguaje: (string). {'spa', 'eng'}. Valor por defecto: 'spa'  Se define el lenguaje del texto que se desea extraer. \
        Tiene las opciones de los lenguajes que se descargan de la página de Tesseract. por ejemplo: español ('spa') e inglés \
        ('eng'). Aplica cuando se extrae el texto de \
        imágenes o archivos escaneados
    :param oem: (int) Valor por defecto: 2. OEM hace referencia al modo del motor OCR (OCR engine mode \
        en inglés). Para mayor información consultar la sección de  :ref:`OCR <seccion_ocr>`.
    :param psm: (int) Valor por defecto: 3 PSM hace referencia a los modos de segmentación \ 
        de las páginas (page segmentation modes, en inglés) de la librería Pytesseract. \ 
        Para mayor información consultar la sección de :ref:`OCR <seccion_ocr>`.
    :param password: (string). Valor por defecto: None. Contraseña del archivo cuyo texto se desea \
        extraer, en caso de requerirlo
    :return: (string). Texto extraído del archivo especificado con la función 'leer_texto'
    """
    le = Lector(ubicacion_archivo)
    return le.archivo_a_texto(
        tipo,
        extraer_medios,
        dir_medios,
        por_paginas,
        encoding,
        ocr,
        preprocesamiento,
        lenguaje,
        oem,
        psm,
        password)
