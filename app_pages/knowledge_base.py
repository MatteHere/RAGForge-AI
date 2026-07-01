import re
import time

import streamlit as st

from database.search_log_repository import SearchLogRepository
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import CrossEncoderReranker
from retrieval.vector_retriever import VectorRetriever
from services.workspace_service import WorkspaceService


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def preview_text(text: str, max_chars: int = 450):
    text = clean_text(text)

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "..."


def render_result(result, rank, max_score):
    percentage = 0

    score = result.get("reranker_score", result.get("score", 0))

    if max_score > 0:
        percentage = round((score / max_score) * 100)

    icon = "📄"
    file_type = result.get("file_type", "")

    if file_type == ".pdf":
        icon = "📕"
    elif file_type == ".docx":
        icon = "📘"
    elif file_type == ".pptx":
        icon = "📙"
    elif file_type == ".txt":
        icon = "📄"

    file_name = result.get("file_name", f"Document {result['document_id']}")
    token_count = result.get("token_count", "N/A")
    status = result.get("document_status", "indexed")

    with st.container(border=True):
        col1, col2 = st.columns([8, 2])

        with col1:
            st.markdown(
                f"""
### {icon} {file_name}

**Chunk #{result["chunk_index"]}**
"""
            )

        with col2:
            st.metric("Relevance", f"{percentage}%")

        st.progress(max(0, min(percentage / 100, 1)))

        st.markdown(preview_text(result["chunk_text"]))

        info1, info2, info3 = st.columns(3)

        with info1:
            st.caption(f"Method: {result['retrieval_method']}")

        with info2:
            st.caption(f"Tokens: {token_count}")

        with info3:
            st.caption(f"Status: {status}")

        sources = result.get("retrieval_sources")
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")

        if "reranker_score" in result:
            st.caption(f"Reranker Score: {result['reranker_score']:.4f}")

        with st.expander("View Complete Chunk"):
            st.write(result["chunk_text"])


def render_knowledge_base():
    workspace_service = WorkspaceService()
    bm25 = BM25Retriever()
    vector = VectorRetriever()
    hybrid = HybridRetriever()
    reranker = CrossEncoderReranker()
    search_log_repository = SearchLogRepository()

    st.title("🔍 Knowledge Base")
    st.caption(
        "Search uploaded document chunks using BM25, Vector Search, Hybrid Retrieval, or Hybrid + Reranking."
    )

    workspaces = workspace_service.get_all_workspaces()

    if not workspaces:
        st.info("Create a workspace first.")
        return

    workspace_map = {workspace.name: workspace.id for workspace in workspaces}

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        query = st.text_input(
            "Search",
            placeholder="Example: hybrid retrieval",
        )

    with col2:
        workspace = st.selectbox(
            "Workspace",
            workspace_map.keys(),
        )

    with col3:
        retrieval_method = st.selectbox(
            "Retrieval",
            ["BM25", "Vector", "Hybrid", "Hybrid + Rerank"],
        )

    if st.button("Search", use_container_width=True, type="primary"):
        if not query.strip():
            st.warning("Please enter a search query.")
            return

        workspace_id = workspace_map[workspace]

        start = time.time()

        if retrieval_method == "BM25":
            results = bm25.search(query=query, workspace_id=workspace_id, top_k=5)
            method_name = "bm25"

        elif retrieval_method == "Vector":
            results = vector.search(query=query, workspace_id=workspace_id, top_k=5)
            method_name = "vector"

        elif retrieval_method == "Hybrid":
            results = hybrid.search(query=query, workspace_id=workspace_id, top_k=5)
            method_name = "hybrid"

        else:
            initial_results = hybrid.search(query=query, workspace_id=workspace_id, top_k=10)
            results = reranker.rerank(query=query, results=initial_results, top_k=5)
            method_name = "hybrid+rerank"

        elapsed_ms = round((time.time() - start) * 1000, 2)

        search_log_repository.create_search_log(
            workspace_id=workspace_id,
            query=query.strip(),
            retrieval_method=method_name,
            result_count=len(results),
            response_time_ms=elapsed_ms,
        )

        if not results:
            st.warning("No relevant chunks found.")
            return

        score_key = "reranker_score" if "reranker_score" in results[0] else "score"
        max_score = max(result.get(score_key, 0) for result in results)

        st.success(
            f"Found {len(results)} relevant chunk(s) using {retrieval_method} in {elapsed_ms} ms"
        )

        st.divider()

        for index, result in enumerate(results, start=1):
            render_result(result, index, max_score)