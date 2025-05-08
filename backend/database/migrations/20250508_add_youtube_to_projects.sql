-- Migration: Add 'youtube' JSON column to projects table
ALTER TABLE projects ADD COLUMN youtube JSON;
