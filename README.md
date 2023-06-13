# Extractor y escritor de texto en PDF

Este es un script de Python que utiliza varias bibliotecas para extraer texto de un archivo PDF y escribirlo en un nuevo archivo PDF. El script está diseñado para procesar un archivo PDF y generar un nuevo archivo PDF con información específica extraída del original.

## Requisitos previos
Asegúrate de tener Python instalado en tu sistema, preferiblemente Python 3.7 o superior.

Además, necesitarás instalar las siguientes bibliotecas de Python:
- reportlab
- PyMuPDF

Puedes instalar estas bibliotecas utilizando el siguiente comando:

```bash
pip install reportlab PyMuPDF
```
Uso
Crea una carpeta llamada "fonts" en el mismo directorio que el script app.py.
Coloca tus archivos de fuente (fuentes TrueType o OpenType) en la carpeta "fonts".
Abre una ventana de línea de comandos (CMD).
Navega hasta el directorio donde se encuentra el archivo app.py.
Ejecuta el siguiente comando:
python app.py "ruta_del_pdf"
Reemplaza "ruta_del_pdf" con la ruta del archivo PDF del cual deseas extraer el texto y escribirlo en un nuevo archivo PDF.
Ejemplo
python app.py "test.pdf"

Este ejemplo ejecutará el script utilizando el archivo aa.pdf como entrada.

Notas
Asegúrate de que el archivo PDF exista y tenga permisos de lectura.
Asegúrate de tener los archivos de fuente correspondientes en la carpeta "fonts".
El archivo de salida se creará en el mismo directorio que el archivo de entrada y se llamará ruta_del_pdf_cut.pdf.
Si el archivo de salida ya existe, se sobrescribirá sin previo aviso.
¡Disfruta utilizando el script para extraer y escribir texto en archivos PDF! Si tienes alguna pregunta o problema, no dudes en contactarme.
