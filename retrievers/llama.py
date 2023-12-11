import json
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI as OpenAILM
from langchain.schema import Document

class LlamaIndexRetriever:
    '''
    LlamaIndexRetriever is a wrapper around VectorStoreIndex that allows for easy addition of functions and queries
    '''
    def __init__(self, openai_key: str, name: str, init_functions: list[dict]):
        self.documents = 0
        for i,f in enumerate(init_functions):
            init_functions[i] = Document(page_content=json.dumps(f), metadata={"index": self.documents})
            self.documents += 1
        llm = OpenAILM(
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