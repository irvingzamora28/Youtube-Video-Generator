"""
Section model for the video generation project.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database.db import query, execute

class Section:
    """Section model class."""
    
    def __init__(self, id: Optional[int] = None, project_id: int = 0, title: str = "", 
                 content: str = "", total_duration: float = 0.0, position: int = 0,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize a Section instance.
        
        Args:
            id: Section ID (None for new sections)
            project_id: ID of the parent project
            title: Section title
            content: Section content
            total_duration: Total duration in seconds
            position: Position in the project
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.project_id = project_id
        self.title = title
        self.content = content
        self.total_duration = total_duration
        self.position = position
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Section':
        """
        Create a Section instance from a dictionary.
        
        Args:
            data: Dictionary containing section data
            
        Returns:
            A Section instance
        """
        return cls(
            id=data.get('id'),
            project_id=data.get('project_id', 0),
            title=data.get('title', ""),
            content=data.get('content', ""),
            total_duration=data.get('total_duration', 0.0),
            position=data.get('position', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Section instance to a dictionary.
        
        Returns:
            A dictionary representation of the section
        """
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'content': self.content,
            'total_duration': self.total_duration,
            'position': self.position,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self) -> bool:
        """
        Save the section to the database.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            # Insert new section
            sql = """
                INSERT INTO sections (project_id, title, content, total_duration, position)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (self.project_id, self.title, self.content, self.total_duration, self.position)
            self.id = execute(sql, params)
            return self.id is not None
        else:
            # Update existing section
            self.updated_at = datetime.now()
            sql = """
                UPDATE sections
                SET project_id = ?, title = ?, content = ?, total_duration = ?, 
                    position = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.project_id, self.title, self.content, self.total_duration,
                     self.position, self.updated_at, self.id)
            return execute(sql, params) is not None
    
    @classmethod
    def get_by_id(cls, section_id: int) -> Optional['Section']:
        """
        Get a section by ID.
        
        Args:
            section_id: The ID of the section
            
        Returns:
            A Section instance or None if not found
        """
        sql = "SELECT * FROM sections WHERE id = ?"
        result = query(sql, (section_id,), one=True)
        
        if result:
            return cls.from_dict(result)
        return None
    
    @classmethod
    def get_by_project_id(cls, project_id: int) -> List['Section']:
        """
        Get all sections for a project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            A list of Section instances
        """
        sql = "SELECT * FROM sections WHERE project_id = ? ORDER BY position"
        results = query(sql, (project_id,))
        
        return [cls.from_dict(result) for result in results] if results else []
    
    def delete(self) -> bool:
        """
        Delete the section from the database.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            return False
        
        sql = "DELETE FROM sections WHERE id = ?"
        return execute(sql, (self.id,)) is not None
