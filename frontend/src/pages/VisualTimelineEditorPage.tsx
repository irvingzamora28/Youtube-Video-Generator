import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Script } from '../types/script';
import { getProject } from '../services/projectApi';
// Import the new timeline component
import VisualTimeline from '../components/VisualTimeline';

const VisualTimelineEditorPage: React.FC = () => {
  const { id: projectId } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [script, setScript] = useState<Script | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (projectId) {
      fetchProject(parseInt(projectId));
    } else {
      setError("Project ID is missing.");
      setLoading(false);
    }
  }, [projectId]);

  const fetchProject = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getProject(id);
      console.log('Project data loaded for timeline:', data);
      if (!data || !data.sections) {
        throw new Error("Loaded project data is missing sections.");
      }
      setScript(data);
    } catch (err) {
      setError(`Failed to load project: ${err instanceof Error ? err.message : 'Unknown error'}`);
      console.error('Error fetching project:', err);
      setScript(null); // Clear script on error
    } finally {
      setLoading(false);
    }
  };

  // Ref to control VisualTimeline
  const timelineRef = useRef<{ playAllSegments: () => void }>(null);

  const handlePlayAllAudio = () => {
    if (timelineRef.current) {
      timelineRef.current.playAllSegments();
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
          <p className="ml-4 text-muted-foreground">Loading Project...</p>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded relative mb-4" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
          <button
            onClick={() => navigate('/projects')}
            className="ml-4 bg-destructive text-destructive-foreground font-bold py-1 px-2 rounded text-xs"
          >
            Back to Projects
          </button>
        </div>
      </Layout>
    );
  }

  if (!script) {
    // This case might be redundant if error handles !script, but good for clarity
    return <Layout><p className="text-center text-muted-foreground">Project data could not be loaded.</p></Layout>;
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-foreground">{script.title} - Visual Timeline</h1>
          <div>
            <button
              onClick={handlePlayAllAudio}
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded mr-2"
              title="Play narration audio for all segments sequentially"
            >
              Play Full Audio
            </button>
             <button
              onClick={() => navigate(`/projects/${projectId}`)} // Link back to project detail
              className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-bold py-2 px-4 rounded"
            >
              Back to Project
            </button>
          </div>
        </div>

        {/* Placeholder for Timeline Component */}
        {/* Render Timeline Component */}
        <VisualTimeline ref={timelineRef} script={script} />

      </div>
    </Layout>
  );
};

export default VisualTimelineEditorPage;
