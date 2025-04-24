import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Script } from '../types/script';
import { getProject } from '../services/projectApi';
import { generateVideo, getVideoStatus } from '../services/api';
// Import the new timeline component
import VisualTimeline from '../components/VisualTimeline';
import VisualTimelineEditor from '../components/VisualTimelineEditor';

const VisualTimelineEditorPage: React.FC = () => {
  // --- Enhancement for segment click-to-seek in editor ---
  const [selectedSegmentIndex, setSelectedSegmentIndex] = useState<number | null>(null);
  const [videoTaskId, setVideoTaskId] = useState<string | null>(null);
  const [videoStatus, setVideoStatus] = useState<'idle'|'pending'|'processing'|'completed'|'error'>('idle');
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [videoError, setVideoError] = useState<string | null>(null);

  // Poll video status if a task is running
  useEffect(() => {
    let interval: any = null; // Use 'any' to avoid NodeJS namespace error
    if (videoTaskId && (videoStatus === 'pending' || videoStatus === 'processing')) {
      interval = setInterval(async () => {
        try {
          const statusResp = await getVideoStatus(videoTaskId);
          setVideoStatus(statusResp.status as any);
          if (statusResp.status === 'completed' && statusResp.video_url) {
            setVideoUrl(statusResp.video_url);
            if (interval) clearInterval(interval);
          } else if (statusResp.status === 'error') {
            setVideoError(statusResp.error || 'Video generation failed');
            if (interval) clearInterval(interval);
          }
        } catch (err: any) {
          setVideoError(err.message || 'Failed to get video status');
          if (interval) clearInterval(interval);
        }
      }, 2000);
    }
    return () => { if (interval) clearInterval(interval); };
  }, [videoTaskId, videoStatus]);

  const handleGenerateVideo = async () => {
    if (!projectId) return;
    setVideoTaskId(null);
    setVideoStatus('idle');
    setVideoUrl(null);
    setVideoError(null);
    try {
      const resp = await generateVideo(Number(projectId));
      setVideoTaskId(resp.task_id);
      setVideoStatus('pending');
    } catch (err: any) {
      setVideoError(err.message || 'Failed to start video generation');
    }
  };

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
              onClick={handleGenerateVideo}
              className="bg-accent hover:bg-accent/90 text-accent-foreground font-bold py-2 px-4 rounded mr-2"
              disabled={videoStatus === 'pending' || videoStatus === 'processing'}
              title="Generate a YouTube-ready video from this project"
            >
              {videoStatus === 'pending' || videoStatus === 'processing' ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-5 w-5 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Generating Video...
                </>
              ) : (
                'Generate Video'
              )}
            </button>
            <button
              onClick={() => navigate(`/projects/${projectId}`)} // Link back to project detail
              className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-bold py-2 px-4 rounded"
            >
              Back to Project
            </button>
        </div>
        </div>
        {/* Video Generation Status & Link */}
        {(videoStatus === 'pending' || videoStatus === 'processing') && (
          <div className="mb-4 flex items-center text-accent">
            <svg className="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating video... This may take a few minutes.
          </div>
        )}
        {videoStatus === 'completed' && videoUrl && (
          <div className="mb-4">
            <a href={videoUrl} target="_blank" rel="noopener noreferrer" className="text-green-700 font-bold underline">
              Download/View Generated Video
            </a>
          </div>
        )}
        {videoStatus === 'error' && videoError && (
          <div className="mb-4 text-destructive font-bold">
            Video generation failed: {videoError}
          </div>
        )}
        </div>

        <VisualTimeline 
          ref={timelineRef} 
          script={script} 
          onSegmentSelectForEditor={setSelectedSegmentIndex}
        />
        <VisualTimelineEditor 
          script={script} 
          onScriptUpdate={setScript} 
          projectId={projectId ? parseInt(projectId) : 0} 
          scrollToSegmentIndex={selectedSegmentIndex}
        />
    </Layout>
  );
}

export default VisualTimelineEditorPage;
