from typing import List

from database.db import get_db_connection


class ChunkRepository:
    def create_chunk(
        self,
        document_id: int,
        workspace_id: int,
        chunk_index: int,
        chunk_text: str,
        token_count: int,
    ) -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO document_chunks (
                document_id,
                workspace_id,
                chunk_index,
                chunk_text,
                token_count
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document_id,
                workspace_id,
                chunk_index,
                chunk_text,
                token_count,
            ),
        )

        connection.commit()
        chunk_id = cursor.lastrowid
        connection.close()

        return chunk_id

    def delete_chunks_by_document(self, document_id: int) -> None:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM document_chunks
            WHERE document_id = ?
            """,
            (document_id,),
        )

        connection.commit()
        connection.close()

    def get_chunks_by_workspace(self, workspace_id: int) -> List[dict]:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                document_chunks.id,
                document_chunks.document_id,
                document_chunks.workspace_id,
                document_chunks.chunk_index,
                document_chunks.chunk_text,
                document_chunks.token_count,
                document_chunks.created_at,
                documents.file_name,
                documents.file_type,
                documents.status AS document_status
            FROM document_chunks
            INNER JOIN documents
                ON document_chunks.document_id = documents.id
            WHERE document_chunks.workspace_id = ?
            ORDER BY document_chunks.document_id, document_chunks.chunk_index
            """,
            (workspace_id,),
        )

        rows = cursor.fetchall()
        connection.close()

        return [dict(row) for row in rows]

    def count_chunks(self) -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM document_chunks
            """
        )

        total = cursor.fetchone()["total"]
        connection.close()

        return total