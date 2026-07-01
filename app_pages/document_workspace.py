import streamlit as st

from services.chunk_service import ChunkService
from services.document_service import DocumentService
from services.indexing_service import IndexingService
from services.workspace_service import WorkspaceService


def format_file_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"

    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"

    return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def render_document_card(document, document_service: DocumentService, chunk_service: ChunkService):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">📄 {document.file_name}</div>
            <div class="metric-note"><b>Type:</b> {document.file_type}</div>
            <div class="metric-note"><b>Status:</b> {document.status}</div>
            <div class="metric-note"><b>Size:</b> {format_file_size(document.file_size)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Chunk Document",
            key=f"chunk_document_{document.id}",
            disabled=document.status != "parsed",
        ):
            try:
                chunk_count = chunk_service.chunk_document(document.id)
                st.success(f"Document chunked into {chunk_count} chunk(s).")
                st.rerun()
            except Exception as error:
                st.error(f"Could not chunk document: {error}")

    with col2:
        if st.button(
            "Delete Document",
            key=f"delete_document_{document.id}",
            type="secondary",
        ):
            try:
                document_service.delete_document(document.id)
                st.success("Document deleted successfully.")
                st.rerun()
            except Exception as error:
                st.error(f"Could not delete document: {error}")


def render_document_workspace():
    workspace_service = WorkspaceService()
    document_service = DocumentService()
    chunk_service = ChunkService()
    indexing_service = IndexingService()

    st.markdown(
        """
        <div class="main-title">Document Workspace</div>
        <div class="main-subtitle">
            Manage workspaces, upload documents, chunk content, and index knowledge into vector databases.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">Create Workspace</div>', unsafe_allow_html=True)

    with st.form("create_workspace_form", clear_on_submit=True):
        workspace_name = st.text_input("Workspace Name")
        workspace_description = st.text_area("Workspace Description")
        submitted = st.form_submit_button("Create Workspace")

        if submitted:
            try:
                workspace_service.create_workspace(
                    name=workspace_name,
                    description=workspace_description,
                )
                st.success("Workspace created successfully.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Could not create workspace: {error}")

    workspaces = workspace_service.get_all_workspaces()

    st.markdown('<div class="section-heading">Upload Documents</div>', unsafe_allow_html=True)

    if not workspaces:
        st.warning("Create a workspace before uploading documents.")
        return

    workspace_options = {workspace.name: workspace.id for workspace in workspaces}

    selected_workspace_name = st.selectbox(
        "Select Workspace",
        list(workspace_options.keys()),
    )

    selected_workspace_id = workspace_options[selected_workspace_name]

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, PPTX, TXT, or Markdown files",
        type=["pdf", "docx", "pptx", "txt", "md"],
        accept_multiple_files=True,
    )

    if st.button("Save Uploaded Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:
            saved_count = 0

            for uploaded_file in uploaded_files:
                try:
                    document_service.save_uploaded_file(
                        uploaded_file=uploaded_file,
                        workspace_id=selected_workspace_id,
                    )
                    saved_count += 1
                except ValueError as error:
                    st.error(f"{uploaded_file.name}: {error}")
                except Exception as error:
                    st.error(f"{uploaded_file.name}: {error}")

            if saved_count > 0:
                st.success(f"{saved_count} document(s) uploaded successfully.")
                st.rerun()

    st.markdown('<div class="section-heading">Workspace Library</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">View, chunk, index, and manage uploaded documents grouped by workspace.</div>',
        unsafe_allow_html=True,
    )

    for workspace in workspaces:
        documents = document_service.get_documents_by_workspace(workspace.id)
        chunked_documents = [
            document
            for document in documents
            if document.status == "chunked"
        ]

        with st.expander(
            f"{workspace.name} • {len(documents)} document(s)",
            expanded=False,
        ):
            st.write(workspace.description or "No description provided.")

            action_col1, action_col2 = st.columns(2)

            with action_col1:
                index_disabled = len(chunked_documents) == 0

                if st.button(
                    "Index Workspace",
                    key=f"index_workspace_{workspace.id}",
                    disabled=index_disabled,
                ):
                    try:
                        indexed_count = indexing_service.index_workspace(workspace.id)
                        st.success(
                            f"Indexed {indexed_count} chunk(s) into ChromaDB and FAISS."
                        )
                    except Exception as error:
                        st.error(f"Could not index workspace: {error}")

            with action_col2:
                delete_workspace_checkbox = st.checkbox(
                    "Confirm delete workspace",
                    key=f"confirm_workspace_delete_{workspace.id}",
                )

                if st.button(
                    "Delete Workspace",
                    key=f"delete_workspace_{workspace.id}",
                    type="secondary",
                    disabled=not delete_workspace_checkbox,
                ):
                    try:
                        for document in documents:
                            document_service.delete_document(document.id)

                        workspace_service.delete_workspace(workspace.id)

                        st.success("Workspace and its documents deleted successfully.")
                        st.rerun()
                    except Exception as error:
                        st.error(f"Could not delete workspace: {error}")

            if not documents:
                st.info("No documents uploaded yet.")
            else:
                columns = st.columns(2)

                for index, document in enumerate(documents):
                    with columns[index % 2]:
                        render_document_card(
                            document=document,
                            document_service=document_service,
                            chunk_service=chunk_service,
                        )