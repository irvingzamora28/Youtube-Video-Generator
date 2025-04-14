# Database

This directory contains the SQLite database for the video generation project.

## Database Files

The database files are not included in the repository. They will be created automatically when the application is run for the first time.

## Schema

The database schema is defined in `schema.sql`. It includes the following tables:

- `projects`: Stores project information and script content as JSON
- `assets`: Stores paths to generated media files (images, audio, video)
- `settings`: Stores application configuration

## Initialization

To initialize the database, run:

```bash
cd backend
python setup_db.py
```

Or the database will be initialized automatically when the API starts.

## Testing

For testing, a separate test database is used. This is created and destroyed during the test run, so it doesn't interfere with your development database.

To run the tests:

```bash
cd backend
pytest
```
