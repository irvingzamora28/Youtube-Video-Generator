"""
Visual model for the video generation project.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database.db import query, execute
from backend.utils.file_storage import save_base64_image, load_image_as_base64, delete_file

class Visual:
    """Visual model class."""
    
    def __init__(self, id: Optional[int] = None, segment_id: int = 0, description: str = "", 
                 timestamp: float = 0.0, duration: float = 0.0, image_path: Optional[str] = None,
                 alt_text: str = "", visual_type: str = "image", visual_style: str = "",
                 position: int = 0, zoom_level: float = 1.0, transition: str = "",
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, remove_background: bool = False):
        """
        Initialize a Visual instance.
        
        Args:
            id: Visual ID (None for new visuals)
            segment_id: ID of the parent segment
            description: Visual description
            timestamp: Timestamp in seconds
            duration: Duration in seconds
            image_path: Path to the image file
            alt_text: Alternative text
            visual_type: Type of visual (image, video, etc.)
            visual_style: Style of the visual
            position: Position in the segment
            zoom_level: Zoom level
            transition: Transition effect
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.segment_id = segment_id
        self.description = description
        self.timestamp = timestamp
        self.duration = duration
        self.image_path = image_path
        self.alt_text = alt_text
        self.visual_type = visual_type
        self.visual_style = visual_style
        self.position = position
        self.zoom_level = zoom_level
        self.transition = transition
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
        # Temporary storage for base64 image data
        self._image_data = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Visual':
        """
        Create a Visual instance from a dictionary.
        
        Args:
            data: Dictionary containing visual data
            
        Returns:
            A Visual instance
        """
        return cls(
            id=data.get('id'),
            segment_id=data.get('segment_id', 0),
            description=data.get('description', ""),
            timestamp=data.get('timestamp', 0.0),
            duration=data.get('duration', 0.0),
            image_path=data.get('image_path'),
            alt_text=data.get('alt_text', ""),
            visual_type=data.get('visual_type', "image"),
            visual_style=data.get('visual_style', ""),
            position=data.get('position', 0),
            zoom_level=data.get('zoom_level', 1.0),
            transition=data.get('transition', ""),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            remove_background=data.get('remove_background', False)
        )
    
    def to_dict(self, include_image_data: bool = False) -> Dict[str, Any]:
        """
        Convert the Visual instance to a dictionary.
        
        Args:
            include_image_data: Whether to include base64 image data
            
        Returns:
            A dictionary representation of the visual
        """
        result = {
            'id': self.id,
            'segment_id': self.segment_id,
            'description': self.description,
            'timestamp': self.timestamp,
            'duration': self.duration,
            'image_path': self.image_path,
            'alt_text': self.alt_text,
            'visual_type': self.visual_type,
            'visual_style': self.visual_style,
            'position': self.position,
            'zoom_level': self.zoom_level,
            'transition': self.transition,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'remove_background': self.remove_background
        }
        
        # Include base64 image data if requested
        if include_image_data and self.image_path:
            success, base64_data = load_image_as_base64(self.image_path)
            if success:
                result['image_data'] = base64_data
        elif include_image_data and self._image_data:
            result['image_data'] = self._image_data
            
        return result
    
    def set_image_data(self, base64_data: str):
        """
        Set the base64 image data.
        
        Args:
            base64_data: Base64-encoded image data
        """
        self._image_data = base64_data
    
    def save(self, project_id: int = None) -> bool:
        """
        Save the visual to the database.
        
        Args:
            project_id: The ID of the project (required for new visuals with image data)
            
        Returns:
            True if successful, False otherwise
        """
        # Save the image if we have base64 data
        if self._image_data and project_id is not None:
            # For new visuals, we need to save with a temporary ID first
            temp_id = self.id or 0
            success, file_path = save_base64_image(self._image_data, project_id, temp_id)
            if success:
                self.image_path = file_path
                self._image_data = None
        
        if self.id is None:
            # Insert new visual
            sql = """
                INSERT INTO visuals (segment_id, description, timestamp, duration, image_path,
                                    alt_text, visual_type, visual_style, position, zoom_level, transition)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.segment_id, self.description, self.timestamp, self.duration, self.image_path,
                     self.alt_text, self.visual_type, self.visual_style, self.position, self.zoom_level, self.transition)
            self.id = execute(sql, params)
            
            # If we have a new ID and we saved a temporary image, rename it
            if self.id is not None and self.image_path and project_id is not None and "0.png" in self.image_path:
                success, new_path = save_base64_image(self._image_data, project_id, self.id)
                if success:
                    self.image_path = new_path
                    # Update the image path in the database
                    update_sql = "UPDATE visuals SET image_path = ? WHERE id = ?"
                    execute(update_sql, (self.image_path, self.id))
            
            return self.id is not None
        else:
            # Update existing visual
            self.updated_at = datetime.now()
            sql = """
                UPDATE visuals
                SET segment_id = ?, description = ?, timestamp = ?, duration = ?, image_path = ?,
                    alt_text = ?, visual_type = ?, visual_style = ?, position = ?, zoom_level = ?,
                    transition = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.segment_id, self.description, self.timestamp, self.duration, self.image_path,
                     self.alt_text, self.visual_type, self.visual_style, self.position, self.zoom_level,
                     self.transition, self.updated_at, self.id)
            return execute(sql, params) is not None
    
    @classmethod
    def get_by_id(cls, visual_id: int, include_image_data: bool = False) -> Optional['Visual']:
        """
        Get a visual by ID.
        
        Args:
            visual_id: The ID of the visual
            include_image_data: Whether to include base64 image data
            
        Returns:
            A Visual instance or None if not found
        """
        sql = "SELECT * FROM visuals WHERE id = ?"
        result = query(sql, (visual_id,), one=True)
        
        if result:
            visual = cls.from_dict(result)
            
            # Load image data if requested
            if include_image_data and visual.image_path:
                success, base64_data = load_image_as_base64(visual.image_path)
                if success:
                    visual._image_data = base64_data
            
            return visual
        return None
    
    @classmethod
    def get_by_segment_id(cls, segment_id: int, include_image_data: bool = False) -> List['Visual']:
        """
        Get all visuals for a segment.
        
        Args:
            segment_id: The ID of the segment
            include_image_data: Whether to include base64 image data
            
        Returns:
            A list of Visual instances
        """
        sql = "SELECT * FROM visuals WHERE segment_id = ? ORDER BY position"
        results = query(sql, (segment_id,))
        
        visuals = []
        if results:
            for result in results:
                visual = cls.from_dict(result)
                
                # Load image data if requested
                if include_image_data and visual.image_path:
                    success, base64_data = load_image_as_base64(visual.image_path)
                    if success:
                        visual._image_data = base64_data
                
                visuals.append(visual)
        
        return visuals
    
    def delete(self) -> bool:
        """
        Delete the visual from the database.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            return False
        
        # Delete the image file if it exists
        if self.image_path:
            delete_file(self.image_path)
        
        sql = "DELETE FROM visuals WHERE id = ?"
        return execute(sql, (self.id,)) is not None
