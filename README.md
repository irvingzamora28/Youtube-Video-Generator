# YT-Vidgen Video Generator

YT-Vidgen is a full-stack application for generating educational videos with AI. It uses a React+TypeScript frontend and a FastAPI backend to create engaging stickman-style educational videos.

## Features

- **AI Script Generation**: Generate complete video scripts from just a topic
- **Segment-Based Structure**: Scripts are organized into sections and segments with precise timing
- **Multiple Visuals Per Segment**: Each segment can have multiple visuals with specific timestamps
- **Visual-Text Synchronization**: Visuals are precisely timed to match specific parts of the narration
- **Interactive Timeline**: Visualize and edit the timing of segments and visuals
- **Script Editing**: Edit generated scripts and regenerate specific sections
- **Preview Mode**: Preview how the script will look as a video
- **Responsive UI**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- React with TypeScript
- Tailwind CSS v4 for styling
- React Router for navigation
- Custom components for script editing and visualization

### Backend
- FastAPI (Python)
- OpenAI/Gemini integration for content generation
- Pydantic for data validation
- Async processing for script generation

## Project Structure

```
.
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── App.tsx         # Main application component
│   └── ...
├── backend/                # FastAPI backend
│   ├── api/                # API endpoints
│   ├── llm/                # LLM integration
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── app/                # Application setup
└── ...
```

## Key Components

### Script Structure

- **Script**: The top-level container for the entire video
- **Section**: Major divisions of the script (e.g., Introduction, Key Concepts)
- **Segment**: Smaller chunks of content with specific narration text
- **Visual**: Individual visual elements (images, animations) with precise timing

### Frontend Components

- **ScriptGenerator**: Main interface for generating scripts
- **SegmentEditor**: Edit individual segments and their visuals
- **SegmentTimeline**: Visualize the timing of segments and visuals
- **ScriptVisualizer**: Preview the script as a video
- **SectionRegenerator**: Regenerate specific sections of the script

### Backend Services

- **ScriptGeneratorService**: Generate scripts using LLM
- **LLMProvider**: Abstract interface for different LLM providers

## Getting Started

### Prerequisites

- Node.js 16+ and npm/bun
- Python 3.9+
- OpenAI API key or Gemini API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sticked-video-generator.git
   cd sticked-video-generator
   ```

2. Install frontend dependencies:
   ```
   cd frontend
   npm install
   # or
   bun install
   ```

3. Install backend dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   # Backend .env file
   OPENAI_API_KEY=your_openai_api_key
   # or
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Running the Application

1. Start the backend:
   ```
   cd backend
   python run.py
   ```

2. Start the frontend:
   ```
   cd frontend
   npm run dev
   # or
   bun dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Usage

1. **Generate a Script**:
   - Enter a topic
   - Select target audience, duration, and style
   - Click "Generate Script"

2. **Edit the Script**:
   - Expand sections to view and edit segments
   - Use the segment editor to modify narration text and visuals
   - Select text to create visuals for specific parts of the narration

3. **Preview the Video**:
   - Click "Preview" to see how the script will look as a video
   - Navigate through sections, segments, and visuals
   - Use the timeline to visualize the timing

4. **Regenerate Content**:
   - Use "Regenerate Section" to improve specific parts
   - Provide additional instructions to guide the regeneration

## Current Status

The project is currently in active development. The following features are implemented:

- ✅ Frontend UI with script generation, editing, and preview
- ✅ Backend API for script generation
- ✅ Integration with LLM providers
- ✅ Segment-based script structure with multiple visuals
- ✅ Visual-text synchronization
- ⬜ Image generation using Gemini
- ⬜ Video rendering
- ⬜ Audio narration generation
- ⬜ User authentication and script saving

## License

[MIT License](LICENSE)

## Acknowledgements

- OpenAI for GPT models
- Google for Gemini models
- The React and FastAPI communities
