-- Migration: Add short_content field to projects table
ALTER TABLE projects ADD COLUMN short_content JSON;
