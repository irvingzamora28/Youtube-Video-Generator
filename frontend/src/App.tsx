import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ScriptGeneratorWithSegments from './pages/ScriptGeneratorWithSegments';
import ProjectsPage from './pages/ProjectsPage';
import NewProjectPage from './pages/NewProjectPage';
import ProjectDetail from './pages/ProjectDetail';
import VisualTimelineEditorPage from './pages/VisualTimelineEditorPage'; // Import the new page

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/new" element={<NewProjectPage />} />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/projects/:id/edit-script" element={<ScriptGeneratorWithSegments />} />
        <Route path="/projects/:id/generate-script" element={<ScriptGeneratorWithSegments />} />
        <Route path="/projects/:id/timeline" element={<VisualTimelineEditorPage />} /> {/* Add route for timeline editor */}
      </Routes>
    </Router>
  );
}

export default App;
