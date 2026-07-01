from database.db import get_db_connection


class AnalyticsService:
    def get_search_logs(self) -> list[dict]:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                search_logs.id,
                search_logs.query,
                search_logs.retrieval_method,
                search_logs.result_count,
                search_logs.response_time_ms,
                search_logs.created_at,
                workspaces.name AS workspace_name
            FROM search_logs
            LEFT JOIN workspaces
                ON search_logs.workspace_id = workspaces.id
            ORDER BY search_logs.created_at DESC
            """
        )

        rows = cursor.fetchall()
        connection.close()

        return [dict(row) for row in rows]

    def get_summary_metrics(self) -> dict:
        logs = self.get_search_logs()

        total_searches = len(logs)

        if total_searches == 0:
            return {
                "total_searches": 0,
                "average_response_time_ms": 0,
                "total_results": 0,
            }

        total_response_time = sum(log["response_time_ms"] or 0 for log in logs)
        total_results = sum(log["result_count"] or 0 for log in logs)

        return {
            "total_searches": total_searches,
            "average_response_time_ms": round(total_response_time / total_searches, 2),
            "total_results": total_results,
        }