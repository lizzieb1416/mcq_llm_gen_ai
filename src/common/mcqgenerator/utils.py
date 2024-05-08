import os 
import json 
import pandas as pd 
import traceback
import PyPDF2

def read_file(file): 
    if file.name.endswith('.pdf'):
        try: 
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text+= page.extract_text()
            return text
        
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
        
    elif file.name.endswith('.txt'):
        return file.read().decode("utf-8")
    
    else: 
        raise Exception("File format not supported: only PDF and text files are supported")
    

def get_table_data(quiz_str):
    try:
        # convert the quiz data from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # iterate over the quiz dictionary and extract the required info
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option} -> {option.value}" for option, option_value in value["options"].items()
                ]
            )

            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False