# AI-Powered Video Content Generator

A web application that generates and processes video content using AI. The system combines text generation, image creation, and animation processing to create engaging video content automatically.

## 🚀 Features

- **AI Content Generation**
  - Text generation using OpenAI GPT models
  - Image generation using DALL-E/Gemini
  - Smart content structuring and formatting

- **Media Processing**
  - Image animations
  - Text overlay animations
  - Video composition and editing
  - Custom transition effects

- **Modern Tech Stack**
  - React + TypeScript frontend
  - FastAPI Python backend
  - Real-time processing updates
  - Responsive design with Tailwind CSS

## 🏗️ Architecture

```plaintext
├── frontend/           # React + TypeScript + Vite application
│   ├── src/           # Frontend source code
│   └── ...            # Frontend configuration files
│
├── backend/           # FastAPI Python server
│   ├── app/          # Main application code
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   └── api/          # API endpoints
```

## 🛠️ Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- OpenAI API key
- Google Cloud (Gemini) API key

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-name>
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Add your API keys and configuration
   ```

## 🚀 Running the Application

1. **Start the Backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:5173`

## 🔧 Configuration

### Environment Variables

```plaintext
# Backend (.env)
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

## 📚 API Documentation

Once the backend is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

- **Frontend Tests**
  ```bash
  cd frontend
  npm test
  ```

- **Backend Tests**
  ```bash
  cd backend
  pytest
  ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT and DALL-E APIs
- Google for Gemini API
- The amazing open-source community
