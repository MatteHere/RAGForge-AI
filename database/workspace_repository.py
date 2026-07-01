from typing import List, Optional

from database.db import get_db_connection
from models.workspace import Workspace


class WorkspaceRepository:
    """
    Repository responsible for all database operations
    related to workspaces.
    """

    def create_workspace(self, name: str, description: str = "") -> int:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO workspaces (name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )

        connection.commit()

        workspace_id = cursor.lastrowid

        connection.close()

        return workspace_id

    def get_all_workspaces(self) -> List[Workspace]:
        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM workspaces
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            Workspace(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_workspace_by_id(self, workspace_id: int) -> Optional[Workspace]:
        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM workspaces
            WHERE id = ?
            """,
            (workspace_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Workspace(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=row["created_at"],
        )

    def update_workspace(
        self,
        workspace_id: int,
        name: str,
        description: str,
    ) -> None:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE workspaces
            SET
                name = ?,
                description = ?
            WHERE id = ?
            """,
            (
                name,
                description,
                workspace_id,
            ),
        )

        connection.commit()

        connection.close()

    def delete_workspace(self, workspace_id: int) -> None:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM workspaces
            WHERE id = ?
            """,
            (workspace_id,),
        )

        connection.commit()

        connection.close()

    def count_workspaces(self) -> int:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM workspaces
            """
        )

        total = cursor.fetchone()["total"]

        connection.close()

        return total