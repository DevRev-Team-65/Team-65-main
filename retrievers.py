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
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI

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

class LlamaIndexRetriever:
    '''
    LlamaIndexRetriever is a wrapper around VectorStoreIndex that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str, name: str, init_functions: list[dict]):
        self.documents = 0
        for i,f in enumerate(init_functions):
            init_functions[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1
        llm = OpenAI(
            api_key=openai_key,
            temperature=0
        )
        service_context = ServiceContext.from_defaults(llm=llm)
        self.index = VectorStoreIndex.from_documents(
            init_functions,
            service_context=service_context
        )
        self.vs_name = name
        self.query_engine = self.index.as_query_engine()
    
    def add_functions(self, function_list: list[dict]):
        for i,f in enumerate(function_list):
            function_list[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1
        self.index.add_documents(function_list)
        self.index.save_local(self.vs_name)
    
    def find_functions(self, query: str):
        response = self.query_engine.query(query)
        return response

class VectorStoreRetriever:
    '''
    VectorStore is a wrapper around FAISS that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str, name: str, init_functions: list[dict]):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_key,
        )

        self.init_functions = init_functions.copy()
        self.documents = 0
        for i,f in enumerate(init_functions):
            self.init_functions[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1

        #create a vector store
        try:
            self.vector_store = FAISS.load_local(name, self.embeddings)
        except:
            #no local store
            self.vector_store = FAISS.from_documents(
                self.init_functions,
                self.embeddings
            )
            self.vector_store.save_local(name)
        self.vs_name = name
        self.vs_retriever = self.vector_store.as_retriever()
        self.documents = len(init_functions)
    
    def add_functions(self, function_list: list[dict]):
        for i,f in enumerate(function_list):
            function_list[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1
        self.vector_store.add_documents(function_list)
        self.vector_store.save_local(self.vs_name)
    
    def find_functions(self, query: str):
        return self.vs_retriever.get_relevant_documents(query)
    
    def get_retriever(self):
        return self.vs_retriever

class CustomMultiQueryRetriever(MultiQueryRetriever):
    '''
    CustomMultiQueryRetriever is a wrapper around MultiQueryRetriever that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str, name: str, init_functions: list[dict]):
        name = "mqr_" + name
        prompt_obj = PromptTemplate(
            input_variables=["question"],
            template="""Your task is to break down the question into a list different steps.
            The steps should be as specific as possible. Your goal is to have the task broken
            minimum number of simpler atomic steps.
            
            Example question: Prioritize my P0 issues and add them to the current sprint
            Example answer:
            1. Get my id
            2. Find my P0 issues using id
            3. Prioritize my P0 issues from #2
            4. Get the current sprint id
            5. Add issues from #2 to the sprint from #4

            Now solve the following question
            Original question: {question}""",
        )
        vector_store = VectorStoreRetriever(openai_key, name, init_functions)
        llm_chat_obj = ChatOpenAI(
            openai_api_key=openai_key,
            temperature=0
        )
        output_parser_obj = LineListOutputParser()
        llm_chain = LLMChain(llm=llm_chat_obj, prompt=prompt_obj, output_parser=output_parser_obj)
        super().__init__(
            retriever=vector_store.get_retriever(),
            llm_chain = llm_chain,
            parser_key='lines'
        )
    
    def add_functions(self, function_list: list[dict]):
        self.retriever.add_functions(function_list)
    
    def find_functions(self, query: str):
        docs = super().get_relevant_documents(query)
        return docs

class CustomContextualCompressionRetriever(ContextualCompressionRetriever):
    '''
    CustomContextualCompressionRetriever is a wrapper around ContextualCompressionRetriever that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str, name: str, init_functions: list[dict]):
        name = "ccr_" + name
        vector_store = VectorStoreRetriever(openai_key, name, init_functions)
        llm = OpenAI(
            openai_api_key=openai_key,
            temperature=0
        )
        compressor = LLMChainExtractor.from_llm(llm)
        super().__init__(
            base_retriever=vector_store.get_retriever(),
            base_compressor=compressor,
            parser_key='lines'
        )
    
    def add_functions(self, function_list: list[dict]):
        self.retriever.add_functions(function_list)
    
    def find_functions(self, query: str):
        docs = super().get_relevant_documents(query)
        return docs
