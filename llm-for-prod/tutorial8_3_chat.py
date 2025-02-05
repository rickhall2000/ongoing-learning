# I have not installed anything, so this won't work

import os
import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from elevenlabs import generate
from langchain.chains import RetrievalQA 
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from streamlit_chat import message

# Constants
TEMP_AUDIO_PATH = "temp_audio.wav"
AUDIO_FORMAT = "audio/wav"

# Load environment variables from .env file and return the keys
openai.api_key = os.environ.get('OPENAI_API_KEY')
eleven_api_key = os.environ.get('ELEVEN_API_KEY')

def load_embeddings_and_database(active_loop_data_set_path):
    embeddings = OpenAIEmbeddings()
    db = DeepLake(
        dataset_path=active_loop_data_set_path,
        read_only=True,
        embedding_function=embeddings
    )
    return db

def transcribe_audio(file_path, openai_key):
    openai.api_key = openai_key
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        print(f"Error calling whisper api {str(e)}")
        return None
    
def record_and_transcribe_audio():
    audio_bytes = audio_recorder()
    transcription = None
    if audio_bytes:
        st.audio(audio_bytes, format=AUDIO_FORMAT)
        
        with open(TEMP_AUDIO_PATH, "wb") as f:
            f.write(audio_bytes)
            
        if st.button("Transcribe"):
            transcription = transcribe_audio(TEMP_AUDIO_PATH, openai.api_key)
            os.remove(TEMP_AUDIO_PATH)
            display_transcription(transcription)
            
    return transcription

def display_transcription(transcription):
    if transcription:
        st.write(f"Transcription: {transcription}")
        with open ("audio_transcript.txt", "w") as f:
            f.write(transcription)
    else:
        st.write("Transcription failed.")
    
def get_user_input(transcription):
    return st.text_input("", value=transcription if transcription else "", key="input")

def search_db(user_input, db):
    print(user_input)
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['fetch_k'] = 100
    retriever.search_kwargs['k'] = 4
    retriever.search_kwargs['maximal_marginal_relevance'] = True
    model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    qa = RetrievalQA.from_llm(model, retriever=retriever, return_source_documents=True)
    return qa({"query": user_input})

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i] is_user=True, key=str(i) + '_user')
        message(history["generated"][i], key=str(i))
        voice = "Bella"
        text = history["generated"][i]
        audio = generate(text=text, voice=voice)
        st.audio(audio, format='audio/mp3')
        
def main():
    st.write('# JavisBase')
    db = load_embeddings_and_database(dataset_path)
    transcription = record_and_transcribe_audio()
    user_input = get_user_input(transcription)
    
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["I am ready to help you"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hi"]
        
    if user_input:
        output = search_db(user_input, db)
        print(output['source_documents'])
        st.session_state.past.append(user_input)
        response = str(output['result'])
        st.session_state.generated.append(response)
        
    if st.session_state["generated"]:
        display_conversation(st.session_state)

if __name__ == "__main__":
    main()
    
