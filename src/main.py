from PyPDF2 import PdfReader
from openai import OpenAI
import os

# Setup OpenAI
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(
    api_key=os.environ.get("OPEN_AI_API_KEY"),
)

# Initialize PDF reader class and get text
reader = PdfReader("test.pdf")
text = ""

# Loops through all pages
for page in reader.pages:
    text += page.extract_text()

# Initialize the prompt
message = """

Your job is to read through a course syllabus and list all assignment deadlines, midterm exam dates, and any other course deliverables that have due dates, all with any grade weightages. You should only include the name of the event with grade weightage if available (if not available, just use a hyphen as a filler), the start date formatted in year-month-day, and the end date formatted in year-month-day. For weekly assignments, list each individual assignment and the due date. Do not include and other text than what I have requested. Format as such: Name of Item, Start date, End date, Weightage

The syllabus you are using is provided below:
"""

system_prompt = [{"role": "system", "content": message}]
user_prompt = [{"role": "user", "content": message + text}]

proceed = input("Proceed? y / n: ")
if proceed == 'y':
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=system_prompt + user_prompt
    )

print(completion.choices[0].message.content)
print("Done!")
