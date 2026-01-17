import streamlit as st
import torch
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   


hf auth login = st.secretshuggingface_api_key
