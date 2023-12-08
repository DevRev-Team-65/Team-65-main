import json
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.prompts import PromptTemplate

class LineList(BaseModel):
    '''
    LineList is a pydantic object that contains a list of strings
    '''
    lines: list[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    '''
    LineListOutputParser is a wrapper around PydanticOutputParser that parses the output of the LLM into a list of strings
    '''
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)

## Classess for the retrievers

class VectorStoreRetriever:
    '''
    VectorStore is a wrapper around FAISS that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_key,
        )
        #create a vector store
        self.vector_store = FAISS.from_documents(
            [],
            self.embeddings,
        )
        self.vs_retriever = self.vector_store.as_retriever()
        self.documents = 0
    
    def add_functions(self, function_list: list[dict]):

        for i,f in enumerate(function_list):
            function_list[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1

        self.vector_store.add_documents(function_list)
    
    def find_functions(self, query: str):
        return self.vector_store.get_relevant_documents(query)
    
    def get_retriever(self):
        return self.vs_retriever

class CustomMultiQueryRetriever(MultiQueryRetriever):
    '''
    CustomMultiQueryRetriever is a wrapper around MultiQueryRetriever that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str):
        self.vector_store = VectorStoreRetriever(openai_key)
        prompt_obj = PromptTemplate(
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
        llm_chat_obj = ChatOpenAI(
            openai_api_key=openai_key,
            temperature=0
        )
        output_parser_obj = LineListOutputParser()
        self.llm_chain = LLMChain(llm=llm_chat_obj, prompt=prompt_obj, output_parser=output_parser_obj)
        super().__init__(
            retriever=self.vector_store.get_retriever(),
            llm_chain = self.llm_chain,
            parser_key='lines'
        )
    
    def add_functions(self, function_list: list[dict]):
        self.vector_store.add_functions(function_list)
    
    def find_functions(self, query: str):
        docs = super().get_relevant_documents(query)
        return docs

class CustomContextualCompressionRetriever(ContextualCompressionRetriever):
    '''
    CustomContextualCompressionRetriever is a wrapper around ContextualCompressionRetriever that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str):
        self.vector_store = VectorStoreRetriever(openai_key)
        llm = OpenAI(
            openai_api_key=openai_key,
            temperature=0
        )
        compressor = LLMChainExtractor.from_llm(llm)

        super().__init__(
            retriever=self.vector_store.get_retriever(),
            compressor=compressor,
            parser_key='lines'
        )
    
    def add_functions(self, function_list: list[dict]):
        self.vector_store.add_functions(function_list)
    
    def find_functions(self, query: str):
        docs = super().get_relevant_documents(query)
        return docs