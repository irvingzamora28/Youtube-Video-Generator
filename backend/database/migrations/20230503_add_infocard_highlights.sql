-- Migration: Add infocard_highlights JSON column to projects table
ALTER TABLE projects ADD COLUMN infocard_highlights JSON;
