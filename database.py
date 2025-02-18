from chromadb import Client

# Initialize ChromaDB Client
client = Client()
collection = client.get_or_create_collection(name="invoices")


def store_invoice(invoice_id, content, source):
    """Stores an invoice in ChromaDB"""
    collection.add(
        ids=[invoice_id],
        documents=[content],
        metadatas=[{"source": source}]
    )
    print(f"✅ Invoice {invoice_id} stored successfully.")


def search_invoices(query_text, top_k=3):
    """Search invoices in ChromaDB"""
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )

    # Debugging statements
    print(f"🔎 Search Query: {query_text}")
    print(f"🔍 Search Results: {results}")

    return results if results else {"documents": []}

# Test storing an invoice (Uncomment to manually test)
# store_invoice("test123", "This is a sample invoice for debugging.", "Test Source")
