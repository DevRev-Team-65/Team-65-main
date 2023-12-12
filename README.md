# AI Agent 007

AI Agent 007 is a Streamlit application that uses OpenAI's GPT-3 model to answer queries based on a set of predefined functions. It uses the Langchain library for embeddings and chat models.

## Installation

1. Clone the repository.
2. Install the requirements using pip:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```
    streamlit run main.py
    ```

2. Open the provided local URL in your web browser.

3. Enter your OpenAI API Key in the sidebar. The key should start with "sk-".

4. Enter your query in the text area and click 'Submit'.

The application will use the `CustomMultiQueryRetriever` to find functions that are similar to the query. Then, it will use the `ChainOfThoughtComposer` to generate an answer based on the query and the retrieved functions.

After submitting a query, the application will display the response in JSON format. It will also display usage information in the sidebar, including the total number of tokens used, the number of prompt tokens, the number of completion tokens, and the total cost.

## Components

- `HuggingFaceEmbeddings`: This is used to generate embeddings for the functions.
- `ChatOpenAI`: This is a chat model from the Langchain library that uses OpenAI's GPT-3 model.
- `CustomMultiQueryRetriever`: This is used to find functions that are similar to the query.
- `ChainOfThoughtComposer`: This is used to generate an answer based on the query and the retrieved functions.

For more details and extensive documentation refer to [library README.md](#Documentation)

## Note

Please ensure that you have a valid OpenAI API Key to use this application. The key should start with "sk-".