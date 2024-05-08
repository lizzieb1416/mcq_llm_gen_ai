from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import dotenv
import logging
import json
logging.getLogger().setLevel(logging.INFO)

dotenv.load_dotenv()

##############################################################################
# This is a test to verify if the code works before doing the actual project #
##############################################################################

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

prompt1 = ChatPromptTemplate.from_template(TEMPLATE)
prompt2 = ChatPromptTemplate.from_template(TEMPLATE2)

model = ChatOpenAI()

NUMBER=5
SUBJECT="machine learning"
TONE="simple"

with open("/llm-gen-ai-project/src/common/mcqgenerator/data.txt", "r") as file:
    TEXT=file.read()

# loading json file 
with open('/llm-gen-ai-project/src/common/mcqgenerator/response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


chain1 = prompt1 | model | StrOutputParser()

chain2 = prompt2 | model | StrOutputParser()

super_chain = (
    {"quiz": chain1, "subject": itemgetter("subject")} | chain2
)


#invoke one chain at a time. 
# result1 = chain1.invoke({"text": TEXT, "number": NUMBER, "subject": SUBJECT, "tone": TONE, "response_json": json.dumps(RESPONSE_JSON)})
# result2 = chain2.invoke({"quiz": result1, "subject": SUBJECT})

# logging.info("CHAIN 1:")
# logging.info(result1)

# logging.info("CHAIN 2:")
# logging.info(result2)

# # Invoke only one chain, not showing intermidiate results. Only final answer.

# result3 = super_chain.invoke({"text": TEXT, "number": NUMBER, "subject": SUBJECT, "tone": TONE, "response_json": json.dumps(RESPONSE_JSON)})

# logging.info("SUPER CHAIN:")
# logging.info(result3)

####################
## Condensed form ##
####################

def review_chain(text, number, subject, tone, response_json):
    quiz = chain1.invoke({"text": text, "number": number, "subject": subject, "tone": tone, "response_json": json.dumps(response_json)})
    review = chain2.invoke({"quiz": quiz, "subject": subject})
    return {"quiz": quiz, "review": review}


response = review_chain(TEXT, 5, "machine learning", "simple", RESPONSE_JSON)

print(response.get("quiz"))
print(response.get("review"))
