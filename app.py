import os
import subprocess
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
import re

cm = 28.35

# COLOCAR ACA LA MEDIDA EN CM, EJEMPLO 10 = 10 CM
WIDTH_GLOBAL = 10 *  cm
HEIGHT_GLOBAL = 15 *  cm

def getFontsInFolder(folder_path):
    """
    Obtiene las fuentes en una carpeta y devuelve un diccionario donde las claves son los nombres
    de las fuentes (sin la extensión) y los valores son las rutas completas a los archivos de fuente.

    Args:
        folder_path (str): Ruta de la carpeta donde se buscarán las fuentes.

    Returns:
        dict: Diccionario de fuentes encontradas en la carpeta.
    """
    fonts = {}
    extensions = ['.ttf', '.otf']

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() in extensions:
            font_name = os.path.splitext(file_name)[0]
            fonts[font_name] = file_path

    return fonts

def registerFonts(fonts):
    """
    Registra una lista de fuentes con el reportlab library usando el objeto Canvas proporcionado.

    Args:
        can (canvas.Canvas): El objeto de lienzo (canvas) en el que se registrarán las fuentes.
        fonts (dict): Un diccionario donde las claves son los nombres de las fuentes
                      y los valores son las rutas a los archivos de fuente correspondientes.
                      Ejemplo: {'Montserrat-Bold': 'path/to/Montserrat-Bold.ttf',
                                'Arial': 'path/to/Arial.ttf'}
    """
    # Registrar las fuentes
    for font_name, font_path in fonts.items():
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        
def create_pdf(ancho, alto, pdf_file):
    WIDTH, HEIGHT = portrait((ancho, alto))
    can = canvas.Canvas(pdf_file, pagesize=(WIDTH, HEIGHT))
    return WIDTH, HEIGHT, can

def cutText(text, characters_per_line):
    lines = []
    original_lines = text.split("\n")

    for line in original_lines:
        words = line.split()
        current_line = words[0]

        for word in words[1:]:
            if len(current_line) + len(word) + 1 <= characters_per_line:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

    return "\n".join(lines)

def split_text(text, n):
    words = text.split()
    result = []
    for i in range(0, len(words), n):
        result.append(' '.join(words[i:i+n]))
    return result

def removeBreak(text, n):
    lines = text.split("\n")
    modified_text = ""
    for i in range(len(lines)-n):
        if i % (n+1) == 0:
            modified_text += lines[i]
            for j in range(1, n+1):
                modified_text += " " + lines[i+j]
            modified_text += "\n"
    return modified_text



def write_text(canvas, x=0, y=0, texto="", nCut=0, paddingx=0, alignment="left", fontSize=8, font = "Helvetica", nBreak=0 ):
    y=HEIGHT_GLOBAL-y
    
    if (nBreak>0):
        texto=removeBreak(texto, nBreak)
        
    if (nCut>0 and texto!=""):
        
        texto=cutText(texto, nCut)
    
    
    
    lines= texto.split("\n")
    
    
    
    if alignment not in ["left", "right", "center"]:
        raise ValueError("La opción de alineación no es válida")
    
    for i, line in enumerate(lines):
        sizeFont_temp=fontSize
        while canvas.stringWidth(line, font, sizeFont_temp) > WIDTH_GLOBAL - paddingx:
            sizeFont_temp-=1
            
        if alignment == "left":
            x_position = x
        elif alignment == "right":
            x_position = WIDTH_GLOBAL - canvas.stringWidth(line, font, sizeFont_temp) - x
        elif alignment == "center":
            x_position = x + (WIDTH_GLOBAL - canvas.stringWidth(line, font, sizeFont_temp)) / 2
            
        canvas.setFont(font, sizeFont_temp)
        canvas.drawString(x_position, y - ((i+1)*fontSize)*1.2, line)

def extract_lines(text_list, search_text, startIndex=0, endIndex=0, textBreak=""):
    for i, line in enumerate(text_list):
        if search_text in line:
            start_index = i + startIndex
            
            if endIndex == 0:
                selected_lines = text_list[start_index:]
            else:
                selected_lines = text_list[start_index:start_index + endIndex]
            
            try:
                text_break_index = selected_lines.index(textBreak)
                selected_lines = selected_lines[:text_break_index]
            except ValueError:
                pass 
            
            return selected_lines
    return []


def list_to_text(lst):
    return '\n'.join(lst)


def main():
    
    #doc = fitz.open('aa.pdf')
    #text = ""
    #first page
    #text = doc[0].get_text()
    
    
    doc = fitz.open('aa.pdf')
    text = ""
    
    pdfName = 'a.pdf'
    WIDTH, HEIGHT, can = create_pdf(WIDTH_GLOBAL, HEIGHT_GLOBAL, pdfName)
    
    for page in doc:
        text = page.get_text()
        cleaned_text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ:\s\d]', '', text)
        text_list = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
        
       
        #agregar fuentes
        folder_path = 'fonts' 
        fonts = getFontsInFolder(folder_path)
        registerFonts( fonts=fonts)
        
        #logo
        write_text(canvas=can, x=30, y=20, texto="Quanta", alignment="right", font="Montserrat-Bold", fontSize=11)

        #Remitente
        write_text(canvas=can,
                x=20,
                y=20+15,
                texto="Remitente:",
                fontSize=10,
                font="Helvetica-Bold")
        write_text(canvas=can,
                x=20,
                y=23+12+15,
                texto="OSCORP TECHNOLOGY SA\nAv. Carlos Antonio Lopez NRO. 7303 CASI Cañada del Carmen\nCIUDAD DEL ESTE - PARAGUAY\nTELEF: (061) 505 762",
                fontSize=8,
                font="Helvetica")
               
        #Entrega
        linesSearch = extract_lines(text_list, search_text="DESTINATARIO",startIndex=1, endIndex=5, textBreak="A")
        textClean = list_to_text(linesSearch)
        write_text(canvas=can,
                x=20,
                y=55+20+40,
                texto="Entrega:",
                fontSize=10,
                font="Helvetica-Bold")
        write_text(canvas=can, 
                x=20, 
                y=55+35+40, 
                texto=textClean,
                nCut=40, 
                paddingx=30,
                alignment="left",
                fontSize=8,
                font="Helvetica")
        
        #referencias
        linesSearch = extract_lines(text_list, search_text="ENTREGA  Indicaciones",startIndex=0, textBreak="Flete")
        textClean = list_to_text(linesSearch)
        write_text(canvas=can, 
                x=20, 
                y=55+83+40, 
                texto=textClean, 
                paddingx=30,
                alignment="left",
                fontSize=8,
                font="Helvetica-Bold",
                nCut=63)
        print (linesSearch)
        
        #Detalles del envio
        linesSearch = extract_lines(text_list, search_text="DETALLES DEL ENVIO",startIndex=1, textBreak="RESUMEN DE LA CARGA",)
        textClean = list_to_text(linesSearch)
        write_text(canvas=can,
                x=20,
                y=200+20,
                texto="Detalles del envio:",
                fontSize=10,
                font="Helvetica-Bold")
        write_text(canvas=can, 
                x=20, 
                y=140+35+60, 
                texto=textClean,
                paddingx=30,
                alignment="left",
                fontSize=8,
                font="Helvetica",
                nBreak=1)
        
        #Valor declarado
        linesSearch = extract_lines(text_list, search_text="VALOR DECLARADO",endIndex=2,)
        textClean = list_to_text(linesSearch)
        
        write_text(canvas=can,
                y=350,
                texto=textClean,
                fontSize=10,
                font="Helvetica-Bold",
                alignment="center")
        
        
        #pasar a la siguiente pagina 
        can.showPage()
        
    can.save()  
    subprocess.Popen(["a.pdf"], shell=True)
        







if __name__ == '__main__':
    
    main()
        
        