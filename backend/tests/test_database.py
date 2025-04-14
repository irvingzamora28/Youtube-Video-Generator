"""
Tests for the database implementation using pytest.
"""
import os
import json
import sqlite3
import pytest
import shutil
import base64
from pathlib import Path
from io import BytesIO
from PIL import Image

# Paths
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = SCRIPT_DIR.parent
DB_DIR = ROOT_DIR / "database"
SCHEMA_FILE = DB_DIR / "schema.sql"

# Test paths
TEST_DB_FILE = ROOT_DIR / "test_database.db"
TEST_STORAGE_DIR = ROOT_DIR / "test_storage"

@pytest.fixture(scope="session")
def test_db():
    """Create a test database."""
    # Create database directory
    os.makedirs(DB_DIR, exist_ok=True)

    # Read schema file
    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()

    # Create and initialize database
    conn = sqlite3.connect(TEST_DB_FILE)
    conn.executescript(schema)
    conn.commit()

    # Return the connection
    yield conn

    # Clean up
    conn.close()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

@pytest.fixture(scope="session")
def test_storage():
    """Create test storage directories."""
    # Create storage directories
    os.makedirs(TEST_STORAGE_DIR, exist_ok=True)
    os.makedirs(TEST_STORAGE_DIR / "projects", exist_ok=True)

    # Return the storage directory
    yield TEST_STORAGE_DIR

    # Clean up
    if os.path.exists(TEST_STORAGE_DIR):
        shutil.rmtree(TEST_STORAGE_DIR)

def get_project_dir(storage_dir, project_id):
    """Get a project directory."""
    project_dir = storage_dir / "projects" / str(project_id)
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories
    images_dir = project_dir / "images"
    audio_dir = project_dir / "audio"
    video_dir = project_dir / "video"
    video_segments_dir = video_dir / "segments"

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(video_segments_dir, exist_ok=True)

    return project_dir

def save_asset(storage_dir, data, project_id, asset_type, asset_id=None, extension=None):
    """Save an asset to the file system."""
    # Get the project directory
    project_dir = get_project_dir(storage_dir, project_id)

    # Determine the subdirectory based on asset type
    if asset_type == 'image':
        subdir = project_dir / "images"
        default_ext = ".png"
    elif asset_type == 'audio':
        subdir = project_dir / "audio"
        default_ext = ".mp3"
    elif asset_type == 'video':
        if asset_id and asset_id.startswith('segment_'):
            subdir = project_dir / "video" / "segments"
        else:
            subdir = project_dir / "video"
        default_ext = ".mp4"
    else:
        subdir = project_dir / asset_type
        default_ext = ".bin"
        os.makedirs(subdir, exist_ok=True)

    # Use provided extension or default
    ext = extension or default_ext

    # Generate a unique filename if asset_id is not provided
    if asset_id is None:
        import uuid
        filename = f"{uuid.uuid4()}{ext}"
    else:
        filename = f"{asset_id}{ext}"

    # Save the asset
    file_path = subdir / filename

    with open(file_path, 'wb') as f:
        f.write(data)

    # Return the relative path from the storage directory
    relative_path = os.path.relpath(file_path, storage_dir)

    return relative_path

def save_base64_image(storage_dir, base64_data, project_id, visual_id=None):
    """Save a base64-encoded image to the file system."""
    # Remove data URL prefix if present
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]

    # Decode the base64 data
    image_data = base64.b64decode(base64_data)

    # Validate the image using PIL
    img = Image.open(BytesIO(image_data))

    # Convert to PNG format
    output = BytesIO()
    img.save(output, format='PNG')
    png_data = output.getvalue()

    # Save the image as an asset
    return save_asset(storage_dir, png_data, project_id, 'image', visual_id)

def load_image_as_base64(storage_dir, file_path):
    """Load an image from the file system and convert it to base64."""
    # Get the absolute path
    abs_path = storage_dir / file_path

    # Read the image file
    with open(abs_path, "rb") as f:
        image_data = f.read()

    # Convert to base64
    base64_data = base64.b64encode(image_data).decode('utf-8')

    return base64_data

def delete_file(storage_dir, file_path):
    """Delete a file from the file system."""
    # Get the absolute path
    abs_path = storage_dir / file_path

    # Delete the file
    os.remove(abs_path)

    return not os.path.exists(abs_path)

# Project Tests
def test_project_create(test_db):
    """Test creating a project."""
    # Create a project
    content = json.dumps({
        "sections": [
            {
                "title": "Introduction",
                "segments": [
                    {
                        "narration_text": "Welcome to the video",
                        "visuals": [
                            {
                                "description": "Opening title",
                                "visual_type": "image"
                            }
                        ]
                    }
                ]
            }
        ]
    })

    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, target_audience, content, status) VALUES (?, ?, ?, ?, ?)",
        ("Test Project", "Test Description", "Test Audience", content, "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Verify the project was created
    assert project_id is not None
    assert project_id > 0

def test_project_read(test_db):
    """Test reading a project."""
    # Create a project
    content = json.dumps({
        "sections": [
            {
                "title": "Introduction",
                "segments": [
                    {
                        "narration_text": "Welcome to the video",
                        "visuals": [
                            {
                                "description": "Opening title",
                                "visual_type": "image"
                            }
                        ]
                    }
                ]
            }
        ]
    })

    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, target_audience, content, status) VALUES (?, ?, ?, ?, ?)",
        ("Test Project", "Test Description", "Test Audience", content, "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Read the project
    cursor.execute("SELECT id, title, description, target_audience, content FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()

    # Verify the project was read correctly
    assert project is not None
    assert project[1] == "Test Project"  # title
    assert project[2] == "Test Description"  # description
    assert project[3] == "Test Audience"  # target_audience

    # Parse the content
    project_content = json.loads(project[4])  # content
    assert len(project_content["sections"]) == 1
    assert project_content["sections"][0]["title"] == "Introduction"
    assert project_content["sections"][0]["segments"][0]["narration_text"] == "Welcome to the video"
    assert project_content["sections"][0]["segments"][0]["visuals"][0]["description"] == "Opening title"

def test_project_update(test_db):
    """Test updating a project."""
    # Create a project
    content = json.dumps({
        "sections": [
            {
                "title": "Introduction",
                "segments": [
                    {
                        "narration_text": "Welcome to the video",
                        "visuals": [
                            {
                                "description": "Opening title",
                                "visual_type": "image"
                            }
                        ]
                    }
                ]
            }
        ]
    })

    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, target_audience, content, status) VALUES (?, ?, ?, ?, ?)",
        ("Test Project", "Test Description", "Test Audience", content, "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Update the project
    updated_content = json.dumps({
        "sections": [
            {
                "title": "Updated Introduction",
                "segments": [
                    {
                        "narration_text": "Welcome to the updated video",
                        "visuals": [
                            {
                                "description": "Updated opening title",
                                "visual_type": "image"
                            }
                        ]
                    }
                ]
            }
        ]
    })

    cursor.execute(
        "UPDATE projects SET title = ?, description = ?, content = ?, status = ? WHERE id = ?",
        ("Updated Project", "Updated Description", updated_content, "in_progress", project_id)
    )
    test_db.commit()

    # Read the updated project
    cursor.execute("SELECT id, title, description, target_audience, content, status FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()

    # Verify the project was updated correctly
    assert project is not None
    assert project[1] == "Updated Project"  # title
    assert project[2] == "Updated Description"  # description

    # Parse the updated content
    project_content = json.loads(project[4])  # content
    assert project_content["sections"][0]["title"] == "Updated Introduction"
    assert project_content["sections"][0]["segments"][0]["narration_text"] == "Welcome to the updated video"
    assert project_content["sections"][0]["segments"][0]["visuals"][0]["description"] == "Updated opening title"
    assert project[5] == "in_progress"  # status

def test_project_delete(test_db):
    """Test deleting a project."""
    # Create a project
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, status) VALUES (?, ?, ?)",
        ("Test Project", "Test Description", "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Delete the project
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    test_db.commit()

    # Verify the project was deleted
    cursor.execute("SELECT COUNT(*) FROM projects WHERE id = ?", (project_id,))
    count = cursor.fetchone()[0]
    assert count == 0

# Asset Tests
def test_asset_create(test_db):
    """Test creating an asset."""
    # Create a project first
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, status) VALUES (?, ?, ?)",
        ("Asset Test Project", "For testing assets", "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Create an asset
    metadata = json.dumps({
        "visual_id": "123",
        "description": "Test Image",
        "timestamp": 10.5
    })

    cursor.execute(
        "INSERT INTO assets (project_id, asset_type, path, metadata) VALUES (?, ?, ?, ?)",
        (project_id, "image", "test/path.png", metadata)
    )
    asset_id = cursor.lastrowid
    test_db.commit()

    # Verify the asset was created
    assert asset_id is not None
    assert asset_id > 0

def test_asset_read(test_db):
    """Test reading an asset."""
    # Create a project first
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, status) VALUES (?, ?, ?)",
        ("Asset Test Project", "For testing assets", "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Create an asset
    metadata = json.dumps({
        "visual_id": "123",
        "description": "Test Image",
        "timestamp": 10.5
    })

    cursor.execute(
        "INSERT INTO assets (project_id, asset_type, path, metadata) VALUES (?, ?, ?, ?)",
        (project_id, "image", "test/path.png", metadata)
    )
    asset_id = cursor.lastrowid
    test_db.commit()

    # Read the asset
    cursor.execute("SELECT id, project_id, asset_type, path, metadata FROM assets WHERE id = ?", (asset_id,))
    asset = cursor.fetchone()

    # Verify the asset was read correctly
    assert asset is not None
    assert asset[1] == project_id  # project_id
    assert asset[2] == "image"  # asset_type
    assert asset[3] == "test/path.png"  # path

    # Parse the metadata
    asset_metadata = json.loads(asset[4])  # metadata
    assert asset_metadata["visual_id"] == "123"
    assert asset_metadata["description"] == "Test Image"
    assert asset_metadata["timestamp"] == 10.5

def test_asset_update(test_db):
    """Test updating an asset."""
    # Create a project first
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, status) VALUES (?, ?, ?)",
        ("Asset Test Project", "For testing assets", "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Create an asset
    metadata = json.dumps({
        "visual_id": "123",
        "description": "Test Image",
        "timestamp": 10.5
    })

    cursor.execute(
        "INSERT INTO assets (project_id, asset_type, path, metadata) VALUES (?, ?, ?, ?)",
        (project_id, "image", "test/path.png", metadata)
    )
    asset_id = cursor.lastrowid
    test_db.commit()

    # Update the asset
    updated_metadata = json.dumps({
        "visual_id": "123",
        "description": "Updated Test Image",
        "timestamp": 15.0,
        "additional_field": "New field"
    })

    cursor.execute(
        "UPDATE assets SET path = ?, metadata = ? WHERE id = ?",
        ("updated/path.png", updated_metadata, asset_id)
    )
    test_db.commit()

    # Read the updated asset
    cursor.execute("SELECT id, project_id, asset_type, path, metadata FROM assets WHERE id = ?", (asset_id,))
    asset = cursor.fetchone()

    # Verify the asset was updated correctly
    assert asset is not None
    assert asset[3] == "updated/path.png"  # path

    # Parse the updated metadata
    asset_metadata = json.loads(asset[4])  # metadata
    assert asset_metadata["description"] == "Updated Test Image"
    assert asset_metadata["timestamp"] == 15.0
    assert asset_metadata["additional_field"] == "New field"

def test_asset_delete(test_db):
    """Test deleting an asset."""
    # Create a project first
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO projects (title, description, status) VALUES (?, ?, ?)",
        ("Asset Test Project", "For testing assets", "draft")
    )
    project_id = cursor.lastrowid
    test_db.commit()

    # Create an asset
    cursor.execute(
        "INSERT INTO assets (project_id, asset_type, path, metadata) VALUES (?, ?, ?, ?)",
        (project_id, "image", "test/path.png", "{}")
    )
    asset_id = cursor.lastrowid
    test_db.commit()

    # Delete the asset
    cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    test_db.commit()

    # Verify the asset was deleted
    cursor.execute("SELECT COUNT(*) FROM assets WHERE id = ?", (asset_id,))
    count = cursor.fetchone()[0]
    assert count == 0

# File Storage Tests
def test_get_project_dir(test_storage):
    """Test getting a project directory."""
    # Get a project directory
    project_dir = get_project_dir(test_storage, 123)

    # Verify the directory structure
    assert os.path.exists(project_dir)
    assert os.path.exists(project_dir / "images")
    assert os.path.exists(project_dir / "audio")
    assert os.path.exists(project_dir / "video")
    assert os.path.exists(project_dir / "video" / "segments")

def test_save_asset(test_storage):
    """Test saving an asset."""
    # Create test data
    test_data = b"Test binary data"

    # Save the asset
    file_path = save_asset(test_storage, test_data, 123, "image", "test_asset")

    # Verify the file exists
    full_path = test_storage / file_path
    assert os.path.exists(full_path)

    # Verify the file content
    with open(full_path, "rb") as f:
        content = f.read()
        assert content == test_data

def test_save_base64_image(test_storage):
    """Test saving a base64-encoded image."""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    base64_data = base64.b64encode(img_data).decode('utf-8')

    # Save the image
    image_path = save_base64_image(test_storage, base64_data, 123, "test_image")

    # Verify the file exists
    full_path = test_storage / image_path
    assert os.path.exists(full_path)

    # Verify it's a valid image
    img = Image.open(full_path)
    assert img.format == 'PNG'
    assert img.size == (100, 100)

def test_load_image_as_base64(test_storage):
    """Test loading an image as base64."""
    # Create and save a test image
    img = Image.new('RGB', (100, 100), color='blue')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()

    # Save the image directly
    # Make sure the directory exists
    get_project_dir(test_storage, 123)
    file_path = "projects/123/images/test_load.png"
    full_path = test_storage / file_path

    with open(full_path, 'wb') as f:
        f.write(img_data)

    # Load the image as base64
    base64_data = load_image_as_base64(test_storage, file_path)

    # Verify the base64 data
    decoded_data = base64.b64decode(base64_data)
    img = Image.open(BytesIO(decoded_data))
    assert img.format == 'PNG'
    assert img.size == (100, 100)

def test_delete_file(test_storage):
    """Test deleting a file."""
    # Create and save a test file
    project_dir = get_project_dir(test_storage, 123)
    test_dir = project_dir / "test"
    os.makedirs(test_dir, exist_ok=True)
    file_path = "projects/123/test/test_delete.txt"
    full_path = test_storage / file_path

    with open(full_path, 'w') as f:
        f.write('Test content')

    # Verify the file exists
    assert os.path.exists(full_path)

    # Delete the file
    result = delete_file(test_storage, file_path)

    # Verify the file was deleted
    assert result
    assert not os.path.exists(full_path)
