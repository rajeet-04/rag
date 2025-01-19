import requests
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from emb import EmbeddingFunction

CHROMA_PATH = "chroma"

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = EmbeddingFunction()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=50)
    print(results)
    if not results:
        print("No relevant documents found.")
        return None

    # Prepare context text from documents
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template("""
    Answer the question based on the following context:

    {context}

    --- 

    Answer the question based on the above context: {question}
    """)

    # Construct the prompt
    prompt = prompt_template.format(context=context_text, question=query_text)

    return prompt


def send_to_local_server(prompt):
    # Prepare the JSON body for the request
    json_body = {
        "stream": False,
        "n_predict": 350,
        "temperature": 0.8,
        "stop": ["</s>", "Llama:", "User:"],
        "repeat_last_n": 78,
        "repeat_penalty": 1.18,
        "top_k": 40,
        "top_p": 1,
        "min_p": 0.05,
        "tfs_z": 1,
        "typical_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "mirostat": 2,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "prompt": prompt
    }

    # Headers
    headers = {
        "accept-language": "en-US,en",
        "cache-control": "no-cache",
        "content-type": "application/json"
    }

    # Send the request to the local server
    response = requests.post("http://127.0.0.1:8080/completion", json=json_body, headers=headers, stream=False)

    return response


def main():
    while True:
        # Get the query from the user
        inp = input('Enter your query: ')

        if inp.lower() == "exit":
            break

        print(f"Sending prompt: {inp}")

        # Step 1: Perform RAG to retrieve relevant context from the database
        rag_prompt = query_rag(inp)
        if not rag_prompt:
            print("No relevant context found for the query.")
            continue

        # Step 2: Send the generated prompt to the local server
        response = send_to_local_server(rag_prompt)

        # Parse the response
        if response.status_code == 200:
            response_text = response.json().get('content', '')
            print(f"Response: {response_text}")
        else:
            print("Failed to get response from the local server.")


if __name__ == "__main__":
    main()
