import os 
import json 
import pandas as pd 
import traceback
from dotenv import load_dotenv
from common.mcqgenerator.logger import logging
from common.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from common.mcqgenerator.mcqgenerator import review_chain

# loading json file 
with open('/llm-gen-ai-project/src/common/mcqgenerator/response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Creator Application with Langchain")

# Create form
with st.form("user_inputs"):
    # file uppload
    upploaded_file = st.file_uploader("Uppload PDF or .txt file")

    # input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=50)

    # subject
    subject = st.text_input("Insert subject", max_chars=20)

    # quiz tone 
    tone = st.text_input("Complexity level of questions", max_chars=20, placeholder="Simple")

    # add button 
    button = st.form_submit_button("Generate MCQs")

    if button and upploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(upploaded_file)
                # count tokens and cost of API call
                with get_openai_callback() as cb:
                    response = review_chain(
                        text, mcq_count, subject, tone, RESPONSE_JSON
                        )
    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error generating MCQs")

            else: 
                print(f"Total tokens:{cb.total_tokens}")
                print(f"Prompt tokens: {cb.prompt_tokens}")
                print(f"Completion tokens: {cb.completion_tokens}")
                print(f"Total cost: {cb.total_cost}")
                
                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None: 
                        #table_data = get_table_data(quiz)
                        # if table_data is not None:
                        #     df = pd.DataFrame(table_data)
                        #     df.index = df.index + 1
                        #     st.table(df)
                        #     # display the review in a text box as well
                        #     st.text_area(label="Review", value=response["review"])
                        # else: 
                        #     st.error("Error extracting quiz data")
                        st.text_area(label="Quiz", value=json.loads(quiz))
                        st.text_area(label="Review", value=response["review"])
                    else: 
                        st.error("Error extracting quiz data")
                else: 
                    st.write(response)
                    






