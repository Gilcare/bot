import streamlit as st
import torch
from huggingface_hub import login
from transformers import pipeline
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   

HF_TOKEN = st.secrets.HF_TOKEN
added_photo = st.file_uploader("Add Image",type = ["jpg", "jpeg", "png"])

pipe = pipeline("image-to-text", model="google/medgemma-1.5-4b-it")
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": added_photo},
            {"type": "text", "text": "What is the graph saying?"}
        ]
    },
]
pipe(text=messages)
