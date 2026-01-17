import streamlit as st
import torch
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   


hf auth login = st.secrets.huggingface_api_key


pipe = pipeline("image-text-to-text", model="google/medgemma-1.5-4b-it")
added_photo = st.file_uploader("Add Image",type = ["jpg", "jpeg", "png"])
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
