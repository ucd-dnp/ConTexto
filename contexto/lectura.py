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

        :param ubicacion_archivo:
        """
        self.establecer_ubicacion(ubicacion_archivo)

    def establecer_ubicacion(self, ubicacion_archivo):
        """

        :param ubicacion_archivo:
        :return:
        """
        self.ubicacion_archivo = ubicacion_archivo

    def leer_txt(self, encoding="utf-8"):
        """

        :param encoding:
        :return:
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
        """

        :param extraer_medios:
        :param dir_medios:
        :return:
        """
        if por_paginas:
            from auxiliares import word_a_pdf
            # El atributo 'ubicacion_archivo' se va a cambiar
            # temporalmente, por lo que se guarda el valor original.
            temp = self.ubicacion_archivo
            archivo_pdf = word_a_pdf(self.ubicacion_archivo)
            if archivo_pdf is None:
                print('No se pudo convertir el documento Word a PDF. intente leer el archivo completo (por_paginas=False)')
                return None
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
        """

            :param por_paginas:
            :param ocr:
            :param preprocesamiento:
            :param lenguaje:
            :param oem:
            :param psm:
            :return:
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
        """

        :return:
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
        """

        :param preprocesamiento:
        :param lenguaje:
        :param oem:
        :param psm:
        :return:
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
        if tipo == 'inferir':
            tipo = self.ubicacion_archivo.split('.')[-1]
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
        if por_paginas:
            return [adecuar_xml(i) for i in salida]
        else:
            return adecuar_xml(salida)

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
    """

    :param ubicacion_archivo:
    :param tipo:
    :param extraer_medios:
    :param dir_medios:
    :param por_paginas:
    :param encoding:
    :param ocr:
    :param preprocesamiento:
    :param lenguaje:
    :param oem:
    :param psm:
    :return:
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
