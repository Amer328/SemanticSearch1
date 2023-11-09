import os
import streamlit as st
import openai

# Fetch the OpenAI Key from Windows env
# api_key = os.environ["OPENAI_API_KEY"]
api_key = st.secrets["OPENAI_API"]

# Set the OpenAI key
openai.api_key = api_key


def create_prompt(context,query):
    header = "Answer the question with as much detail as possible using the provided context and support your answer with paragraphs and bullet points. If no answer is generated, print 'Sorry insufficient data to answer query' \n"
    return header + context + "\n\n" + query + "\n"


def generate_answer(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    max_tokens=12000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return(response.choices[0].message.content)
