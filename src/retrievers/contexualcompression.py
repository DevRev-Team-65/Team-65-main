from .vectorstore import VectorStoreRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


class CustomContextualCompressionRetriever(ContextualCompressionRetriever):
    '''
    CustomContextualCompressionRetriever is a wrapper around ContextualCompressionRetriever that allows for easy addition of functions and queries
    '''
    def __init__(self, llm, embeddings, name: str, init_functions: list[dict]):
        name = "ccr_" + name
        vector_store = VectorStoreRetriever(embeddings, name, init_functions)
        compressor = LLMChainExtractor.from_llm(llm)
        super().__init__(
            base_retriever=vector_store.get_retriever(),
            base_compressor=compressor,
            parser_key='lines'
        )
    
    def add_functions(self, function_list: list[dict]):
        self.base_retriever.add_functions(function_list)
    
    def find_functions(self, query: str):
        docs = super().get_relevant_documents(query)
        return docs