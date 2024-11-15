import pandas as pd
import numpy as np
import streamlit as st
import time
import faiss
import pickle
import os
from pathlib import Path
import openai
import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = st.secrets.get('openai_api_key')

# Custom CSS for styling and responsiveness
st.markdown("""
    <style>
        body {
            background-color: #0B0B45;  /* Dark navy background */
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .header {
            font-size: 40px;
            color: #A8FF00;  /* Neon green */
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
            animation: fadeIn 2s ease-in-out;
        }
        .subheader {
            font-size: 22px;
            color: #FFFFFF;
            text-align: center;
            margin-top: -20px;
            margin-bottom: 20px;
            animation: fadeIn 2s ease-in-out;
        }
        .quote {
            text-align: center;
            font-size: 20px;
            color: #A8FF00;
            font-style: italic;
            margin-top: 10px;
            margin-bottom: 30px;
            animation: fadeIn 2s ease-in-out;
        }
        .input-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 20px 0;
        }
        .stTextInput>div>div>input {
            width: 100%;
            max-width: 600px;
            padding: 15px;
            font-size: 18px;
            border: 2px solid #A8FF00;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #A8FF00;
            color: #000000;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #C0FF00;
            transform: scale(1.05);
        }
        .suggestion-box {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .suggestion-button {
            background-color: #A8FF00;
            color: #000000;
            padding: 10px 15px;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.1s ease, background-color 0.3s ease;
        }
        .suggestion-button:hover {
            transform: scale(1.05);
            background-color: #C0FF00;
        }
        .answer-section {
            background-color: #1E1E66;
            padding: 20px;
            border-radius: 8px;
            font-size: 18px;
            color: #A8FF00;
            line-height: 1.6;
            animation: fadeIn 2s ease-in-out;
            margin-top: 20px;
        }
        .footer {
            font-size: 16px;
            color: #FFFFFF;
            text-align: center;
            margin-top: 50px;
            font-weight: bold;
        }
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 10px;
        }
        .social-icons img {
            width: 30px;
            height: 30px;
            transition: transform 0.2s;
        }
        .social-icons img:hover {
            transform: scale(1.2);
        }

        /* Keyframes for animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Display logo
st.image("Search.png", width=150)

# Header and Subheader
st.markdown("<div class='header'>INDIAN.GIVES</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Ask Bhagavad Gita Your Questions</div>", unsafe_allow_html=True)

# Display an inspirational Hindi quote
st.markdown("""
    <div class='quote'>
        "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।"
    </div>
""", unsafe_allow_html=True)

# Input field and search button
with st.form(key='question-form'):
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    question = st.text_input(
        "What wisdom are you seeking today?",
        placeholder="Type your question here...",
        key="user-input"
    )
    submit_button = st.form_submit_button("Ask")
    st.markdown("</div>", unsafe_allow_html=True)

# Suggested questions
suggestions = [
    "How can I find true happiness?",
    "What should I do if I'm feeling anxious?",
    "How do I overcome fear?",
    "What is my purpose in life?",
    "How can I find peace of mind?"
]

st.markdown("<div class='suggestion-box'>", unsafe_allow_html=True)
for suggestion in suggestions:
    if st.button(suggestion, key=f"suggestion-{suggestion}"):
        question = suggestion
st.markdown("</div>", unsafe_allow_html=True)

# Process user input
if submit_button and question:
    # Call OpenAI API or generate response based on the Bhagavad Gita
    st.markdown(f"<div class='answer-section'>Your question: {question}</div>", unsafe_allow_html=True)
    st.markdown("<div class='answer-section'>Response: <em>Based on the Bhagavad Gita...</em></div>", unsafe_allow_html=True)

# Footer with social media links
st.markdown("""
    <div class='footer'>
        Powered by <b>GJAM Technologies</b><br>
        Part of the <b>Tumhari Universe</b> product line<br>
        <div class="social-icons">
            <a href="https://www.facebook.com/gjamtechnologies" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
            </a>
            <a href="https://www.twitter.com/gjamtechnologies" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Twitter">
            </a>
            <a href="https://www.linkedin.com/company/gjamtechnologies" target="_blank">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn">
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)
