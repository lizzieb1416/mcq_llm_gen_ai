import os 
import json 
import pandas as pd 
import traceback
from operator import itemgetter
from dotenv import load_dotenv
from common.mcqgenerator.logger import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.5)

template1= """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
{response_json}
"""

template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}
Check from an expert English Writer of the above quiz:
"""

prompt1 = ChatPromptTemplate.from_template(template1)
prompt2 = ChatPromptTemplate.from_template(template2)

quiz_chain = prompt1 | llm | StrOutputParser()
quiz_evaluation_chain = prompt2 | llm | StrOutputParser()

def review_chain(text, number, subject, tone, response_json):
    quiz = quiz_chain.invoke({"text": text, "number": number, "subject": subject, "tone": tone, "response_json": json.dumps(response_json)})
    review = quiz_evaluation_chain.invoke({"quiz": quiz, "subject": subject})
    return {"quiz": quiz, "review": review}



