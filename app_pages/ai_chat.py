import streamlit as st

from services.answer_service import AnswerService
from services.workspace_service import WorkspaceService


def render_citation_card(citation: dict):
    with st.container(border=True):
        st.markdown(f"### Source {citation['citation_id']}")
        st.write(f"**File:** {citation['file_name']}")
        st.write(f"**Type:** `{citation['file_type']}`")
        st.write(f"**Chunk:** `{citation['chunk_index']}`")
        st.write(f"**Method:** `{citation['retrieval_method']}`")

        with st.expander("View cited chunk"):
            st.write(citation["chunk_text"])


def render_ai_chat():
    workspace_service = WorkspaceService()
    answer_service = AnswerService()

    st.title("💬 AI Chat")
    st.caption("Ask questions over your uploaded documents with citation-enforced answers.")

    workspaces = workspace_service.get_all_workspaces()

    if not workspaces:
        st.info("Create a workspace and upload documents first.")
        return

    workspace_map = {workspace.name: workspace.id for workspace in workspaces}

    selected_workspace = st.selectbox(
        "Workspace",
        workspace_map.keys(),
    )

    question = st.text_area(
        "Ask a question",
        placeholder="Example: What is Hybrid Retrieval?",
        height=120,
    )

    if st.button("Ask RAGForge AI", use_container_width=True, type="primary"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Retrieving, reranking, generating, and enforcing citations..."):
            try:
                response = answer_service.answer_question(
                    question=question,
                    workspace_id=workspace_map[selected_workspace],
                )

                st.subheader("Answer")
                st.write(response["answer"])

                st.subheader("Citations")

                if not response["citations"]:
                    st.info("No citations found.")
                else:
                    for citation in response["citations"]:
                        render_citation_card(citation)

            except Exception as error:
                st.error(f"Could not generate answer: {error}")