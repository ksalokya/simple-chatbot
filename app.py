import time
import streamlit as st
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load LLM
llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()

# Add context if needed
context = """
"""

# Prompt Template
prompt = ChatPromptTemplate.from_template(
    """
You are Chat Assistant. Your role is to provide information clearly and politely.
Please answer the questions based only on this context : 

<context>
{context}e
</context>

Answer the question briefly, using neutral language.

Question: {question}
"""
)



# Title
st.markdown(
    "<h3 style='text-align:center; color:#6a1b4d; font-weight:600; font-size:20px;'>What can I help with?</h3>",
    unsafe_allow_html=True,
)


import streamlit as st
import time

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.chat_input("Ask a question...")

if question:
    st.session_state.chat_history.append(("You", question))

    # Display all previous messages including the new question
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)

    # Show animation while LLM is processing
    loader_placeholder = st.empty()
    loader_placeholder.image("https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif", width=100, caption="Loading...")

    # Get response from LLM
    chain = prompt | llm | output_parser
    full_response = chain.invoke({"context": context, "question": question})

    # Remove loader
    loader_placeholder.empty()

    # Typing animation placeholder
    placeholder = st.empty()

    assistant_response = ""
    for i in range(len(full_response)):
        assistant_response = full_response[: i + 1]
        placeholder.markdown(f"{assistant_response}▌")
        time.sleep(0.05)

    placeholder.markdown(f"{full_response}")

    st.session_state.chat_history.append(("S", full_response))

else:
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)
