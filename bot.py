import streamlit as st
import torch
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   

@st.cache_resource
def load_pipeline():
    # Adding torch_dtype="auto" or "float16" speeds up GPU inference
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.float16)

pipe = load_pipeline()

def chatbot():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # ... (History initialization and display code) ...

    if user_input := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Setup for streaming
        streamer = TextIteratorStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        # Prepare arguments
        messages = st.session_state.messages # Use full history for context
        generation_kwargs = dict(
            text_inputs=messages, 
            streamer=streamer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

        # Run generation in a background thread to prevent UI blocking
        thread = Thread(target=pipe, kwargs=generation_kwargs)
        thread.start()

      
        # Display the stream
        full_response = st.write_stream(streamer)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})



tab1, tab2, tab3 = st.tabs(["📝 Today", "📊 Metrics","✨Ask Kyma"])

with tab1:
    st.subheader("Hi")
with tab2:
    st.subheader("Metrics")
with tab3:
    chatbot()


