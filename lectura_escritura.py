'''
Código, funciones y clases relacionadas a la carga y lectura de
diferentes tipos de archivo (word, txt, rtf, pdf inicialmente).
'''
from utils.helper import verify_create_dir

# prueba
# Clase lector


class Lector():
    def __init__(self, ubicacion_archivo):
        self.definir_ubicacion(ubicacion_archivo)

    def definir_ubicacion(self, ubicacion_archivo):
        self.file_path = ubicacion_archivo

    def read_txt(self, encoding="utf-8"):
        out = []
        with open(self.file_path, encoding=encoding) as fp:
            line = fp.readline()
            while line:
                try:
                    out.append(line.strip())
                    line = fp.readline()
                except BaseException:
                    continue
        return '\n'.join(out)

    def read_word(self, extraer_medios, dir_medios):
        import docx2txt
        if extraer_medios is False:
            texto = docx2txt.process(self.file_path)
        else:
            verify_create_dir(dir_medios)
            texto = docx2txt.process(self.file_path, dir_medios)
        return texto

    def read_pdf(self, por_paginas, ocr, preprocess, lang, oem, psm):
        if ocr:
            from utils.ocr import OCR
            recog = OCR(preprocess, lang, oem, psm)
            paginas = recog.pdf2text(self.file_path)
        else:
            import PyPDF2
            # Función para prevenir errores

            def leer_pag(reader, pag):
                try:
                    return reader.getPage(pag).extractText()
                except BaseException:
                    return ''
            pdf_file = open(self.file_path, 'rb')
            # reader = PyPDF2.PdfFileReader(pdf_file)
            reader = PyPDF2.PdfFileReader(pdf_file, strict=False)
            number_of_pages = reader.getNumPages()
            paginas = [leer_pag(reader, i) for i in range(number_of_pages)]
            pdf_file.close()
        if por_paginas:
            return paginas
        else:
            return ' '.join(paginas)

    def read_rtf(self):
        from .utils.helper import striprtf
        text = []
        with open(self.file_path) as fp:
            line = fp.readline()
            while line:
                try:
                    text.append(line.strip())
                    line = fp.readline()
                except BaseException:
                    continue
        text = [striprtf(i) for i in text]
        texto = ' '.join(text)
        return texto

    def read_image(self, preprocess, lang, oem, psm):
        from .utils.ocr import OCR
        recog = OCR(preprocess, lang, oem, psm)
        texto = recog.image2text(self.file_path)
        return texto

    def archivo_a_texto(
            self,
            tipo='inferir',
            extraer_medios=False,
            dir_medios="temp/img_dir/",
            por_paginas=False,
            encoding="utf-8",
            ocr=False,
            preprocess=4,
            lang='spa',
            oem=2,
            psm=3):
        if tipo == 'inferir':
            tipo = self.file_path.split('.')[-1]
        if tipo in ['txt', 'csv']:
            return self.read_txt(encoding)
        elif tipo == 'pdf':
            return self.read_pdf(por_paginas, ocr, preprocess, lang, oem, psm)
        elif tipo == 'rtf':
            return self.read_rtf()
        elif tipo in ['doc', 'docx']:
            return self.read_word(extraer_medios, dir_medios)
        elif tipo in ['png', 'jpg', 'jpeg']:
            return self.read_image(preprocess, lang, oem, psm)
        else:
            print(
                'Formato desconocido. Por favor ingrese un archivo en formato adecuado.')
            return None

# Clase escritor


class Escritor():
    def __init__(self, ubicacion_archivo, texto):
        self.definir_ubicacion(ubicacion_archivo)
        self.definir_texto(texto)

    def definir_ubicacion(self, ubicacion_archivo):
        self.file_path = ubicacion_archivo

    def definir_texto(self, texto):
        self.txt = texto

    def write_txt(self):
        if isinstance(self.txt, list):
            self.txt = '\n\n|**|\n\n'.join(self.txt)
        # with open(self.file_path, 'w') as fp:
        with open(self.file_path, 'w', encoding="utf-8") as fp:

            fp.write(self.txt)

    def write_word(self):
        from docx import Document
        document = Document()
        if isinstance(self.txt, list):
            for i, page in enumerate(self.txt):
                document.add_paragraph(page)
                if i < len(self.txt) - 1:
                    document.add_page_break()
        else:
            document.add_paragraph(self.txt)
        document.save(self.file_path)

    def write_pdf(self):
        import PyPDF2
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        from textwrap import wrap

        def write_page(text):
            text = text.split('\n')
            temp = BytesIO()
            can = canvas.Canvas(temp, pagesize=letter)
            t = can.beginText()
            t.setFont('Helvetica-Bold', 7)
            t.setCharSpace(0)
            t.setTextOrigin(50, 700)
            for line in text:
                sublines = wrap(line, 150)
                if len(sublines) > 0:
                    for subline in sublines:
                        t.textLine(subline)
                else:
                    t.textLine('')
            can.drawText(t)
            # can.drawString(5, 550, text)
            can.save()
            temp.seek(0)
            lector = PyPDF2.PdfFileReader(temp)
            return lector
        salida = PyPDF2.PdfFileWriter()
        if isinstance(self.txt, list):
            for page in self.txt:
                lector = write_page(page)
                salida.addPage(lector.getPage(0))
        else:
            lector = write_page(self.txt)
            salida.addPage(lector.getPage(0))
        with open(self.file_path, 'wb') as fp:
            salida.write(fp)

    def texto_a_archivo(self, tipo='inferir'):
        if tipo == 'inferir':
            tipo = self.file_path.split('.')[-1]
        if tipo in ['txt', 'csv']:
            self.write_txt()
        elif tipo == 'pdf':
            self.write_pdf()
        elif tipo in ['doc', 'docx']:
            self.write_word()
        else:
            print('Formato desconocido. Se escribirá en un formato plano (.txt).')
            nueva_ruta = ''.join(self.file_path.split(
                '.')[:-1]) + '_{}.txt'.format(tipo)
            self.definir_ubicacion(nueva_ruta)
            self.write_txt()


# Funciones que encapsulan el proceso de lectura y escritura de archivos
# de texto

def leer_texto(
        ubicacion_archivo,
        tipo='inferir',
        extraer_medios=False,
        dir_medios="temp/img_dir/",
        por_paginas=False,
        encoding="utf-8",
        ocr=False,
        preprocess=4,
        lang='spa',
        oem=2,
        psm=3):
    le = Lector(ubicacion_archivo)
    return le.archivo_a_texto(
        tipo,
        extraer_medios,
        dir_medios,
        por_paginas,
        encoding,
        ocr,
        preprocess,
        lang,
        oem,
        psm)


def escribir_texto(ubicacion_archivo, texto, tipo='inferir'):
    es = Escritor(ubicacion_archivo, texto)
    es.texto_a_archivo(tipo)
