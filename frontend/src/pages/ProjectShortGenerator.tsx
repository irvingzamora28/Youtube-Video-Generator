import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import { generateShortScript, generateAllShortProjectAudio, generateAllShortProjectVisuals, generateShortVideo, getVideoStatus } from '../services/api';
import { Script } from '../types/script';
import { getProjectShortContent, updateProjectShortScript } from '../services/projectApi';

const ProjectShortGenerator: React.FC = () => {
  const { id: projectId } = useParams<{ id: string }>();

  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [shortScript, setShortScript] = useState<any>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  // State for bulk audio generation for short script
  const [isGeneratingAudios, setIsGeneratingAudios] = useState(false);
  const [audioGenStatus, setAudioGenStatus] = useState<string | null>(null);
  // State for bulk visuals generation for short script
  const [isGeneratingVisuals, setIsGeneratingVisuals] = useState(false);
  const [visualGenStatus, setVisualGenStatus] = useState<string | null>(null);
  // State for short video generation
  const [isGeneratingShortVideo, setIsGeneratingShortVideo] = useState(false);
  const [shortVideoStatus, setShortVideoStatus] = useState<string | null>(null);
  const [shortVideoUrl, setShortVideoUrl] = useState<string | null>(null);
  const [shortVideoTaskId, setShortVideoTaskId] = useState<string | null>(null);

  useEffect(() => {
      if (projectId) {
        loadProjectData(parseInt(projectId));
      }
    }, [projectId]);
  
    const loadProjectData = async (id: number) => {
      try {
        setIsLoading(true);
        setError(null);
        const project = await getProjectShortContent(id);
  
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
          setShortScript(project);
        }
      } catch (err) {
        console.error('Error loading project:', err);
        setError('Failed to load project data. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

  const handleGenerateShort = async () => {
    if (!projectId) return;
    setIsGenerating(true);
    setError(null);
    setShortScript(null);
    setSaveStatus(null);
    try {
      // Use simple defaults for now; these could be editable fields later
      const script = await generateShortScript(
        Number(projectId),
        '', // topic (let backend use project default)
        '', // targetAudience (let backend use project default)
        'educational', // style
        'modern', // visualStyle
        '' // inspiration
      );
      setShortScript(script);
      // Save to project.short_content
      await saveShortScriptToProject(script);
      setSaveStatus('Short script saved to project!');
    } catch (err: any) {
      setError(err.message || 'Failed to generate or save short script.');
    } finally {
      setIsGenerating(false);
    }
  };


  const saveShortScriptToProject = async (script: Script) => {
      if (!projectId) return;
  
      try {
        setIsSaving(true);
        await updateProjectShortScript(parseInt(projectId), script);
      } catch (error) {
        console.error('Error saving script to project:', error);
        setError('Failed to save script to project. Please try again.');
      } finally {
        setIsSaving(false);
      }
    };

  // Handler for generating all audios for the short script
  const handleGenerateAllShortAudios = async () => {
    if (!projectId) return;
    setIsGeneratingAudios(true);
    setAudioGenStatus(null);
    setError(null);
    try {
      const resp = await generateAllShortProjectAudio(Number(projectId));
      setAudioGenStatus(resp.message || 'Audio generation for short script started!');
    } catch (err: any) {
      setError(err.message || 'Failed to start audio generation for short script.');
    } finally {
      setIsGeneratingAudios(false);
    }
  };

  // Handler for generating all visuals for the short script
  const handleGenerateAllShortVisuals = async () => {
    if (!projectId) return;
    setIsGeneratingVisuals(true);
    setVisualGenStatus(null);
    setError(null);
    try {
      const resp = await generateAllShortProjectVisuals(Number(projectId));
      if (resp.errors && resp.errors.length > 0) {
        setVisualGenStatus(`Visuals generated with ${resp.errors.length} errors.`);
      } else {
        setVisualGenStatus('Visuals generation for short script completed!');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to generate visuals for short script.');
    } finally {
      setIsGeneratingVisuals(false);
    }
  };

  // Handler for organizing all visuals for the short script
  const [isOrganizingVisuals, setIsOrganizingVisuals] = useState(false);
  const [organizeVisualStatus, setOrganizeVisualStatus] = useState<string | null>(null);
  const handleOrganizeAllShortVisuals = async () => {
    if (!projectId) return;
    setIsOrganizingVisuals(true);
    setOrganizeVisualStatus(null);
    setError(null);
    try {
      const resp = await import('../services/api').then(mod => mod.organizeAllShortProjectVisuals(Number(projectId)));
      setOrganizeVisualStatus(resp.message || 'Visuals organization for short script completed!');
    } catch (err: any) {
      setError(err.message || 'Failed to organize visuals for short script.');
    } finally {
      setIsOrganizingVisuals(false);
    }
  };


  // Handler for generating the short video
  const handleGenerateShortVideo = async () => {
    if (!projectId) return;
    setIsGeneratingShortVideo(true);
    setShortVideoStatus('Starting short video generation...');
    setShortVideoUrl(null);
    setShortVideoTaskId(null);
    setError(null);
    try {
      const resp = await generateShortVideo(Number(projectId));
      setShortVideoTaskId(resp.task_id);
      setShortVideoStatus('Video generation started. Waiting for completion...');
      // Poll status
      pollShortVideoStatus(resp.task_id);
    } catch (err: any) {
      setError(err.message || 'Failed to start short video generation.');
      setShortVideoStatus(null);
      setIsGeneratingShortVideo(false);
    }
  };

  // Polling function for video status
  const pollShortVideoStatus = async (taskId: string) => {
    let attempts = 0;
    const maxAttempts = 120; // e.g., poll for up to 10 minutes
    const poll = async () => {
      try {
        const statusResp = await getVideoStatus(taskId);
        if (statusResp.status === 'completed') {
          setShortVideoStatus('Short video generation complete!');
          setShortVideoUrl(statusResp.video_url || null);
          setIsGeneratingShortVideo(false);
          return;
        } else if (statusResp.status === 'error') {
          setShortVideoStatus('Short video generation failed.');
          setError(statusResp.error || 'Unknown error during video generation.');
          setIsGeneratingShortVideo(false);
          return;
        } else {
          setShortVideoStatus(`Short video status: ${statusResp.status}...`);
        }
      } catch (err: any) {
        setShortVideoStatus('Error polling video status.');
        setError(err.message || 'Failed to poll video status.');
        setIsGeneratingShortVideo(false);
        return;
      }
      attempts++;
      if (attempts < maxAttempts) {
        setTimeout(poll, 5000); // poll every 5 seconds
      } else {
        setShortVideoStatus('Timed out waiting for video generation.');
        setIsGeneratingShortVideo(false);
      }
    };
    poll();
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto py-8">
        <h1 className="text-2xl font-bold mb-4">Generate Short Video</h1>
        <p>This page will allow you to generate a 59-second short video for Project ID: {projectId}.</p>
        <button
          className="bg-blue-600 hover:bg-blue-700 text-foreground font-bold py-2 px-4 rounded mb-4"
          onClick={handleGenerateShort}
          disabled={isGenerating || isSaving}
        >
          {isGenerating ? 'Generating...' : 'Generate Short Script'}
        </button>
        <button
          className="bg-green-600 hover:bg-green-700 text-foreground font-bold py-2 px-4 rounded mb-4 ml-2"
          onClick={handleGenerateAllShortAudios}
          disabled={isGeneratingAudios || isLoading}
        >
          {isGeneratingAudios ? 'Generating Audios...' : 'Generate All Audios for Short'}
        </button>
        <button
          className="bg-purple-600 hover:bg-purple-700 text-foreground font-bold py-2 px-4 rounded mb-4 ml-2"
          onClick={handleGenerateAllShortVisuals}
          disabled={isGeneratingVisuals || isLoading}
        >
          {isGeneratingVisuals ? 'Generating Visuals...' : 'Generate All Visuals for Short'}
        </button>
        <button
          className="bg-yellow-600 hover:bg-yellow-700 text-foreground font-bold py-2 px-4 rounded mb-4 ml-2"
          onClick={handleOrganizeAllShortVisuals}
          disabled={isOrganizingVisuals || isLoading}
        >
          {isOrganizingVisuals ? 'Organizing Visuals...' : 'Organize All Visuals for Short'}
        </button>
        <button
          className="bg-pink-600 hover:bg-pink-700 text-foreground font-bold py-2 px-4 rounded mb-4 ml-2"
          onClick={handleGenerateShortVideo}
          disabled={isGeneratingShortVideo || isLoading}
        >
          {isGeneratingShortVideo ? 'Generating Short Video...' : 'Generate Short Video'}
        </button>
        {shortVideoStatus && <div className="text-pink-600 mb-2">{shortVideoStatus}</div>}
        {shortVideoUrl && (
          <div className="mb-2">
            <a href={shortVideoUrl} target="_blank" rel="noopener noreferrer" className="text-blue-700 underline">Download/View Short Video</a>
          </div>
        )}
        {error && <div className="text-red-600 mb-2">{error}</div>}
        {saveStatus && <div className="text-green-600 mb-2">{saveStatus}</div>}
        {audioGenStatus && <div className="text-green-600 mb-2">{audioGenStatus}</div>}
        {visualGenStatus && <div className="text-purple-600 mb-2">{visualGenStatus}</div>}
        {organizeVisualStatus && <div className="text-yellow-600 mb-2">{organizeVisualStatus}</div>}
        {shortScript && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Generated Short Script (Raw JSON):</h2>
            <pre className="bg-card p-4 rounded text-sm text-foreground border border-border overflow-x-auto">
              {JSON.stringify(shortScript, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ProjectShortGenerator;
