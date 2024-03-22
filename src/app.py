from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
from openai import OpenAI

# Initialize OpenAI client with API key
OPEN_AI_API_KEY = "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"
client = OpenAI(api_key=OPEN_AI_API_KEY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFiles' not in request.files:
        return "No PDF files uploaded."
    
    pdf_files = request.files.getlist('pdfFiles')
    #print(pdf_files)

    all_text = process_pdf(pdf_files)
    completion_content = process_syllabus(all_text)
    #print(completion_content)

    return render_template('page.html', completion_content=completion_content)

def process_syllabus(all_text):
    # Initialize the prompt
    message = """
    Your job is to read through a course syllabus and list all assignment deadlines, midterm exam dates, and any other course deliverables that have due dates, all with any grade weightages. You should only include the name of the event with grade weightage if available (if not available, just use a hyphen as a filler), the start date formatted in year-month-day, and the end date formatted in year-month-day. For weekly assignments, list each individual assignment and the due date. Do not include and other text than what I have requested. Format as such: Name of Item, Start date, End date, Weightage.
    The syllabus you are using is provided below:
    """

    system_prompt = [{"role": "system", "content": message}]
    user_prompt = [{"role": "user", "content": message + all_text}]

    # No need for input() as this is a web application

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=system_prompt + user_prompt
    )

    return completion.choices[0].message.content

def process_pdf(pdf_files):
    all_text = ""  # Variable to store all text from PDF files

    for file in pdf_files:
        # Extract text from each PDF file
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Append the text from this file to the overall text
        all_text += text

    return all_text




def ics_syllabus(all_text):
    # Initialize the prompt
    message = """
    After printing the text requested above, you must print out an ics formatted text file where each item is listed as such: SUMMARY: Item Name
    DTSTART: Start date (YYYYMMDDT000000Z)
    DTEND: End date (YYYYMMDDT000000Z)
    Description: Weightage
    Include this line after you your BEGIN and VERSION lines:
    PRODID:-//Your Company//NONSGML v1.0//EN
    The syllabus you are using is provided below:
    """

    system_prompt = [{"role": "system", "content": message}]
    user_prompt = [{"role": "user", "content": message + all_text}]

    # No need for input() as this is a web application

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=system_prompt + user_prompt
    )

    return completion.choices[0].message.content

def process_pdf(pdf_files):
    all_text = ""  # Variable to store all text from PDF files

    for file in pdf_files:
        # Extract text from each PDF file
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Append the text from this file to the overall text
        all_text += text

    return all_text


if __name__ == '__main__':
    app.run(debug=True)
