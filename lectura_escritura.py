'''Código, funciones y clases relacionadas a la carga y lectura de diferentes tipos de archivo (word, txt, rtf, pdf inicialmente).'''
import re
from utils import verify_create_dir

class Lector():
    def __init__(self, ubicacion_archivo):
        self.definir_ubicacion(ubicacion_archivo)
    def definir_ubicacion(self, ubicacion_archivo):
            self.file_path = ubicacion_archivo
    def read_txt(self):
        out = []
        with open(self.file_path) as fp:  
            line = fp.readline()
            while line:
                try:
                    out.append(line.strip())
                    line = fp.readline()
                except:
                    continue
        return ' '.join(out)
    def read_word(self, extraer_medios, dir_medios):
        import docx2txt
        if extraer_medios is False:
            texto = docx2txt.process(self.file_path)
        else:
            verify_create_dir(dir_medios) 
            texto = docx2txt.process(self.file_path, dir_medios)
        return texto
    def read_pdf(self, por_paginas, ocr, preprocess):
        if ocr:
            from ocr import OCR
            recog = OCR(preprocess)
            paginas = recog.pdf2text(self.file_path)
        else:
            import PyPDF2
            pdf_file = open(self.file_path, 'rb')
            reader = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = reader.getNumPages()
            paginas = [reader.getPage(i).extractText() for i in range(number_of_pages)]
            pdf_file.close()
        if por_paginas:
            return paginas
        else:
            return ' '.join(paginas)
    def read_rtf(self):
        text = []
        with open(self.file_path) as fp:  
            line = fp.readline()
            while line:
                try:
                    text.append(line.strip())
                    line = fp.readline()
                except:
                    continue
        text = [striprtf(i) for i in text]
        texto = ' '.join(text)
        return texto
    def read_image(self, preprocess):
        from ocr import OCR
        recog = OCR(preprocess)
        texto = recog.image2text(self.file_path)
        return texto
    def archivo_a_texto(self, tipo='inferir', extraer_medios=False, dir_medios="temp/img_dir/", por_paginas=False, ocr=False, preprocess=True):
        if tipo == 'inferir':
            tipo = self.file_path.split('.')[-1]
        if tipo in ['txt','csv']:
            return self.read_txt()
        elif tipo == 'pdf':
            return self.read_pdf(por_paginas, ocr, preprocess)
        elif tipo =='rtf':
            return self.read_rtf()
        elif tipo in ['doc', 'docx']:
            return self.read_word(extraer_medios, dir_medios)
        elif tipo in ['png','jpg','jpeg']:
            return self.read_image(preprocess)
        else:
            print('Formato desconocido. Por favor ingrese un archivo en formato adecuado.')
            return None

class Escritor():
    def __init__(self, ubicacion_archivo, texto):
        self.definir_ubicacion(ubicacion_archivo)
        self.definir_texto(texto)
    def definir_ubicacion(self, ubicacion_archivo):
        self.file_path = ubicacion_archivo
    def definir_texto(self, texto):
        self.txt = texto
    def write_txt(self):
        if type(self.txt) == list:
            self.txt = '\n\n|**|\n\n'.join(self.txt)
        with open(self.file_path, 'w') as fp:
            fp.write(self.txt)
    def write_word(self):
        from docx import Document
        document = Document()
        if type(self.txt) == list:
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
        if type(self.txt) == list:
            for page in self.txt:
                lector = write_page(page)
                salida.addPage(lector.getPage(0))
        else:
            lector = write_page(a[0])
            lector = write_page(self.txt)
            salida.addPage(lector.getPage(0))
        with open(self.file_path, 'wb') as fp:
            salida.write(fp)
    def texto_a_archivo(self, tipo='inferir'):
        if tipo == 'inferir':
            tipo = self.file_path.split('.')[-1]
        if tipo in ['txt','csv']:
            return self.read_txt()
        elif tipo == 'pdf':
            return self.read_pdf(por_paginas, ocr, thresh, blur)
        elif tipo =='rtf':
            return self.read_rtf()
        elif tipo in ['doc', 'docx']:
            return self.read_word(extraer_medios, dir_medios)
        elif tipo in ['png','jpg','jpeg']:
            return self.read_image(thresh, blur)
        else:
            print('Formato desconocido. Por favor ingrese un archivo en formato adecuado.')
            return None

# Función para pasar de texto enriquecido a texto plano
def striprtf(text):
    """
    Extract text in RTF Files. Refactored to use with Python 3.x
    Source:
        http://stackoverflow.com/a/188877
    Code created by Markus Jarderot: http://mizardx.blogspot.com
    """
    pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
   # control words which specify a "destionation".
    destinations = frozenset((
      'aftncn','aftnsep','aftnsepc','annotation','atnauthor','atndate','atnicn','atnid',
      'atnparent','atnref','atntime','atrfend','atrfstart','author','background',
      'bkmkend','bkmkstart','blipuid','buptim','category','colorschememapping',
      'colortbl','comment','company','creatim','datafield','datastore','defchp','defpap',
      'do','doccomm','docvar','dptxbxtext','ebcend','ebcstart','factoidname','falt',
      'fchars','ffdeftext','ffentrymcr','ffexitmcr','ffformat','ffhelptext','ffl',
      'ffname','ffstattext','field','file','filetbl','fldinst','fldrslt','fldtype',
      'fname','fontemb','fontfile','fonttbl','footer','footerf','footerl','footerr',
      'footnote','formfield','ftncn','ftnsep','ftnsepc','g','generator','gridtbl',
      'header','headerf','headerl','headerr','hl','hlfr','hlinkbase','hlloc','hlsrc',
      'hsv','htmltag','info','keycode','keywords','latentstyles','lchars','levelnumbers',
      'leveltext','lfolevel','linkval','list','listlevel','listname','listoverride',
      'listoverridetable','listpicture','liststylename','listtable','listtext',
      'lsdlockedexcept','macc','maccPr','mailmerge','maln','malnScr','manager','margPr',
      'mbar','mbarPr','mbaseJc','mbegChr','mborderBox','mborderBoxPr','mbox','mboxPr',
      'mchr','mcount','mctrlPr','md','mdeg','mdegHide','mden','mdiff','mdPr','me',
      'mendChr','meqArr','meqArrPr','mf','mfName','mfPr','mfunc','mfuncPr','mgroupChr',
      'mgroupChrPr','mgrow','mhideBot','mhideLeft','mhideRight','mhideTop','mhtmltag',
      'mlim','mlimloc','mlimlow','mlimlowPr','mlimupp','mlimuppPr','mm','mmaddfieldname',
      'mmath','mmathPict','mmathPr','mmaxdist','mmc','mmcJc','mmconnectstr',
      'mmconnectstrdata','mmcPr','mmcs','mmdatasource','mmheadersource','mmmailsubject',
      'mmodso','mmodsofilter','mmodsofldmpdata','mmodsomappedname','mmodsoname',
      'mmodsorecipdata','mmodsosort','mmodsosrc','mmodsotable','mmodsoudl',
      'mmodsoudldata','mmodsouniquetag','mmPr','mmquery','mmr','mnary','mnaryPr',
      'mnoBreak','mnum','mobjDist','moMath','moMathPara','moMathParaPr','mopEmu',
      'mphant','mphantPr','mplcHide','mpos','mr','mrad','mradPr','mrPr','msepChr',
      'mshow','mshp','msPre','msPrePr','msSub','msSubPr','msSubSup','msSubSupPr','msSup',
      'msSupPr','mstrikeBLTR','mstrikeH','mstrikeTLBR','mstrikeV','msub','msubHide',
      'msup','msupHide','mtransp','mtype','mvertJc','mvfmf','mvfml','mvtof','mvtol',
      'mzeroAsc','mzeroDesc','mzeroWid','nesttableprops','nextfile','nonesttables',
      'objalias','objclass','objdata','object','objname','objsect','objtime','oldcprops',
      'oldpprops','oldsprops','oldtprops','oleclsid','operator','panose','password',
      'passwordhash','pgp','pgptbl','picprop','pict','pn','pnseclvl','pntext','pntxta',
      'pntxtb','printim','private','propname','protend','protstart','protusertbl','pxe',
      'result','revtbl','revtim','rsidtbl','rxe','shp','shpgrp','shpinst',
      'shppict','shprslt','shptxt','sn','sp','staticval','stylesheet','subject','sv',
      'svb','tc','template','themedata','title','txe','ud','upr','userprops',
      'wgrffmtfilter','windowcaption','writereservation','writereservhash','xe','xform',
      'xmlattrname','xmlattrvalue','xmlclose','xmlname','xmlnstbl',
      'xmlopen',
    ))
    # Translation of some special characters.
    specialchars = {
      'par': '\n',
      'sect': '\n\n',
      'page': '\n\n',
      'line': '\n',
      'tab': '\t',
      'emdash': '\u2014',
      'endash': '\u2013',
      'emspace': '\u2003',
      'enspace': '\u2002',
      'qmspace': '\u2005',
      'bullet': '\u2022',
      'lquote': '\u2018',
      'rquote': '\u2019',
      'ldblquote': '\201C',
      'rdblquote': '\u201D',
    }
    stack = []
    ignorable = False       # Whether this group (and all inside it) are "ignorable".
    ucskip = 1              # Number of ASCII characters to skip after a unicode character.
    curskip = 0             # Number of ASCII characters left to skip
    out = []                # Output buffer.
    #    for match in pattern.finditer(text.decode()):
    for match in pattern.finditer(text):
        word,arg,hex,char,brace,tchar = match.groups()
        if brace:
            curskip = 0
            if brace == '{':
                # Push state
                stack.append((ucskip,ignorable))
            elif brace == '}':
                # Pop state
                try:
                    ucskip,ignorable = stack.pop()
                except:
                    pass
        elif char: # \x (not a letter)
            curskip = 0
            if char == '~':
                if not ignorable:
                    out.append('\xA0')
            elif char in '{}\\':
                if not ignorable:
                    out.append(char)
            elif char == '*':
                ignorable = True
        elif word: # \foo
            curskip = 0
            if word in destinations:
                ignorable = True
            elif ignorable:
                pass
            elif word in specialchars:
                out.append(specialchars[word])
            elif word == 'uc':
                ucskip = int(arg)
            elif word == 'u':
                c = int(arg)
                if c < 0: 
                    c += 0x10000
                if c > 127: 
                    out.append(chr(c)) #NOQA
                else: 
                    out.append(chr(c))
                curskip = ucskip
        elif hex: # \'xx
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                c = int(hex,16)
                if c > 127:
                    out.append(chr(c)) #NOQA
                else:
                    out.append(chr(c))
        elif tchar:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(tchar)
    return ''.join(out)