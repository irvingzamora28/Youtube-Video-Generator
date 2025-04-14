"""
Segment model for the video generation project.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database.db import query, execute

class Segment:
    """Segment model class."""
    
    def __init__(self, id: Optional[int] = None, section_id: int = 0, narration_text: str = "", 
                 start_time: float = 0.0, duration: float = 0.0, position: int = 0,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize a Segment instance.
        
        Args:
            id: Segment ID (None for new segments)
            section_id: ID of the parent section
            narration_text: Narration text
            start_time: Start time in seconds
            duration: Duration in seconds
            position: Position in the section
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.section_id = section_id
        self.narration_text = narration_text
        self.start_time = start_time
        self.duration = duration
        self.position = position
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Segment':
        """
        Create a Segment instance from a dictionary.
        
        Args:
            data: Dictionary containing segment data
            
        Returns:
            A Segment instance
        """
        return cls(
            id=data.get('id'),
            section_id=data.get('section_id', 0),
            narration_text=data.get('narration_text', ""),
            start_time=data.get('start_time', 0.0),
            duration=data.get('duration', 0.0),
            position=data.get('position', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Segment instance to a dictionary.
        
        Returns:
            A dictionary representation of the segment
        """
        return {
            'id': self.id,
            'section_id': self.section_id,
            'narration_text': self.narration_text,
            'start_time': self.start_time,
            'duration': self.duration,
            'position': self.position,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self) -> bool:
        """
        Save the segment to the database.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            # Insert new segment
            sql = """
                INSERT INTO segments (section_id, narration_text, start_time, duration, position)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (self.section_id, self.narration_text, self.start_time, self.duration, self.position)
            self.id = execute(sql, params)
            return self.id is not None
        else:
            # Update existing segment
            self.updated_at = datetime.now()
            sql = """
                UPDATE segments
                SET section_id = ?, narration_text = ?, start_time = ?, duration = ?, 
                    position = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.section_id, self.narration_text, self.start_time, self.duration,
                     self.position, self.updated_at, self.id)
            return execute(sql, params) is not None
    
    @classmethod
    def get_by_id(cls, segment_id: int) -> Optional['Segment']:
        """
        Get a segment by ID.
        
        Args:
            segment_id: The ID of the segment
            
        Returns:
            A Segment instance or None if not found
        """
        sql = "SELECT * FROM segments WHERE id = ?"
        result = query(sql, (segment_id,), one=True)
        
        if result:
            return cls.from_dict(result)
        return None
    
    @classmethod
    def get_by_section_id(cls, section_id: int) -> List['Segment']:
        """
        Get all segments for a section.
        
        Args:
            section_id: The ID of the section
            
        Returns:
            A list of Segment instances
        """
        sql = "SELECT * FROM segments WHERE section_id = ? ORDER BY position"
        results = query(sql, (section_id,))
        
        return [cls.from_dict(result) for result in results] if results else []
    
    def delete(self) -> bool:
        """
        Delete the segment from the database.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            return False
        
        sql = "DELETE FROM segments WHERE id = ?"
        return execute(sql, (self.id,)) is not None
