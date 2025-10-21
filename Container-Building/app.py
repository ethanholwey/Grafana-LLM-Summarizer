from fastapi import FastAPI
from dotenv import load_dotenv
import os
from openai import OpenAI
from collections import Counter
import re

app = FastAPI()

@app.get("/")
def root():
    # Load environment variables from .env
    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    vector_store = client.beta.vector_stores.create(  # Create vector store
        name="File DB",
    )

    # Debug print file contents
    with open("test.txt", "r", encoding="utf-8") as f:
        contents = f.read()
        print("DEBUG: File contents:\n", contents)

    # Upload file to vector store
    with open("test.txt", "rb") as f:
        client.beta.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=f
        )

    # Create assistant to read from the vector store
    assistant = client.beta.assistants.create(
        name="Content retrieval Assistant",
        instructions="You are a helpful assistant. Use the uploaded file to answer questions.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # then start a thread to ask about your file
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What does this file say: "
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    LLM_response = None
    for msg in messages.data:
        print(f"{msg.role}: {msg.content[0].text.value}")
        if msg.role == "assistant":
            LLM_response = msg.content[0].text.value
            print(LLM_response)
            break

    return {msg.role: LLM_response}

@app.get("/count")
def keyword_count():

    with open("test.txt", "r", encoding="utf-8") as f:
        contents = f.read()

    keywords = ["good", "critical", "failed","warning"]
    word_counts = Counter()

    for word in keywords:
        word_counts[word] = len(re.findall(rf"\b{word}\b", contents, re.IGNORECASE))

    grafana_data = [{"keyword": k, "count": v} for k, v in word_counts.items()]

    return grafana_data


@app.get("/file")
def read_file():
    with open("test.txt", "r", encoding="utf-8") as f:
        contents = f.read()
    return contents
