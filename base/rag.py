import os
import bs4
import csv
import uuid
import pandas as pd
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.utilities import BingSearchAPIWrapper

from base.search import load_websites
from base.vectorstore import create_vectorstore, split_docs
import os
import csv
import pandas as pd

def initialize_cache(cache_file='urls_cache.csv'):
    """Initialize the cache file with headers if it doesn't exist."""
    if not os.path.exists(cache_file):
        with open(cache_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['collection_name', 'url'])

def load_cached_urls(collection_name, cache_file='urls_cache.csv'):
    """Load cached URLs for a specific collection from a CSV file."""
    if not os.path.exists(cache_file):
        initialize_cache(cache_file)
    df_cached_urls = pd.read_csv(cache_file)
    df_cached_urls_of_collection = df_cached_urls[df_cached_urls['collection_name'] == collection_name]
    cached_urls = df_cached_urls_of_collection['url'].tolist()
    return cached_urls

def update_cache(new_urls, collection_name, cache_file='urls_cache.csv'):
    """Append new URLs for a specific collection to the CSV cache file."""
    if not new_urls:
        return  # If no new URLs to add, skip writing to the file
    
    with open(cache_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        for url in new_urls:
            writer.writerow([collection_name, url])


def search_and_store(query, db_collection_name, db_persist_directory='./vectorstore', chunk_size=1000, num_results=3):
    # Initialize the cache file if it doesn't exist
    # Perform the search query
    cache_file = f'{db_persist_directory}/urls_cache.csv'
    search = BingSearchAPIWrapper()
    search_results = search.results(query, num_results)
    url_link_list = [website_info['link'] for website_info in search_results]
    
    # Load cached URLs to avoid duplicates for the specific collection
    cached_urls = load_cached_urls(db_collection_name, cache_file)
    
    # Filter out URLs that are already in the cache
    new_urls = [url for url in url_link_list if url not in cached_urls]
    
    if not new_urls:
        print("All content is already in the database.")
        vectorstore = create_vectorstore(db_collection_name, 'sentence_transformer', db_persist_directory)
        return vectorstore

    try:
        docs = load_websites(new_urls)
    except Exception as e:
        # raise Exception(f'Error loading websites for concept {query}: {e}')
        print(f'Error loading websites for concept {query}: {e}')
        docs = []
    
    vectorstore = create_vectorstore(db_collection_name, 'sentence_transformer', db_persist_directory)
    splits = split_docs(docs, chunk_size=chunk_size, split_by='token')
    if len(splits) > 1:
        print(f"Splitting {len(docs)} documents into {len(splits)} chunks for storage.")
        vectorstore.add_documents(documents=splits)
        update_cache(new_urls, db_collection_name, cache_file)
        
    return vectorstore

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
