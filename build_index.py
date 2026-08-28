import json
import time
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

KB_DIR = Path("knowledge_base")
INDEX_DIR = Path("index")
INDEX_DIR.mkdir(exist_ok=True)


def main():
    start = time.time()

    loader = DirectoryLoader(
        str(KB_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        separators=["\n## ", "\n# ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        source = chunk.metadata.get("source", "")
        chunk.metadata["title"] = Path(source).stem if source else f"chunk_{i}"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(INDEX_DIR))

    meta = {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "num_documents": len(documents),
        "num_chunks": len(chunks),
        "chunk_size": 600,
        "chunk_overlap": 100,
        "build_time_sec": round(time.time() - start, 2),
    }
    with open(INDEX_DIR / "index_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    query = "Кто такой Акакий?"
    results = vectorstore.similarity_search(query, k=2)

    example = {
        "query": query,
        "results": [
            {
                "title": doc.metadata.get("title"),
                "chunk_id": doc.metadata.get("chunk_id"),
                "content": doc.page_content[:300]
            }
            for doc in results
        ]
    }
    with open(INDEX_DIR / "search_example.json", "w", encoding="utf-8") as f:
        json.dump(example, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
