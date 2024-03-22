from flask import Flask, render_template, request, send_file
import os
from ics import Calendar, Event

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def process_pdf(pdf_files):

    file_name = pdf_files[0].filename

    print(file_name)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFiles' not in request.files:
        return "No PDF files uploaded."
    
    pdf_files = request.files.getlist('pdfFiles')
    
    process_pdf(pdf_files)

    return render_template('index.html')

@app.route('/generate_ics', methods=['GET'])
def generate_ics():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    c = Calendar()

    for file in files:
        event = Event()
        event.name = file
        c.events.add(event)

    temp_file = 'calendar.ics'
    with open(temp_file, 'w') as f:
        f.writelines(c)

    return send_file(temp_file, as_attachment=True, attachment_filename='calendar.ics')

if __name__ == '__main__':
    app.run(debug=True)




