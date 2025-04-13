import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ScriptGenerator from './pages/ScriptGenerator';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create" element={<ScriptGenerator />} />
      </Routes>
    </Router>
  );
}

export default App;
