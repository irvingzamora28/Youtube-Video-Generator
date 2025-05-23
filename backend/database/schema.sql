-- SQLite schema for video generation project

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    target_audience TEXT,
    content JSON,  -- Stores the entire script structure (sections, segments, etc.)
    short_content JSONB,  -- New field to store short content
    style TEXT,
    visual_style TEXT,
    total_duration REAL,
    status TEXT,
    background_image TEXT, -- Optional local path to background image
    inspiration TEXT,
    infocard_highlights JSON, -- Stores infocard highlight objects
    youtube JSON, -- Stores YouTube-related properties (title, description, thumbnail_prompt, thumbnail_url, etc.)
    social_posts JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assets table for storing paths to generated media
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    asset_type TEXT NOT NULL,  -- 'image', 'audio', 'video', etc.
    path TEXT NOT NULL,        -- Relative path to the asset
    metadata JSON,             -- Additional metadata (e.g., visual_id, segment_id, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Settings table for application configuration
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_assets_project_id ON assets(project_id);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_settings_key ON settings(key);
