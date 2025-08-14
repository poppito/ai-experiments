from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core import Settings
import os


# LLM
Settings.llm = Ollama(model="llama3.2", request_timeout=30.0)  # Use local Ollama LLM


# embeddings model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# When we load data, this seems to cause the process to fork resulting in a warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
INDEX_DIR = "./index_storage"

def persist_index():
    if os.path.exists(INDEX_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context=storage_context)
        return index
    else:
        books = index_docs(path="./data", type="books", purpose="Fictional books of various kinds with supernatural themes")
        documents = []
        documents.extend(books)
        index = VectorStoreIndex.from_documents(documents=documents)
        index.storage_context.persist(persist_dir=INDEX_DIR)
        return index


def index_docs(path, type, purpose):
    documents = []
    for filename in os.listdir(path=path):
        file_path = os.path.join(path, filename)
        print("indexing " + file_path)
        if os.path.isfile(file_path):
            doc = SimpleDirectoryReader(input_files=[file_path]).load_data()
            for d in doc:
                d.metadata = { "source": filename, "type": "ebook", type: type, purpose: purpose}
            documents.extend(doc)
    return documents


def run_query(index):
    query_engine = index.as_query_engine()
    print("Type your query or 'exit' to quit")
    while True:
        query = input("> ")
        if query.lower() == "exit":
            break
        response = query_engine.query(query)  # No need for response_mode
        print(response)
        print("\nCitations:")
        if hasattr(response, "source_nodes") and response.source_nodes:
            for source in response.source_nodes:
                print(f"- {source.node.metadata.get('source', 'Unknown')}")
        else:
            print("No citations available.")

if __name__ == "__main__":
    index = persist_index()
    run_query(index = index)