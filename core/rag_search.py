import chromadb
import uuid
from vectorstore.ingest import get_split_chunks
from typing import List
class VectorDatabase:
    def __init__(self):
        # In-memory Chroma client
        self.client = chromadb.Client()

        # Create or get collection (no embedding_function needed)
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"hnsw:space": "cosine"}
        )

    def store_embeddings(self, chunk_list:List):
        """
        Stores plain text documents into ChromaDB.
        Chroma automatically generates embeddings internally.
        """

        # texts = [doc.page_content for doc in chunk_list]
        ids = [str(uuid.uuid4()) for _ in chunk_list]

        self.collection.add(ids=ids, documents=chunk_list)
        print(f"✅ Stored {len(chunk_list)} chunks in ChromaDB (temporary, auto-embedded)!")

    def similarity_search(self, query, top_k=3, threshold=0.55):
        """
        Searches for similar documents using Chroma’s built-in embedding logic.
        """
        sc= get_split_chunks()

        self.store_embeddings(sc)
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["distances", "documents"]
        )
        print(results)

        if not results["documents"] or not results["documents"][0]:
            return None

        docs = results["documents"][0]
        sims = [1 - d for d in results["distances"][0]]
        print(f"🔍 Similarities: {sims}")

        # Filter docs above threshold
        filtered = [(doc, sim) for doc, sim in zip(docs, sims) if sim >= threshold]
        if not filtered:
            return None

        docs, sims = zip(*filtered)
        return list(docs), list(sims)
