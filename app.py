import os
import google.generativeai as genai
import streamlit as st
from pdfextractor import text_extractor
from wordextractor import doc_text_extract
from image2text import extract_text_image


# Lets configure Genai model
gemini_key = os.getenv('GOOGLE_API_KEY2')
genai.configure(api_key = gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                              generation_config={'temperature':0.9})

# Lets create the side bar
st.sidebar.title(':red[UPLOADS YOUR NOTES:]')
st.sidebar.subheader(':blue[Only upload Images, PDFs and DOCX]')
user_file = st.sidebar.file_uploader('Upload Here:',type=['pdf','docx','png','jpg','jpeg','jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type in ["image/png","image/jpeg","image/jpg","image/jfif"]:
        user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)
    else:
        st.sidebar.error('Enter the correct file type')

# Lets create main page
st.title(':orange[MoM Generator:-] :green[AI Assisted Minutes of meeting Generator]')
st.subheader(':red[This application creates generalized minutes from notes.]')
st.write('''
         Follow the steps:
         1. Upload the notes in PDF, DOCX or Image Format in sidebar.
         2. Click "generate" to generate the MoM.''')

if st.button('Generate'):
    with st.spinner('Please wait...'):
        prompt=f'''
        <Role> -You are an expert in writing and formating minutes of meetings.
        
        <Goal> Create minutes of meetings from the notes that user has provided.
        <Context> The user has provided some rough notes as text. Here are the notes: {user_file}
        <Format> The output must follow the below format:
        * Title: asume title of the meeting
        * Agenda: Assume agenda of the meeting.
        * Attendees: Name of the Attendees(If name of the attendees is not in their keep in it).
        * Date and Place: Date and the Place of the meeting (If not provided keep it Online)
        * Body: The body should follow the following sequence of points
            - Key points:
            - Highlights and Decision that has been taken.
            - Mention actionable items.
            - Mention any deadline if discussed.
            - Next meeting date if discussed.
            - Add a 2-3 line of summary.
        <Instruction>
        - Use bullet points and highlight the important keywords by making them bold.
        - Generate the output in docx format.
        - Do not add any word of your own.'''

        response = model.generate_content(prompt)
        st.write(response.text)

    if st.download_button(label='DOWNLOAD',data=response.text,
                          file_name='mom_generated.txt',mime ='text/plain'):
        st.success('Your File has been Downloaded')
