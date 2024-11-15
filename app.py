# Page configuration must be the first Streamlit command
import streamlit as st
st.set_page_config(
    page_title="Bhagavad Gita GPT",
    page_icon="🕉️",
    layout="wide"
)

import time
import pickle
import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['openai_api_key'])

# Initialize Hugging Face model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
    model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
    return tokenizer, model

tokenizer, model = load_model()

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #0B0B45;
        padding: 2rem;
    }
    
    /* Header styles */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1E1E66, #0B0B45);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .title {
        color: #A8FF00;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-family: 'Devanagari MT', serif;
    }
    
    .subtitle {
        color: #FFFFFF;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .sanskrit-quote {
        color: #A8FF00;
        font-size: 1.2rem;
        font-style: italic;
        margin: 1rem 0;
    }
    
    /* Input container */
    .input-container {
        background: rgba(30, 30, 102, 0.7);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    /* Suggestion buttons */
    .suggestion-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .stButton button {
        background-color: #A8FF00 !important;
        color: #0B0B45 !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #C0FF00 !important;
        transform: scale(1.05) !important;
    }
    
    /* Response container */
    .response-container {
        background: rgba(30, 30, 102, 0.7);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        color: #FFFFFF;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border: 2px solid #A8FF00 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        color: #FFFFFF;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #A8FF00;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Override default Streamlit theme */
    .stApp {
        background-color: #0B0B45 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="title">🕉️ BHAGAVAD GITA GPT</h1>
    <p class="subtitle">Seek Divine Wisdom Through AI</p>
    <p class="sanskrit-quote">"कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।"</p>
</div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Suggested questions
    suggestions = [
        "How can I find inner peace in difficult times?",
        "What does the Gita say about duty and dharma?",
        "How to overcome fear and anxiety?",
        "What is the path to true happiness?",
        "How to maintain balance in life?"
    ]

    # Display suggestions in a scrollable container
    st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)
    for suggestion in suggestions:
        if st.button(suggestion, key=f"suggestion-{suggestion}"):
            st.session_state.question = suggestion
    st.markdown('</div>', unsafe_allow_html=True)

    # Input field
    question = st.text_input(
        "Ask your question",
        key="question",
        placeholder="Type your question here...",
        value=st.session_state.get('question', '')
    )

def generate_response(question):
    # First, try with OpenAI
    try:
        prompt = f"""You are Krishna from the Mahabharata, answering questions based on the Bhagavad Gita's teachings.
        Question: {question}
        Please provide guidance with wisdom, compassion, and references to specific verses when applicable."""
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        # Fallback to local model
        try:
            inputs = tokenizer(f"Question about Bhagavad Gita: {question}\nAnswer:", return_tensors="pt", max_length=512, truncation=True)
            with torch.no_grad():
                output_sequences = model.generate(
                    input_ids=inputs["input_ids"],
                    max_length=200,
                    temperature=0.7,
                    top_p=0.9,
                    num_return_sequences=1
                )
            response = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
            return response
        except Exception as local_e:
            return "I apologize, but I am unable to process your question at the moment. Please try again later."

# Process question when submitted
if question:
    with st.spinner('Seeking divine wisdom...'):
        response = generate_response(question)
        
        st.markdown("""
        <div class="response-container">
            <h3>Divine Guidance:</h3>
            <p>{}</p>
        </div>
        """.format(response), unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🕉️ Created with devotion by GJAM Technologies</p>
    <p>Part of the Tumhari Universe</p>
</div>
""", unsafe_allow_html=True)