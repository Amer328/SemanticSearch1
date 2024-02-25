import streamlit as st
from io import StringIO
from vector_search import *
import qa
from utils import *
import os
from pytube import YouTube
from io import BytesIO
from pathlib import Path

st.markdown("<h1 style='text-align: center; color: white;'>Semantic Search Engine for Documents and Q&A</h1>", unsafe_allow_html=True)



st.title("Ask Questions Relating to General Content, uses the Open AI Chat GPT API")
st.text("")

# Sidebar section for uploading files and providing a  URL
with st.sidebar:

    with st.form("my-form2", clear_on_submit=True):
        download_url = st.text_input("Please enter your video url:")
        submitted = st.form_submit_button("Download from URL")

    if submitted and download_url is not None:
        
        st.write("Downloading Video URL...",download_url)
        # do stuff with your file 
        buffer = BytesIO()
        youtube_video = YouTube(download_url)
        audio = youtube_video.streams.get_audio_only()
        video = youtube_video.streams.first()
        default_filename = audio.default_filename
        #audio.stream_to_buffer(buffer)
        video.stream_to_buffer(buffer)

        st.subheader("Title")
        st.write(default_filename)
        title_vid = Path(default_filename).with_suffix(".mp4").name
        st.subheader("Download Video File")
        st.download_button(
            label="Download mp4",
            data=buffer,
            file_name=title_vid,#'c:\\temp\\download.mp3',
            mime="video/mpeg")

         
    with st.form("my-form", clear_on_submit=True):
        uploaded_files = st.file_uploader("Please upload your file, one file at a time only please...", accept_multiple_files=True, type=None)
        for uploaded_file in uploaded_files:
            
            # Create the full file path for the uploaded file
            filename = os.path.join(os.getcwd(), uploaded_file.name)
            # Save the uploaded file to disk
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())

        submitted = st.form_submit_button("Upload File")

    if submitted and filename is not None:
        st.write("Uploaded",filename)
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
            elif file_type in ('png', 'jpeg', 'jpg', 'gif','GIF','JPG'):
                corpusData = scrape_text_from_image(filename)
                addData(corpusData,filename)
                st.success("Database Updated With Image")
            elif file_type == 'mp4':
                corpusData = scrape_text_from_mp4(filename)
                addData(corpusData,filename)
                upload_url = ''
                st.success("Database Updated With Video Transcript")
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
