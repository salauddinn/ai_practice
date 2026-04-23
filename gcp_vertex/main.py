from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
import os
project = os.getenv('GOOGLE_CLOUD_PROJECT')

def main():  
    # Initialize model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        vertexai=True,
        project=project
    )

    # Ask a question
    response = llm.invoke("What is the capital of France?")

    print(response.content)


if __name__ == "__main__":
    main()
