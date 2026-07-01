from database.db import get_db_connection


class SearchLogRepository:
    def create_search_log(
        self,
        workspace_id: int,
        query: str,
        retrieval_method: str,
        result_count: int,
        response_time_ms: float,
    ) -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO search_logs (
                workspace_id,
                query,
                retrieval_method,
                result_count,
                response_time_ms
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                workspace_id,
                query,
                retrieval_method,
                result_count,
                response_time_ms,
            ),
        )

        connection.commit()
        search_log_id = cursor.lastrowid
        connection.close()

        return search_log_id