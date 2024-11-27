import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader, AsyncChromiumLoader, AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer, Html2TextTransformer

from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_community.utilities import BingSearchAPIWrapper


class BeautifulSoupTransformer:
    def transform_documents(self, docs):
        transformed_docs = []
        for doc in docs:
            try:
                soup = BeautifulSoup(doc.page_content, 'html.parser')

                main_content = ""
                if soup.title:
                    main_content += soup.title.get_text() + "\n\n"
                
                for paragraph in soup.find_all('p'):
                    main_content += paragraph.get_text() + "\n"
                
                if main_content.strip():
                    doc.page_content = main_content
                    transformed_docs.append(doc)
            except Exception as e:
                print(f"Error processing document: {e}")

        return transformed_docs

def load_websites(urls, loader='html', transformer='beautiful_soup'):
    assert isinstance(urls, list) or isinstance(urls, str)
    assert loader in ['html', 'chromium']
    assert transformer in ['beautiful_soup', 'html2text']
    
    if not isinstance(urls, list):
        urls = [urls]
    
    if loader == 'html':
        loader = AsyncHtmlLoader(urls)
    elif loader == 'chromium':
        loader = AsyncChromiumLoader(urls)
    
    docs = loader.load()

    if transformer == 'beautiful_soup':
        transformer = BeautifulSoupTransformer()
    elif transformer == 'html2text':
        transformer = Html2TextTransformer()
    
    docs = transformer.transform_documents(docs)
    return docs


def bing_search(query, offset=0, count=50, safeSearch="Strict"):
    subscription_key = os.environ["BING_SUBSCRIPTION_KEY"]
    search_url = os.environ["BING_SEARCH_URL"]

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": query, 
        "textDecorations": False, 
        "textFormat": "Raw", 
        "count": count, 
        "safeSearch": safeSearch,
        "offset": offset
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results

def browse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.body.get_text(separator='\n', strip=True)
        return text
    return None
