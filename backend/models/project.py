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
                 style: Optional[str] = None,
                 visual_style: Optional[str] = None,
                 background_image: Optional[str] = None,
                 inspiration: Optional[str] = None,
                 infocard_highlights: Optional[list] = None,
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
        self.style = style
        self.visual_style = visual_style
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.background_image = background_image
        self.inspiration = inspiration
        self.infocard_highlights = infocard_highlights or []

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

        # Parse infocard_highlights JSON if it's a string
        highlights = data.get('infocard_highlights')
        if isinstance(highlights, str):
            try:
                highlights = json.loads(highlights)
            except json.JSONDecodeError:
                highlights = []

        return cls(
            id=data.get('id'),
            title=data.get('title', ""),
            description=data.get('description', ""),
            target_audience=data.get('target_audience', ""),
            content=content,
            total_duration=data.get('total_duration', 0.0),
            status=data.get('status', "draft"),
            style=data.get('style'),
            visual_style=data.get('visual_style'),
            background_image=data.get('background_image'),
            inspiration=data.get('inspiration'),
            infocard_highlights=highlights,
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
            'style': self.style,
            'visual_style': self.visual_style,
            'background_image': self.background_image,
            'inspiration': self.inspiration,
            'infocard_highlights': self.infocard_highlights,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self) -> bool:
        """
        Save the project to the database.

        Returns:
            True if successful, False otherwise
        """
        print(f"Saving project {self.id}")
        # print(f"Content before JSON conversion: {self.content}")

        # Convert content and infocard_highlights to JSON string
        try:
            content_json = json.dumps(self.content)
            print(f"Content JSON: {content_json[:100]}..." if len(content_json) > 100 else content_json)
        except Exception as e:
            print(f"Error converting content to JSON: {str(e)}")
            return False
        try:
            highlights_json = json.dumps(self.infocard_highlights)
            print(f"Highlights JSON: {highlights_json[:100]}..." if len(highlights_json) > 100 else highlights_json)
        except Exception as e:
            print(f"Error converting highlights to JSON: {str(e)}")
            return False

        if self.id is None:
            # Insert new project
            sql = """
                INSERT INTO projects (title, description, target_audience, content, style, visual_style, total_duration, status, background_image, inspiration, infocard_highlights, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.title, self.description, self.target_audience, content_json,
                     self.style, self.visual_style, self.total_duration, self.status, self.background_image, self.inspiration, highlights_json, self.created_at, self.updated_at)
            self.id = execute(sql, params)
            return self.id is not None
        else:
            # Update existing project
            self.updated_at = datetime.now()
            sql = """
                UPDATE projects
                SET title = ?, description = ?, target_audience = ?, content = ?,
                    style = ?, visual_style = ?, total_duration = ?, status = ?, background_image = ?, inspiration = ?, infocard_highlights = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.title, self.description, self.target_audience, content_json,
                     self.style, self.visual_style, self.total_duration, self.status, self.background_image, self.inspiration, highlights_json, self.updated_at, self.id)
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
        print(f"Updating content for project {self.id}")
        self.content = content
        result = self.save()
        return result
    
    def get_full_script(self) -> str:
        """
        Returns the concatenated narrationText from all segments in all sections.
        """
        script_text = ""
        for section in self.content.get("sections", []):
            for seg in section.get("segments", []):
                narration = seg.get("narrationText", "")
                if narration:
                    script_text += narration + "\n"
        return script_text
