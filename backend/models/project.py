"""
Project model for the video generation project.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from backend.database.db import query, execute

class Project:
    """Project model class."""

    def __init__(self, id: Optional[int] = None, title: str = "", description: str = "",
                 target_audience: str = "", content: Dict[str, Any] = None,
                 total_duration: float = 0.0, status: str = "draft",
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize a Project instance.

        Args:
            id: Project ID (None for new projects)
            title: Project title
            description: Project description
            target_audience: Target audience
            content: Project content (script structure)
            total_duration: Total duration in seconds
            status: Project status (draft, in_progress, completed)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.title = title
        self.description = description
        self.target_audience = target_audience
        self.content = content or {}
        self.total_duration = total_duration
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """
        Create a Project instance from a dictionary.

        Args:
            data: Dictionary containing project data

        Returns:
            A Project instance
        """
        # Parse content JSON if it's a string
        content = data.get('content')
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                content = {}

        return cls(
            id=data.get('id'),
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_audience=data.get('target_audience', ""),
            content=content,
            total_duration=data.get('total_duration', 0.0),
            status=data.get('status', "draft"),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Project instance to a dictionary.

        Returns:
            A dictionary representation of the project
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_audience': self.target_audience,
            'content': self.content,
            'total_duration': self.total_duration,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self) -> bool:
        """
        Save the project to the database.

        Returns:
            True if successful, False otherwise
        """
        # Convert content to JSON string
        content_json = json.dumps(self.content)

        if self.id is None:
            # Insert new project
            sql = """
                INSERT INTO projects (title, description, target_audience, content, total_duration, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.title, self.description, self.target_audience, content_json,
                     self.total_duration, self.status)
            self.id = execute(sql, params)
            return self.id is not None
        else:
            # Update existing project
            self.updated_at = datetime.now()
            sql = """
                UPDATE projects
                SET title = ?, description = ?, target_audience = ?, content = ?,
                    total_duration = ?, status = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.title, self.description, self.target_audience, content_json,
                     self.total_duration, self.status, self.updated_at, self.id)
            return execute(sql, params) is not None

    @classmethod
    def get_by_id(cls, project_id: int) -> Optional['Project']:
        """
        Get a project by ID.

        Args:
            project_id: The ID of the project

        Returns:
            A Project instance or None if not found
        """
        sql = "SELECT * FROM projects WHERE id = ?"
        result = query(sql, (project_id,), one=True)

        if result:
            return cls.from_dict(result)
        return None

    @classmethod
    def get_all(cls) -> List['Project']:
        """
        Get all projects.

        Returns:
            A list of Project instances
        """
        sql = "SELECT * FROM projects ORDER BY updated_at DESC"
        results = query(sql)

        return [cls.from_dict(result) for result in results] if results else []

    def delete(self) -> bool:
        """
        Delete the project from the database.

        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            return False

        sql = "DELETE FROM projects WHERE id = ?"
        return execute(sql, (self.id,)) is not None

    def update_content(self, content: Dict[str, Any]) -> bool:
        """
        Update the project content.

        Args:
            content: New content dictionary

        Returns:
            True if successful, False otherwise
        """
        self.content = content
        return self.save()
