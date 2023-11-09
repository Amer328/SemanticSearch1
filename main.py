import streamlit as st
from io import StringIO
from vector_search import *
import qa
from utils import *


st.markdown("<h1 style='text-align: center; color: white;'>Semantic Search Engine for Documents and Q&A</h1>", unsafe_allow_html=True)



st.title("Ask Questions Relating to General Content, uses the Open AI Chat GPT API")
st.text("")

filename = False
query = False
options = st.radio(
    'Choose task',
    ('Ask a question','Update the Database of Documents', 'Delete Database of Documents'))

if 'Update the Database' in options:
    filename = st.text_input("Enter the full path of the PDF document")
    
if 'Ask a question' in options:
    query = st.text_input("Enter your question")

if 'Delete Database of Documents' in options:
    reset_index = "True"

button = st.button("Submit")
  
if button and (filename or query or reset_index):
    if 'Delete Database of Documents' in options:
        with st.spinner("Deleting Database of Documents, this may take a few minutes..."):
            rebuildIndex()
            st.success("Database Re-created")
            
    if 'Update the Database' in options:
        with st.spinner("Updating Database..."):

            # Split on last '.' 
            name, file_type = filename.rsplit('.', 1)

            if file_type == 'docx':
                corpusData = scrape_text_from_docx(filename)
                addData(corpusData,filename)
                st.success("Database Updated")
            elif file_type == 'pdf':
                corpusData = scrape_text_from_pdf(filename)
                addData(corpusData,filename)
                st.success("Database Updated")
            elif file_type == 'pptx':
                corpusData = scrape_text_from_pptx(filename)
                addData(corpusData,filename)
                st.success("Database Updated")
            elif file_type == 'csv':
                corpusData = scrape_text_from_csv(filename)
                addData(corpusData,filename)
                st.success("Database Updated")
            else:
                st.success("Unsupported file type")
            
            
    if 'Ask a question' in options:
        with st.spinner("Searching for the answer..."):
            result = find_match(query, 25)
            # Arrange the matching result as source, data, source ,data etc
            formatted_result = []
            for item in result:
                formatted_result.append(item[0])
                formatted_result.append(item[1])
            context= "\n\n".join(formatted_result)
            print(context)
            st.expander("Context").write(context)
            prompt = qa.create_prompt(context,query)
            answer = qa.generate_answer(prompt)
            # answer = str(source[0]) + "\n" + answer
            st.success("Answer: "+answer)
