import os
import json
import pandas as pd
import traceback
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import PyPDF3 
from langchain.schema.runnable import RunnableSequence
from dotenv import load_dotenv

import streamlit as st
KEY = st.secrets["openai_api_key"]

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import quiz_chain, quiz_evaluation_prompt
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain


from pathlib import Path

file_json = Path(__file__).parent / "Response.json"
with open(file_json, "r", encoding="utf-8") as file:
    RESPONSE_JSON = file.read()



import streamlit as st
import pandas as pd
import traceback

#creating a title for the app
st.title("MCQs Creator Application with LangChain ❶ %$")

#Create a form using st.form
with st.form("user_input"):
    #File Upload
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",placeholder="Topic",max_chars=20)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    #Submit Button
    button=st.form_submit_button("Generate MCQs")
    
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(uploaded_file)

            response = generate_evaluate_chain(
                {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                }
            )

        except Exception as e:
            st.error(f"Error: {e}")

    
    if isinstance(response, dict):
        #Extract the quiz data from the response
        quiz=response.get("quiz", None)
        if quiz is not None:
            table_data=get_table_data(quiz)
            if table_data is not None:
                df=pd.DataFrame(table_data)     
                df.index=df.index+1
                st.table(df)
                #Display the review in atext box as well
                st.text_area(label="Review", value=response["review"])
            else:
                st.error("Error in the table data")
        
        else:
            st.write(response)


            
    
