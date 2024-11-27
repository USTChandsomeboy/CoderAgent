# import chromadb
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from config import *

from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter

from langchain_text_splitters import TokenTextSplitter


def split_docs(docs, chunk_size=1000, chunk_overlap=0, split_by="token"):
    if split_by == "character":
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    elif split_by == "recursive_character":
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    elif split_by == "token":
        text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        raise ValueError(f"Unknown split_by value: {split_by}")
    splits = text_splitter.split_documents(docs)
    return splits


def create_openai_embeddings():
    from langchain_openai import AzureOpenAIEmbeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.environ["AZURE_EMBEDDINGS_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_EMBEDDINGS_API_VERSION"],
    )
    return embeddings

def create_sentence_transformer_embeddings():
    model_name = "sentence-transformers/all-mpnet-base-v2"
    # model_kwargs = {'device': 'gpu'}
    # encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        # model_kwargs=model_kwargs,
        # encode_kwargs=encode_kwargs
    )
    return embeddings

def create_embeddings(backbone="sentence_transformer"):
    if backbone == "sentence_transformer":
        return create_sentence_transformer_embeddings()
    elif backbone == "openai":
        return create_openai_embeddings()
    else:
        raise ValueError(f"Unsupported backbone: {backbone}")

def create_vectorstore(
        collection_name,
        embeddings_type='sentence_transformer',
        persist_directory='./chroma_db', 
    ):
    # chroma_client = chromadb.PersistentClient(path=save_dir)
    embeddings = create_embeddings(embeddings_type)
    try:
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
    except Exception as e:
        print(f"Collection {collection_name} already exists. Using the existing collection.")
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
    print(f'There are {vector_store._collection.count()} records in the collection')
    return vector_store
