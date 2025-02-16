from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAI
import openai
from langchain_openai import AzureOpenAIEmbeddings
import pymupdf4llm as mupdf
from langchain.schema import Document
import whisper
import yt_dlp
from langchain_experimental.text_splitter import SemanticChunker



openai.api_type = "Azure"
openai.api_key = "D7lXAaH2pucZEL5XmNmKskLgiMfnstppi7MqjouRQhyIK2EMxNs1JQQJ99BBACYeBjFXJ3w3AAABACOGWCUd"
openai.api_base = "https://my-openai-service-asjad.openai.azure.com/"
chunk_size = 500
chunk_overlap = 50


pc = Pinecone(api_key="pcsk_2QQPsk_62HtsrmqT6u75a9QD64mHinG8PMsyBLcP9s62ceadbmx2RbMf8kYNt7Hrqa1Kt3")

index_name = "quickstart"

""" if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1536,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
 """
index = pc.Index(index_name)
print(pc.list_indexes())

llm = GoogleGenerativeAI(model="gemini-pro", api_key="AIzaSyA0zV8_N1dCriPUIiiF-Nit1sZHLeYU-no",streaming = True)

name_space = {}
def file_loader(file_path):
    
    if file_path.endswith("txt"):

        name_space["latest"] = "ns1"

        chat_data = mupdf.to_markdown(file_path,page_chunks=True)

        documents=[]
        
        for page in chat_data:
            
            doc = (Document(page_content=page["text"]))
            
            documents.append(doc)

        return text_splitter(documents),name_space["latest"]
    
    elif "www.youtube.com" in file_path:
        global chunk_size, chunk_overlap
        chunk_size = 1000
        chunk_overlap = 100
        ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.mp3",
        "quiet": True,
    }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([file_path])
        documents = []
        model = whisper.load_model("small.en")  
        result = model.transcribe("audio.mp3") 
        documents = [Document(page_content=result["text"])]

        name_space["latest"] = "ns2"

        return text_splitter(documents),name_space["latest"]

    else :
        chat_data = mupdf.to_markdown(file_path,page_chunks=True)
        extracted_images=[]
        documents=[]
        for page in chat_data:
            if "image" in page and page["image"]:
                for img_index,img in enumerate (page["image"]):
                    img_text = img.get("text","").strip()
                    if img_text:
                        extracted_text = Document(page_content = f"\\Image {img_index+1} \n {img_text}")
                        extracted_images.append(extracted_text)

            doc = (Document(page_content=page["text"]))
            documents.append(doc)
        documents.extend(extracted_images)

        name_space["latest"] = "ns3"
        

        return text_splitter(documents),name_space["latest"]

def text_splitter(data):
    splitter = SemanticChunker(embeddings,breakpoint_threshold_type = "percentile")
    text_list = [doc.page_content for doc in data]
    return splitter.create_documents(text_list)

print("\nfile Loaded Successfully\n")


embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://my-openai-service-asjad.openai.azure.com/",
    api_key= "D7lXAaH2pucZEL5XmNmKskLgiMfnstppi7MqjouRQhyIK2EMxNs1JQQJ99BBACYeBjFXJ3w3AAABACOGWCUd",
    model="text-embedding-ada-002",  
    deployment="text-embedding-ada-002",  
    api_version="2023-12-01-preview",
    
)

               

def response_loader(query,name_space,data):

    print(data)

    vectors = []

    for i, doc in enumerate(data):
        embedded_text = embeddings.embed_query(doc.page_content)
        vectors.append((str(i), embedded_text, {"text": doc.page_content}))
    
    
    index.upsert(vectors, namespace=name_space)
    query_vector = embeddings.embed_query(query)

    search_result = index.query(vector=query_vector, top_k=10, include_metadata=True,namespace=name_space)

    best_match = search_result["matches"][0]
    perfect_match = best_match["metadata"]["text"] 
     #response = llm.invoke(f"Using the following text as a reference: {perfect_match}, provide a comprehensive and well-structured answer to the query: {query} reflect on the query 2 to 3 times understand its meaning properly and then answer it. Extract as much relevant detail as possible from the document, refine the information for clarity and completeness, and enhance it where necessary. If no relevant information is found, explicitly state: 'The document does not contain information related to the query.'")

    return perfect_match


