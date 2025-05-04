import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../components/Layout';
import { generateShortScript } from '../services/api';
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
        {error && <div className="text-red-600 mb-2">{error}</div>}
        {saveStatus && <div className="text-green-600 mb-2">{saveStatus}</div>}
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
