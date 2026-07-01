# RAGForge AI

RAGForge AI is a production-style Retrieval-Augmented Generation platform for uploading documents, parsing content, chunking text, indexing knowledge, retrieving relevant context, generating AI answers, enforcing citations, and evaluating answer quality.

## Features

- Workspace management
- Document upload and deletion
- PDF, DOCX, PPTX, TXT, and Markdown parsing
- Sentence-aware chunking pipeline
- SQLite metadata database
- BM25 keyword retrieval
- ChromaDB vector storage
- FAISS vector index
- Hybrid retrieval using BM25 + vector search
- Cross-encoder reranking
- Citation-enforced AI answers
- Ollama-based local LLM generation
- Search analytics
- Evaluation pipeline
- Pytest smoke tests

## Tech Stack

- Python
- Streamlit
- SQLite
- PyMuPDF
- python-docx
- python-pptx
- Sentence Transformers
- ChromaDB
- FAISS
- rank-bm25
- Ollama
- Pytest
- Ruff

## Project Structure

```text
RAGForge-AI/
├── app.py
├── app_pages/
├── database/
├── document_processing/
├── evaluation/
├── llm/
├── models/
├── retrieval/
├── services/
├── storage/
├── tests/
├── ui/
├── vector_store/
├── requirements.txt
└── README.md