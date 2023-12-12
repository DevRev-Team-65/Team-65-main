# Core requirements
import os
# from dotenv import load_dotenv

# Framework Requirements
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI

# Library Requirements
from src.retrievers import (
    VectorStoreRetriever,
    CustomMultiQueryRetriever,
    CustomContextualCompressionRetriever
)
from src.composers import (
    ChainOfThoughtComposer
)
from src.functions import devrev_functions
from src.examples import example_queries


# # Load the environment variables from the .env file
# load_dotenv()

# # Fetch the openai_api_key from the environment variables
# try:
#     openai_api_key = os.getenv("OPENAI_API_KEY")
# except:
#     raise Exception("Please set the OPENAI_API_KEY environment variable or create a .env file with the key.")

st.title("AI Agent 007")

openai_api_key = st.sidebar.text_input("OpenAI API Key", value="", type="password")

hf_embeddings = HuggingFaceEmbeddings()

example_str = "".join(
    [
        f"""
        Query:
        {query}
        Answer:
        {functions}
        """
        for query, functions in example_queries[:4]
    ]
)

with st.text("Tooling Up For Success...."):
    
    while True:
        if openai_api_key is None:
            continue
        elif not openai_api_key.startswith("sk-"):
            st.warning("Please enter a valid OpenAI API Key")
        else:
            break

with st.spinner("Initializing Components...."):
    chat_llm = ChatOpenAI(
        openai_api_key = openai_api_key,
        temperature=0.7,
    )

    cmq_ret = CustomMultiQueryRetriever(
        chat_llm,
        embeddings=hf_embeddings,
        name = "cmq_ret_01",
        init_functions=devrev_functions.copy()
    )

    composer = ChainOfThoughtComposer(
        chat_llm=chat_llm,
    )

def run_query(query_str: str):
    retrieved_simfunc = cmq_ret.find_functions(query_str)
    answer = composer(
        query=query_str,
        functions=retrieved_simfunc,
        examples=example_str
    )
    return answer['text']
### STREAMLIT UI ###

with st.form('Chat'):
    if openai_api_key is not None:
        text = st.text_area('Enter your query here', value='')
        submit = st.form_submit_button('Submit')
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter a valid OpenAI API Key")
        elif submit:
            with st.spinner("Thinking..."):
                json_res = run_query(text)
            st.json(json_res)