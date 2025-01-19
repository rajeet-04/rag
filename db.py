import os
import shutil
from langchain.schema import Document
from emb import EmbeddingFunction
from langchain_chroma import Chroma
from to_md import convert_to_md

def main():

    # Get the folder path from the user.
    folder_path = input("📂 Enter the path to the folder containing documents: ").strip().replace("\\", "/").replace("\"", "")

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("❌ Invalid folder path. Please try again.")
        return

    # Ask for the Chroma database path.
    chroma_path = input("📂 Enter the path to store the Chroma database (default: ./chroma): ").strip()
    if not chroma_path:
        chroma_path = "./chroma"

    # Ask if the user wants to reset the database.
    reset = input("✨ Do you want to reset the database? (yes/no): ").strip().lower() == "yes"

    if reset:
        print("🗑️ Clearing the database...")
        clear_database(chroma_path)

    # Scan the folder for document files and convert them to Markdown.
    document_files = scan_folder_for_documents(folder_path)
    for file_path in document_files:
        print(f"📄 Converting file: {file_path}")
        try:
            # Convert the document to Markdown using the to_md function
            md_content = convert_to_md(file_path)

            # Save the converted Markdown temporarily
            temp_md_file = f"{file_path}.md"
            with open(temp_md_file, "w", encoding="utf-8") as f:
                f.write(md_content)

            # Add the Markdown file to the Chroma database
            add_to_chroma([Document(page_content=md_content, metadata={"source": file_path})], chroma_path)

            # Delete the temporary Markdown file after adding to Chroma
            os.remove(temp_md_file)

        except Exception as e:
            print(f"❌ Error converting {file_path}: {e}")

    print("✅ All documents processed and added to the database!")


def scan_folder_for_documents(folder_path: str) -> list[str]:
    """Scan the folder and find all document files."""
    document_extensions = [".pdf", ".docx", ".txt", ".html", ".epub", ".mobi", ".azw3", ".pptx", ".xlsx", ".odt", ".rtf", ".latex", ".tex"]
    document_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in document_extensions):
                document_files.append(os.path.join(root, file))

    return document_files




def add_to_chroma(chunks: list[Document], chroma_path: str):
    print(f"📦 Loading Chroma database from: {chroma_path}")
    embedding_function = EmbeddingFunction()  # Use the custom embedding function
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Add new documents to the database.
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    embeddings = embedding_function.embed_documents(texts)

    if embeddings is None or len(embeddings) == 0:
        print("❌ No embeddings generated. Aborting...")
        return

    # Add documents to the database
    db.add_texts(texts=texts, metadatas=metadatas)
    print("✅ Documents added successfully!")


def clear_database(chroma_path: str):
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)
        print(f"🗑️ Cleared database at: {chroma_path}")
    else:
        print("⚠️ No database found to clear.")


if __name__ == "__main__":
    main()
