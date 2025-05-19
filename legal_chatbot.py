import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# If the API key isn't found, show an error and stop execution
if not api_key:
    st.error("API key not found. Please change GROQ_API_KEY in your .env file.")
    st.stop()

# Set up OpenAI client (for Groq)
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama3-8b-8192"

# --- Streamlit UI ---

st.set_page_config(page_title="Legal Chatbot")
st.title("Legal Chatbot")
st.write("Ask any basic legal question below:")

# Dropdown for legal category
category = st.selectbox("Choose a legal category:", ["General", "Property", "Contracts", "Employment"])

# Manage input box key so we can reset it properly
if "input_key" not in st.session_state:
    st.session_state.input_key = "input_1"

# Show the text input box
user_input = st.text_input("Enter your legal question:", key=st.session_state.input_key)

# Add a reset button to clear chat history and input box
if st.button("Reset"):
    st.session_state.chat_history = []             
    st.session_state.input_key = "input_reset"     
    st.rerun()



# Init chat history if missing
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to query Groq
def get_groq_response(question, category):
    prompt = f"You are a helpful legal assistant specialized in {category} law. Answer this question clearly and concisely:\n\n{question}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# When the user submits a question, fetch the answer and update chat history
if user_input:
    with st.spinner("Thinking..."):
        try:
            answer = get_groq_response(user_input, category)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", answer))
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Show the full chat conversation on the page
for role, msg in st.session_state.chat_history:
    st.write(f"**{role}:** {msg}")
