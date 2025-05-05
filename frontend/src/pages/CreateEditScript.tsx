import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import { ArrowLeft } from 'lucide-react';
import { generateScript, parseScriptJson } from '../services/api';
import { getProject, getProjectContent, updateProjectScript } from '../services/projectApi';
import { Script } from '../types/script';

export default function CreateEditScript() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();

  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [duration, setDuration] = useState('5');
  const [style] = useState('educational');
  const [visualStyle, setVisualStyle] = useState('stick-man');
  const [inspiration, setInspiration] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // For pasted JSON
  const [pastedJson, setPastedJson] = useState('');
  const [isParsingJson, setIsParsingJson] = useState(false);

  // Load project data if projectId is provided
    useEffect(() => {
      if (projectId) {
        loadProjectData(parseInt(projectId));
      }
    }, [projectId]);

    const loadProjectData = async (id: number) => {
        try {
          // setIsLoading(true);
          setError(null);
          const project = await getProject(id);
          const projectContent = await getProjectContent(id);
    
          // If the project has content, use it
          if (project) {
            console.log('Project loaded for editing:', project);
            console.log('Project sections:', project.sections);
            if (project.sections && project.sections.length > 0) {
              console.log('First section segments:', project.sections[0].segments);
              if (project.sections[0].segments && project.sections[0].segments.length > 0) {
                console.log('First segment narration:', project.sections[0].segments[0].narrationText);
              }
            }
    
            setTopic(project.title || '');
            setAudience(project.targetAudience || 'general');
            setDuration(projectContent.totalDuration.toString() || '5');
            setVisualStyle(project.visualStyle || 'stick-man');
            setInspiration(project.inspiration || '');
          }
        } catch (err) {
          console.error('Error loading project:', err);
          setError('Failed to load project data. Please try again.');
        } finally {
          // setIsLoading(false);
        }
      };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setError(null);
    try {
      const durationMinutes = parseFloat(duration);
      const script: Script = await generateScript(
        topic,
        audience,
        durationMinutes,
        visualStyle,
        style,
        inspiration
      );
      if (projectId) {
        await updateProjectScript(Number(projectId), script);
        navigate(`/projects/${projectId}/edit-script`);
      }
    } catch (err: any) {
      setError('Failed to generate script. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  // Handler for parsing and saving pasted JSON
  const handleParseJson = async () => {
    setIsParsingJson(true);
    setError(null);
    try {
      const script = await parseScriptJson({
        jsonStr: pastedJson,
        topic,
        targetAudience: audience,
        durationMinutes: parseFloat(duration),
        style,
        visualStyle,
        inspiration,
      });
      if (projectId) {
        await updateProjectScript(Number(projectId), script);
        navigate(`/projects/${projectId}/edit-script`);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to parse and save script.');
    } finally {
      setIsParsingJson(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <button
          type="button"
          className="mb-4 px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 flex items-center gap-2"
          onClick={() => navigate(`/projects/${projectId}`)}
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Project Detail
        </button>
        <h1 className="text-2xl font-bold text-foreground mb-2">Create/Edit Script</h1>

        {/* Paste JSON and parse/save section */}
        <div className="mb-8">
          <label htmlFor="pasted-json" className="block text-sm font-medium text-foreground mb-1">
            Paste Script JSON
          </label>
          <textarea
            id="pasted-json"
            value={pastedJson}
            onChange={(e) => setPastedJson(e.target.value)}
            rows={8}
            className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary font-mono"
            placeholder="Paste raw LLM JSON here..."
          />
          <button
            type="button"
            className="mt-2 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50"
            onClick={handleParseJson}
            disabled={isParsingJson || !pastedJson.trim() || !projectId}
          >
            {isParsingJson ? 'Parsing & Saving...' : 'Parse & Save Script from JSON'}
          </button>
        </div>
        {error && (
          <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-md mb-4">{error}</div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="topic" className="block text-sm font-medium text-foreground mb-1">
              What topic would you like to create a video about?
            </label>
            <input
              type="text"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="e.g., Quantum Computing, Climate Change, Financial Literacy"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label htmlFor="audience" className="block text-sm font-medium text-foreground mb-1">
                Target Audience
              </label>
              <select
                id="audience"
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="beginners">Beginners</option>
                <option value="general">General Audience</option>
                <option value="students">Students</option>
                <option value="professionals">Professionals</option>
                <option value="experts">Experts</option>
              </select>
            </div>
            <div>
              <label htmlFor="duration" className="block text-sm font-medium text-foreground mb-1">
                Approximate Duration (minutes)
              </label>
              <select
                id="duration"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="2">2 minutes</option>
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="15">15 minutes</option>
                <option value="20">20+ minutes</option>
              </select>
            </div>
            <div>
              <label htmlFor="style" className="block text-sm font-medium text-foreground mb-1">
                Visual Style
              </label>
              <select
                id="style"
                value={visualStyle}
                onChange={(e) => setVisualStyle(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="stick-man">Stick Man</option>
                <option value="realistic">Realistic</option>
                <option value="cartoon">Cartoon</option>
                <option value="3d">3D</option>
                <option value="3d-cartoon">3D Cartoon</option>
              </select>
            </div>
          </div>
          <div>
            <label htmlFor="inspiration" className="block text-sm font-medium text-foreground mb-1">
              Inspiration
            </label>
            <textarea
              id="inspiration"
              value={inspiration}
              onChange={(e) => setInspiration(e.target.value)}
              className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="e.g., Pixar, Disney, etc."
              rows={5}
            />
          </div>
          <div className="pt-4">
            <button
              type="submit"
              disabled={isGenerating || !topic}
              className="w-full md:w-auto px-6 py-3 bg-primary text-primary-foreground rounded-md font-medium shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? 'Generating Script...' : 'Generate Script'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
