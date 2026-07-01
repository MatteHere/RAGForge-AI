import os
from pathlib import Path
from typing import List

from database.document_repository import DocumentRepository
from document_processing.document_parser import DocumentParser
from models.document import Document


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"

ALLOWED_FILE_TYPES = {".pdf", ".docx", ".pptx", ".txt", ".md"}


class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()
        self.document_parser = DocumentParser()

    def save_uploaded_file(self, uploaded_file, workspace_id: int) -> int:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        original_file_name = uploaded_file.name
        file_extension = Path(original_file_name).suffix.lower()

        if file_extension not in ALLOWED_FILE_TYPES:
            raise ValueError("Unsupported file type.")

        file_path = UPLOAD_DIR / original_file_name

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        file_size = file_path.stat().st_size

        document_id = self.document_repository.create_document(
            workspace_id=workspace_id,
            file_name=original_file_name,
            file_type=file_extension,
            file_path=str(file_path),
            file_size=file_size,
            status="uploaded",
        )

        try:
            extracted_text = self.document_parser.parse_document(str(file_path))

            self.document_repository.update_extracted_text(
                document_id=document_id,
                extracted_text=extracted_text,
                status="parsed",
            )

        except Exception:
            self.document_repository.update_document_status(
                document_id=document_id,
                status="failed",
            )

        return document_id

    def get_all_documents(self) -> List[Document]:
        return self.document_repository.get_all_documents()

    def get_documents_by_workspace(self, workspace_id: int) -> List[Document]:
        return self.document_repository.get_documents_by_workspace(workspace_id)

    def count_documents(self) -> int:
        return self.document_repository.count_documents()

    def delete_document(self, document_id: int) -> None:
        document = self.document_repository.get_document_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        self.document_repository.delete_document(document_id)