from typing import List
import json
import logging
import sys
from langchain.chains import LLMChain
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from devrev.functions import devrev_functions as tools

from config import openai_key

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

adapted_toolbase = [
    Document(page_content=json.dumps(e), metadata={"index": i})
    for i,e in enumerate(tools)
]

embeddings = OpenAIEmbeddings(
    openai_api_key=openai_key,
)

vector_store = FAISS.from_documents(
    adapted_toolbase,
    embeddings,
)

# Output parser will split the LLM result into a list of queries
class LineList(BaseModel):
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)


output_parser = LineListOutputParser()

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to break down
    the question into a list different steps. The steps should be as specific as 
    possible. The number of steps should be less, but not lesser than neccessary.
    Your goal is to have the task broken down into simpler atomic steps.
    
    Example question: Summarize work items similar to don:core:dvrv-us-1:devo/0:issue/1
    Example answer:
    1. What are the work items similar to don:core:dvrv-us-1:devo/0:issue/1?
    2. Summarize the work items recieved from #1
    
    Example question: Prioritize my P0 issues and add them to the current sprint
    Example answer:
    1. Get my id
    2. Find my P0 issues using id
    3. Prioritize my P0 issues from #2
    4. Get the current sprint id
    5. Add issues from #2 to the sprint from #4

    Example question: What is the meaning of life?
    Example answer:
    1. Find the meaning of life

    Now solve the following question
    Original question: {question}""",
)

llm = OpenAI(
    openai_api_key=openai_key,
    temperature=0
)

llm_chat = ChatOpenAI(
    openai_api_key=openai_key,
    temperature=0
)

compressor = LLMChainExtractor.from_llm(llm)

llm_chain = LLMChain(llm=llm_chat, prompt=QUERY_PROMPT, output_parser=output_parser)

# RETRIEVERS

vs_retriever = vector_store.as_retriever()

llm_mq_retriever = MultiQueryRetriever(
    retriever=vs_retriever,
    llm_chain = llm_chain,
    parser_key='lines'
)

compression_retriever = ContextualCompressionRetriever(
    retriever=vs_retriever,
    compressor=compressor,
    parser_key='lines'
)

def get_tools_vs(query: str) -> list:
    """Get the tools from the query"""
    docs = vs_retriever.get_relevant_documents(query)
    return [ tools[int(doc.metadata["index"])] for doc in docs ]

def get_tools_mq(query:str) -> list:
    """Get the tools from the query"""
    docs = llm_mq_retriever.get_relevant_documents(query)
    return [ tools[int(doc.metadata["index"])] for doc in docs ]

def get_tools_cr(query:str) -> list:
    """Get the tools from the query"""
    docs = compression_retriever.get_relevant_documents(query)
    return [ tools[int(doc.metadata["index"])] for doc in docs ]

if __name__ == '__main__':
    print('tool retriever is running')
    while True:
        prompt = input('prompt: ')
        retrieved = get_tools_vs(prompt)
        print('retrieved tools:', len(retrieved))
        for tool in retrieved:
            print(tool['name'])