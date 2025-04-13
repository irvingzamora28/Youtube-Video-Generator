import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ScriptGenerator from './pages/ScriptGenerator';
import ScriptGeneratorWithSegments from './pages/ScriptGeneratorWithSegments';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create" element={<ScriptGeneratorWithSegments />} />
      </Routes>
    </Router>
  );
}

export default App;
