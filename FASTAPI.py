from fastapi import FastAPI, HTTPException
import RAG_FINAL as rag  
from fastapi import UploadFile
from langchain_google_genai import GoogleGenerativeAI  
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable
from pydantic import BaseModel
import asyncio
from langchain_core.output_parsers import StrOutputParser
import json

app = FastAPI()

documents_store = {}
namespace_store = {}

def streaming_function(query: str, perfect_match: str):
    callback = AsyncIteratorCallbackHandler()

    model = GoogleGenerativeAI(
        model="gemini-1.5-pro",
        api_key="AIzaSyA0zV8_N1dCriPUIiiF-Nit1sZHLeYU-no", 
        streaming=True,
        verbose=False,
        callbacks=[callback],
    )

    prompt = (
        f"Using the following text as a reference: {perfect_match}, provide a comprehensive answer to the query: {query}. "
        "Reflect on the query multiple times to understand it properly before answering. "
        "Extract relevant details, refine information for clarity, and enhance where necessary. "
        "If no relevant information is found, explicitly state: 'The document does not contain information related to the query.'"
    )

    return model.astream(prompt)

    

@app.post("/youtube")  # Corrected route name
def youtube(video_url: str):
    global documents_store, namespace_store
    try:
        documents, namespace = rag.file_loader(video_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing YouTube link: {e}")

    documents_store["latest_documents"] = documents
    namespace_store["latest_namespace"] = namespace
    return {"message": "YouTube link processed successfully", "namespace": namespace}


@app.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()

    with open(file.filename, "wb") as f:
        f.write(content)

    global documents_store, namespace_store
    documents, name_space = rag.file_loader(file.filename)

    documents_store["latest_documents"] = documents
    namespace_store["latest_namespace"] = name_space
    return {"message": "File uploaded successfully", "namespace": name_space}


@app.get("/query")
async def query(question: str):  

    if "latest_namespace" not in namespace_store or "latest_documents" not in documents_store:
        return {"error": "No file uploaded. Please upload a file first."}

    name = namespace_store["latest_namespace"]
    documents = documents_store["latest_documents"]

    answer = rag.response_loader(question, name, documents) 
    async def generate_response():  
        async for chunk in streaming_function(question, answer): 
            if chunk:  
                yield f"{chunk.strip()}\n" 
                await asyncio.sleep(0.05) 

    return StreamingResponse(generate_response(), media_type="text/plain")