# Core requirements
import os
# from dotenv import load_dotenv

# Framework Requirements
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
import os
import logging
from datetime import datetime
from langchain.callbacks import get_openai_callback
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the logs folder if it doesn't exist
logs_folder = "logs"
os.makedirs(logs_folder, exist_ok=True)

# Set up the logging configuration
log_file = os.path.join(logs_folder, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rest of the code...

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

    retriever = CustomMultiQueryRetriever(
        chat_llm,
        embeddings=hf_embeddings,
        name = "cmq_ret_01",
        init_functions=devrev_functions.copy()
    )

    composer = ChainOfThoughtComposer(
        chat_llm=chat_llm,
    )

def run_query(query_str: str):
    with get_openai_callback() as cb: #for tracking usage
        retrieved_simfunc = retriever.find_functions(query_str)
        answer = composer(
            query=query_str,
            functions=retrieved_simfunc,
            examples=example_str
        )
    return answer['text'], cb
### STREAMLIT UI ###

with st.form('Chat'):
    if openai_api_key is not None:
        text = st.text_area('Enter your query here', value='')
        submit = st.form_submit_button('Submit')
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter a valid OpenAI API Key")
        elif submit:
            with st.spinner("Thinking..."):
                json_res, usage = run_query(text)
            st.json(json_res)
            st.sidebar.info(f"""
            Usage Info for this query:
                Total Tokens: {usage.total_tokens}\n
                Prompt Tokens: {usage.prompt_tokens}\n
                Completion Tokens: {usage.completion_tokens}\n
                Total Cost: ${usage.total_cost}
            """)