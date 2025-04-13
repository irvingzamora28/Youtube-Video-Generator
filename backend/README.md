# Backend for AI Video Content Generator

This is the FastAPI backend for the AI Video Content Generator application.

## Features

- FastAPI server with automatic API documentation
- LLM integration with OpenAI and Google Gemini
- Streaming API responses
- Environment-based configuration

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp ../.env.example .env
   # Edit .env with your API keys and configuration
   ```

## Running the Server

```bash
# From the backend directory
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/                # Main application code
│   ├── __init__.py
│   └── main.py         # FastAPI application
├── api/                # API endpoints
│   ├── __init__.py
│   └── llm.py          # LLM API endpoints
├── config/             # Configuration
│   ├── __init__.py
│   └── settings.py     # Application settings
├── llm/                # LLM providers
│   ├── __init__.py
│   ├── base.py         # Base LLM provider
│   ├── factory.py      # LLM provider factory
│   ├── google_provider.py  # Google Gemini provider
│   └── openai_provider.py  # OpenAI provider
├── models/             # Data models
│   ├── __init__.py
│   └── llm.py          # LLM data models
├── utils/              # Utilities
│   ├── __init__.py
│   └── text_formatter.py  # Text formatting utilities
├── requirements.txt    # Dependencies
└── run.py              # Script to run the server
```
