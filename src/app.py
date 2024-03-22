from flask import Flask, render_template, send_file, request
import os
import tempfile
from ics import Calendar, Event

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFiles' not in request.files:
        return "No PDF files uploaded."
    
    pdf_files = request.files.getlist('pdfFiles')
    
    for file in pdf_files:
        if file.filename == '':
            return "No selected file"
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return "Files uploaded successfully"

@app.route('/download_ics', methods=['POST'])
def download_ics():
    if 'pdfFiles' not in request.files:
        return "No PDF files uploaded."

    pdf_files = request.files.getlist('pdfFiles')
    c = Calendar()

    for file in pdf_files:
        event = Event()
        event.name = file.filename
        c.events.add(event)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    with open(temp_file.name, 'w') as f:
        f.writelines(c)

    return send_file(temp_file.name, as_attachment=True, attachment_filename='calendar.ics')

if __name__ == '__main__':
    app.run(debug=True)
