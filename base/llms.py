import os
import logging

from dotenv import load_dotenv
load_dotenv(override=True)

temperature = 0.7


def create_hf_llm(model_type="prometheus"):
    from langchain_huggingface import HuggingFacePipeline
    if model_type == "prometheus":
        hf_llm = HuggingFacePipeline(
            model_id="prometheus-eval/prometheus-7b-v2.0",
            # task="text-generation",
        )
    elif model_type == "gpt2":
        hf_llm = HuggingFacePipeline(
            model_id="gpt2",
            task="text-generation",
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    return hf_llm

def create_llama_llm():
    from langchain_ollama import ChatOllama
    llama_llm = ChatOllama(
        model="llama3.2",
        temperature=temperature,
        max_tokens=50000,
    )
    return llama_llm

def create_gpt4o_llm(deployment=None):
    from langchain_openai import AzureChatOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    if deployment:
        os.environ["AZURE_DEPLOYMENT"] = deployment
    
    print('='*80)
    print(os.environ["AZURE_OPENAI_ENDPOINT"])
    print(os.environ["AZURE_API_VERSION"])
    print(os.environ["AZURE_DEPLOYMENT"])
    print('='*80)
    llm = AzureChatOpenAI(
        azure_ad_token_provider=token_provider,
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_API_VERSION"],
        azure_deployment=os.environ["AZURE_DEPLOYMENT"],
        temperature=temperature,
        # max_tokens=50000,
    )
    return llm

def create_llm(backbone="gpt4o", deployment=None):
    if backbone == "gpt4o":
        logging.info("Creating Azure OpenAI LLM")
        return create_gpt4o_llm(deployment)
    elif backbone == "llama":
        return create_llama_llm()
    else:
        raise ValueError(f"Unsupported backbone: {backbone}")


if __name__ == "__main__":
    llm = create_gpt4o_llm()
    llm = create_llama_llm()
    query = "How to create a chatbot"
    response = llm.invoke(query)
    print(response)
