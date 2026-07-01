from typing import List, Optional

from database.db import get_db_connection
from models.document import Document


class DocumentRepository:
    def create_document(
        self,
        workspace_id: int,
        file_name: str,
        file_type: str,
        file_path: str,
        file_size: int,
        status: str = "uploaded",
        extracted_text: str = "",
    ) -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO documents (
                workspace_id,
                file_name,
                file_type,
                file_path,
                file_size,
                status,
                extracted_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                workspace_id,
                file_name,
                file_type,
                file_path,
                file_size,
                status,
                extracted_text,
            ),
        )

        connection.commit()
        document_id = cursor.lastrowid
        connection.close()

        return document_id

    def _map_row_to_document(self, row) -> Document:
        return Document(
            id=row["id"],
            workspace_id=row["workspace_id"],
            file_name=row["file_name"],
            file_type=row["file_type"],
            file_path=row["file_path"],
            file_size=row["file_size"],
            status=row["status"],
            extracted_text=row["extracted_text"] or "",
            created_at=row["created_at"],
        )

    def get_all_documents(self) -> List[Document]:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()
        connection.close()

        return [self._map_row_to_document(row) for row in rows]

    def get_documents_by_workspace(self, workspace_id: int) -> List[Document]:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            WHERE workspace_id = ?
            ORDER BY created_at DESC
            """,
            (workspace_id,),
        )

        rows = cursor.fetchall()
        connection.close()

        return [self._map_row_to_document(row) for row in rows]

    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            WHERE id = ?
            """,
            (document_id,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return self._map_row_to_document(row)

    def update_document_status(self, document_id: int, status: str) -> None:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE documents
            SET status = ?
            WHERE id = ?
            """,
            (status, document_id),
        )

        connection.commit()
        connection.close()

    def update_extracted_text(
        self,
        document_id: int,
        extracted_text: str,
        status: str = "parsed",
    ) -> None:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE documents
            SET
                extracted_text = ?,
                status = ?
            WHERE id = ?
            """,
            (extracted_text, status, document_id),
        )

        connection.commit()
        connection.close()

    def delete_document(self, document_id: int) -> None:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM documents
            WHERE id = ?
            """,
            (document_id,),
        )

        connection.commit()
        connection.close()

    def count_documents(self) -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM documents
            """
        )

        total = cursor.fetchone()["total"]
        connection.close()

        return total