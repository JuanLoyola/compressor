from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfWriter, PdfReader

# Creamos la intancia y ubicamos el folder que contiene el template
app = Flask(__name__,template_folder='templates')

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Definimos una función para verificar si la extensión del archivo es permitida.
def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Definimos la funcion para leer, comprimir y recorrer las paginas del .PDF
def compress_pdf(input_path, output_path):
    
    input_pdf = PdfReader(open(input_path, "rb"))
    output_pdf = PdfWriter()

    # Seteamos las paginas
    num_pages = len(input_pdf.pages)

    # Iteramos cada pagina
    for page_number in range(num_pages):
        page = input_pdf.pages[page_number]
        output_pdf.add_page(page)
        
    # Revisamos si existe folder descargas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Guardamos el pdf comprimido
    with open(output_path, "wb") as f:
        output_pdf.write(f)

@app.route('/', methods=['GET', 'POST'])


# Al subir un pdf lo guardamosy luego lo comprimimos. Devolvemos el archivo comprimido como una descarga
def upload_file():
    
    if request.method == 'POST':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        
        if file and allowed_file(file.filename):
            filename = file.filename
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'compressed_' + filename)
            
            compress_pdf(input_path, output_path)
            return send_file(output_path, as_attachment=True)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
