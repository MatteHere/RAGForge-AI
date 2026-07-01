from typing import List

from database.workspace_repository import WorkspaceRepository
from models.workspace import Workspace


class WorkspaceService:
    def __init__(self):
        self.workspace_repository = WorkspaceRepository()

    def create_workspace(self, name: str, description: str = "") -> int:
        clean_name = name.strip()
        clean_description = description.strip()

        if not clean_name:
            raise ValueError("Workspace name cannot be empty.")

        return self.workspace_repository.create_workspace(
            name=clean_name,
            description=clean_description,
        )

    def get_all_workspaces(self) -> List[Workspace]:
        return self.workspace_repository.get_all_workspaces()

    def count_workspaces(self) -> int:
        return self.workspace_repository.count_workspaces()

    def delete_workspace(self, workspace_id: int) -> None:
        self.workspace_repository.delete_workspace(workspace_id)