import streamlit as st
from io import StringIO
from vector_search import *
import qa
from utils import *
import os

st.markdown("<h1 style='text-align: center; color: white;'>Semantic Search Engine for Documents and Q&A</h1>", unsafe_allow_html=True)



st.title("Ask Questions Relating to General Content, uses the Open AI Chat GPT API")
st.text("")

# Sidebar section for uploading files and providing a  URL
with st.sidebar:

     with st.form("my-form", clear_on_submit=True):
        uploaded_files = st.file_uploader("Please enter youtube url:", accept_multiple_files=True, type=None)
         
    with st.form("my-form", clear_on_submit=True):
        uploaded_files = st.file_uploader("Please upload your file, one file at a time only please...", accept_multiple_files=True, type=None)
        for uploaded_file in uploaded_files:
            
            # Create the full file path for the uploaded file
            filename = os.path.join(os.getcwd(), uploaded_file.name)
            # Save the uploaded file to disk
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())

        submitted = st.form_submit_button("UPLOAD!")

    if submitted and filename is not None:
        st.write("UPLOADED!",filename)
        # do stuff with your file
        with st.spinner("Updating Database..."):

            # Split on last '.' 
            name, file_type = filename.rsplit('.', 1)

            if file_type == 'docx':
                corpusData = scrape_text_from_docx(filename)
                addData(corpusData,filename)
                st.success("Database Updated With docx")    
            elif file_type == 'txt':
                corpusData = scrape_text_from_txt(filename)
                addData(corpusData,filename)
                st.success("Database Updated With txt")
            elif file_type == 'pdf':
                corpusData = scrape_text_from_pdf(filename)
                addData(corpusData,filename)
                st.success("Database Updated With pdf")
            elif file_type == 'pptx':
                corpusData = scrape_text_from_pptx(filename)
                addData(corpusData,filename)
                st.success("Database Updated With ppt")
            elif file_type == 'csv':
                corpusData = scrape_text_from_csv(filename)
                addData(corpusData,filename)
                st.success("Database Updated With csv")
            elif file_type in ('png', 'jpeg', 'jpg', 'gif'):
                corpusData = scrape_text_from_image(filename)
                addData(corpusData,filename)
                st.success("Database Updated With Image")
            else:
                st.success("Unsupported file type")
            uploaded_files=''
            filename = ''


filename = False
query = False
options = st.radio(
    'Choose task',
    ('Ask a question', 'Delete Database of Documents'))

    
if 'Ask a question' in options:
    query = st.text_input("Enter your question")

if 'Delete Database of Documents' in options:
    reset_index = "True"

button = st.button("Submit")
  
if button and (query or reset_index):
    if 'Delete Database of Documents' in options:
        with st.spinner("Deleting Database of Documents, this may take a few minutes..."):
            rebuildIndex()
            st.success("Database Re-created")
            
            
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
