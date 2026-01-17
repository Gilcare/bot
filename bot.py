import streamlit as st
import torch
from huggingface_hub import login
from transformers import pipeline
#from transformers import AutoProcessor, AutoModelForImageTextToText
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   

HF_TOKEN = st.secrets.HF_TOKEN





pipe = pipeline("image-text-to-text", model="Qwen/Qwen3-VL-2B-Instruct")
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]
pipe(text=messages)
