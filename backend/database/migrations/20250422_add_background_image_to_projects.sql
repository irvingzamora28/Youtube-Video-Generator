-- Migration: Add background_image column to projects table
ALTER TABLE projects ADD COLUMN background_image TEXT;
