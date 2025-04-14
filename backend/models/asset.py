"""
Asset model for the video generation project.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from backend.database.db import query, execute
from backend.utils.file_storage import delete_file

class Asset:
    """Asset model class."""
    
    def __init__(self, id: Optional[int] = None, project_id: int = 0, asset_type: str = "", 
                 path: str = "", metadata: Dict[str, Any] = None,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        """
        Initialize an Asset instance.
        
        Args:
            id: Asset ID (None for new assets)
            project_id: ID of the parent project
            asset_type: Type of asset (image, audio, video)
            path: Path to the asset file
            metadata: Additional metadata
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.project_id = project_id
        self.asset_type = asset_type
        self.path = path
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Asset':
        """
        Create an Asset instance from a dictionary.
        
        Args:
            data: Dictionary containing asset data
            
        Returns:
            An Asset instance
        """
        # Parse metadata JSON if it's a string
        metadata = data.get('metadata')
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except json.JSONDecodeError:
                metadata = {}
        
        return cls(
            id=data.get('id'),
            project_id=data.get('project_id', 0),
            asset_type=data.get('asset_type', ""),
            path=data.get('path', ""),
            metadata=metadata,
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Asset instance to a dictionary.
        
        Returns:
            A dictionary representation of the asset
        """
        return {
            'id': self.id,
            'project_id': self.project_id,
            'asset_type': self.asset_type,
            'path': self.path,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self) -> bool:
        """
        Save the asset to the database.
        
        Returns:
            True if successful, False otherwise
        """
        # Convert metadata to JSON string
        metadata_json = json.dumps(self.metadata)
        
        if self.id is None:
            # Insert new asset
            sql = """
                INSERT INTO assets (project_id, asset_type, path, metadata)
                VALUES (?, ?, ?, ?)
            """
            params = (self.project_id, self.asset_type, self.path, metadata_json)
            self.id = execute(sql, params)
            return self.id is not None
        else:
            # Update existing asset
            self.updated_at = datetime.now()
            sql = """
                UPDATE assets
                SET project_id = ?, asset_type = ?, path = ?, metadata = ?, updated_at = ?
                WHERE id = ?
            """
            params = (self.project_id, self.asset_type, self.path, metadata_json,
                     self.updated_at, self.id)
            return execute(sql, params) is not None
    
    @classmethod
    def get_by_id(cls, asset_id: int) -> Optional['Asset']:
        """
        Get an asset by ID.
        
        Args:
            asset_id: The ID of the asset
            
        Returns:
            An Asset instance or None if not found
        """
        sql = "SELECT * FROM assets WHERE id = ?"
        result = query(sql, (asset_id,), one=True)
        
        if result:
            return cls.from_dict(result)
        return None
    
    @classmethod
    def get_by_project_id(cls, project_id: int, asset_type: Optional[str] = None) -> List['Asset']:
        """
        Get all assets for a project.
        
        Args:
            project_id: The ID of the project
            asset_type: Optional filter by asset type
            
        Returns:
            A list of Asset instances
        """
        if asset_type:
            sql = "SELECT * FROM assets WHERE project_id = ? AND asset_type = ? ORDER BY created_at"
            results = query(sql, (project_id, asset_type))
        else:
            sql = "SELECT * FROM assets WHERE project_id = ? ORDER BY created_at"
            results = query(sql, (project_id,))
        
        return [cls.from_dict(result) for result in results] if results else []
    
    @classmethod
    def get_by_metadata(cls, project_id: int, key: str, value: Any) -> List['Asset']:
        """
        Get assets by metadata key-value pair.
        
        Args:
            project_id: The ID of the project
            key: Metadata key
            value: Metadata value
            
        Returns:
            A list of Asset instances
        """
        # This is a bit tricky with SQLite JSON support, so we'll get all assets and filter in Python
        assets = cls.get_by_project_id(project_id)
        return [asset for asset in assets if asset.metadata.get(key) == value]
    
    def delete(self) -> bool:
        """
        Delete the asset from the database and file system.
        
        Returns:
            True if successful, False otherwise
        """
        if self.id is None:
            return False
        
        # Delete the file if it exists
        if self.path:
            delete_file(self.path)
        
        sql = "DELETE FROM assets WHERE id = ?"
        return execute(sql, (self.id,)) is not None
