import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def ingest_docs():
    # Load the document
    loader = TextLoader("info.txt")
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Initialize Vertex AI embeddings
    embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

    # Create and persist the vector store
    persist_directory = "db"
    if os.path.exists(persist_directory):
        import shutil
        shutil.rmtree(persist_directory)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Ingested {len(docs)} chunks into {persist_directory} using Vertex AI embeddings")

if __name__ == "__main__":
    ingest_docs()
