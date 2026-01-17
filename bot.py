import streamlit as st
import torch
from transformers import pipeline


HF_TOKEN = st.secrets.HF_TOKEN


st.title("PeriodIQ✨")

@st.cache_resource
def get_pipe():
    # Loading in bfloat16 to save memory
    return pipeline("image-text-to-text", model="Qwen/Qwen3-VL-2B-Instruct", dtype=torch.bfloat16)

pipe = get_pipe()

# Use file uploader instead of a hardcoded URL to make it interactive
added_photo = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if added_photo:
    # Use the uploaded file object directly
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": added_photo},
                {"type": "text", "text": "What is the graph saying?"}
            ]
        },
    ]
    
    with st.spinner("Analyzing..."):
        result = pipe(text=messages)
        st.write(result[0]['generated_text'])




