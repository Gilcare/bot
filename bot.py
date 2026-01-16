import streamlit as st
import torch
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

st.markdown('<h1 style="color:#FF46A2; text-align: center;">PeriodIQ✨</h1>', unsafe_allow_html=True)
st.divider()   


# Initialize session state to track if we should show the image agent
if 'show_image_agent' not in st.session_state:
    st.session_state.show_image_agent = False

def image_agent():
    # Load pipeline only once to save memory/time
    if "image_pipe" not in st.session_state:
        with st.spinner("Loading Vision Model..."):
            # Ensure model name is correct (e.g., Qwen2-VL or Qwen2.5-VL)
            st.session_state.image_pipe = pipeline("image-text-to-text", model="Qwen/Qwen3-VL-2B-Instruct")
    
    add_image = st.file_uploader("Add Image", type=["jpg", "jpeg", "png"])
    
    if add_image is not None:
        # Display the image so the user knows it's uploaded
        st.image(add_image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Analyze Graph"):
            with st.spinner("Analyzing..."):
                # Use the bytes directly from the uploaded file
                image_input = [{ 
                    "role": "user", 
                    "content": [
                        {"type": "image", "image": add_image.getvalue()}, # Use getvalue() for raw bytes
                        {"type": "text", "text": "Explain this graph in very simple terms?"}
                    ]
                }]
                result = st.session_state.image_pipe(image_input)
                st.write(result[0]['generated_text'])

# In your main app logic











'''
@st.cache_resource
def load_pipeline():
    # Adding torch_dtype="auto" or "float16" speeds up GPU inference
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.float16)
def image_agent():
    image_pipe = pipeline("image-text-to-text", model="Qwen/Qwen3-VL-2B-Instruct")
    add_image = st.file_uploader("Add Image", type = ["csv","jpg", "jpeg", "png"])
    image_input = [{ 
        "role": "user", 
        "content":[
            {"type": "image", "image": add_image},
            {"type": "text", "text": "Explain this graph in very simple terms?"}]},]
    st.write(image_pipe(text = image_input))
    '''






app = st.sidebar.selectbox("Menu",["🧭 Metrics", "🧠Insights","✨ Ask Kyma"])
if app == "🧭 Metrics":
    st.subheader("🧭 Metrics")
elif app == "🧠Insights":
    st.subheader("🧠 Insights")
    if st.button("Open Insights Tool"):
        st.session_state.show_image_agent = True
    
    if st.session_state.show_image_agent:
        image_agent()
elif app == "✨ Ask Kyma":
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

        with st.chat_message("assistant", avatar="👩🏼‍🦰"):
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

    





