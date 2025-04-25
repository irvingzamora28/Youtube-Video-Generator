-- Migration: Add 'inspiration' column to projects table
ALTER TABLE projects ADD COLUMN inspiration TEXT;
