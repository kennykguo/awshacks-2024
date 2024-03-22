from PyPDF2 import PdfReader 
from openai import OpenAI
#from dotenv import load_dotenv
import os


OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

client = OpenAI(
   api_key=os.environ.get("OPEN_AI_API_KEY"),
) 


# Initalize OpenAI class
from openai import OpenAI
client = OpenAI()

# Initalize PDF reader class and get text
reader = PdfReader("test.pdf")
text = ""
# Loops through all pages
for page in reader.pages:
   text += page.extract_text()  

# Initalize the prompt
prompt = '''Your job is now to read through a course syllabus and list all assignment deadlines, midterm exam dates, and any other course deliverables that have due dates, all with any grade weightages. Do not include any extra text. This information is going to be used to create an ics file that the user (students) should be able to use to upload to their preferred calendar application: 

The syllabus you are using is provided below: '''

sys_prompt = [{"role": "system", "content": prompt}]
usr_prompt = [{"role": "user", "content": text}]
model = "gpt-3.5-turbo"

proceed = input("Proceed? y / n")
if proceed == 'y':
    response = client.chat.completions.create(
        model = model,
        messages = sys_prompt + usr_prompt
    )
    
    print("Done!")

print(response.choices[0].message)
