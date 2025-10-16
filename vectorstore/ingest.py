import os

class SimpleDocumentLoader:
    def __init__(self, directory_path="vectorstore/documents"):
        self.directory_path = directory_path

    def load_documents(self):
        text_files = []
        # List all .txt files in the folder
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        text_files.append({"file_path": file_path, "content": content})
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")
        print(f"Loaded {len(text_files)} text documents.")
        return text_files

    def split_into_chunks(self, text_files, chunk_size=500, chunk_overlap=300):
        chunks = []
        for doc in text_files:
            text = doc["content"]
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk_text = text[start:end]
                chunks.append( chunk_text)
                start += chunk_size - chunk_overlap
        print(f"Split into {len(chunks)} text chunks.")
        return chunks

def get_split_chunks():
    loader = SimpleDocumentLoader()
    docs = loader.load_documents()
    split_docs = loader.split_into_chunks(docs)
    return split_docs

# Load and split
sc = get_split_chunks()
