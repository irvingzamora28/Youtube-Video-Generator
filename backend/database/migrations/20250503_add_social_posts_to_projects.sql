-- Migration: Add 'social_posts' column to projects table
ALTER TABLE projects ADD COLUMN social_posts JSON;
