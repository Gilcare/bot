import streamlit as st
import torch
from huggingface_hub import login
from transformers import AutoProcessor, AutoModelForImageTextToText
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   

HF_TOKEN = st.secrets.HF_TOKEN




processor = AutoProcessor.from_pretrained("google/medgemma-1.5-4b-it")
model = AutoModelForImageTextToText.from_pretrained("google/medgemma-1.5-4b-it")
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]
inputs = processor.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=40)
print(processor.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
