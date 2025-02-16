import asyncio
from langchain_google_genai import GoogleGenerativeAI

model = GoogleGenerativeAI(
        model="gemini-pro",
        api_key="AIzaSyA0zV8_N1dCriPUIiiF-Nit1sZHLeYU-no",  # Replace with your actual key
        streaming = True
    )
prompt = [f"tell me a story"]

async def process_response():
    response = model.astream(prompt)
    async for chunk in response:  # Iterate through the generator
        yield chunk

print(asyncio.run(process_response()))