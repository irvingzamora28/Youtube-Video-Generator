import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProjectContent, updateProject, ProjectUpdateParams, deleteProject } from '../services/projectApi';
import { Script } from '../types/script';
import ProjectScriptViewer from '../components/ProjectScriptViewer';
import Layout from '../components/Layout';

const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [script, setScript] = useState<Script | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<ProjectUpdateParams>({
    title: '',
    description: '',
    targetAudience: '',
    visualStyle: '',
    inspiration: '',
  });

  useEffect(() => {
    if (id) {
      fetchProject(parseInt(id));
    }
  }, [id]);

  const fetchProject = async (projectId: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getProjectContent(projectId);
      console.log('Project data loaded:', data);
      console.log('Script sections:', data.sections);
      setScript(data);
      setFormData({
        title: data.title,
        description: data.description,
        targetAudience: data.targetAudience,
        visualStyle: data.visualStyle || '',
        inspiration: data.inspiration || '',
      });
    } catch (err) {
      setError('Failed to load project. Please try again.');
      console.error('Error fetching project:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!id || !formData.title?.trim()) {
      setError('Project title is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await updateProject(parseInt(id), formData);

      // Refresh the project data
      await fetchProject(parseInt(id));

      setIsEditing(false);
    } catch (err) {
      setError('Failed to update project. Please try again.');
      console.error('Error updating project:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id || !window.confirm('Are you sure you want to delete this project?')) {
      return;
    }

    try {
      setLoading(true);
      await deleteProject(parseInt(id));
      navigate('/projects');
    } catch (err) {
      setError('Failed to delete project. Please try again.');
      console.error('Error deleting project:', err);
      setLoading(false);
    }
  };

  if (loading && !script) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error && !script) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold mb-4">Project not found</h2>
        <button
          onClick={() => navigate('/projects')}
          className="bg-primary hover:bg-primary-dark text-white font-bold py-2 px-4 rounded"
        >
          Back to Projects
        </button>
      </div>
    );
  }

  return (
    <Layout>
      {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded relative mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => navigate('/projects')}
          className="text-primary hover:text-primary/80 hover:underline flex items-center"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Projects
        </button>

        <div className="flex space-x-2">
          {!isEditing && (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded"
              >
                Edit Project
              </button>
              <button
                onClick={handleDelete}
                className="bg-destructive hover:bg-destructive/90 text-destructive-foreground font-bold py-2 px-4 rounded"
              >
                Delete
              </button>
            </>
          )}
        </div>
      </div>

      {isEditing ? (
        <div className="bg-card rounded-lg shadow-md p-6 mb-8 border border-border">
          <h2 className="text-2xl font-bold mb-6 text-foreground">Edit Project</h2>

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="title" className="block text-sm font-medium mb-1 text-foreground">
                Project Title <span className="text-destructive">*</span>
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
                placeholder="Enter project title"
                required
              />
            </div>

            <div className="mb-4">
              <label htmlFor="description" className="block text-sm font-medium mb-1">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={4}
                className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
                placeholder="Enter project description"
              />
            </div>

            <div className="mb-6">
              <label htmlFor="targetAudience" className="block text-sm font-medium mb-1">
                Target Audience
              </label>
              <input
                type="text"
                id="targetAudience"
                name="targetAudience"
                value={formData.targetAudience}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
                placeholder="Enter target audience"
              />
            </div>

            <div className="mb-6">
              <label htmlFor="visualStyle" className="block text-sm font-medium mb-1">
                Visual Style (optional)
              </label>
              <input
                type="text"
                id="visualStyle"
                name="visualStyle"
                value={formData.visualStyle}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
                placeholder="Describe desired visual style (e.g. stickman, minimal, whiteboard, etc.)"
              />
            </div>

            <div className="mb-6">
              <label htmlFor="inspiration" className="block text-sm font-medium mb-1">
                Inspiration (optional)
              </label>
              <textarea
                id="inspiration"
                name="inspiration"
                value={formData.inspiration}
                onChange={handleChange}
                rows={8}
                className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
                placeholder="Describe your inspiration or theme for the script"
              />
            </div>
            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => setIsEditing(false)}
                className="px-4 py-2 border border-input rounded-md hover:bg-accent text-foreground"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      ) : (
        <div className="bg-card rounded-lg shadow-md p-6 mb-8 border border-border">
          <h1 className="text-3xl font-bold mb-2 text-foreground">{script.title}</h1>

          {script.description && (
            <p className="text-muted-foreground mb-4">{script.description}</p>
          )}

          <div className="mb-4">
            <span className="text-muted-foreground">Visual Style:</span>
            <span className="ml-2 text-foreground">{script.visualStyle ? script.visualStyle : 'Not specified'}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <span className="text-muted-foreground">Target Audience:</span>
              <span className="ml-2 text-foreground">{script.targetAudience || 'Not specified'}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Status:</span>
              <span className="ml-2 capitalize text-foreground">{script.status}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Created:</span>
              <span className="ml-2 text-foreground">{new Date(script.createdAt).toLocaleDateString()}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Last Updated:</span>
              <span className="ml-2 text-foreground">{new Date(script.updatedAt).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Background Image Upload */}
          <div className="mb-4">
            <span className="text-muted-foreground font-semibold">Background Image:</span>
            <div className="flex items-center mt-2 space-x-4">
              {script.background_image && (
                <img
                  src={`/${script.background_image}`}
                  alt="Background Preview"
                  style={{ maxWidth: 200, maxHeight: 120, borderRadius: 8, border: '1px solid #ddd' }}
                />
              )}
              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  const input = e.currentTarget.elements.namedItem('bgImage') as HTMLInputElement;
                  if (!input?.files?.[0] || !id) return;
                  setLoading(true);
                  setError(null);
                  try {
                    // @ts-ignore
                    const { uploadBackgroundImage } = await import('../services/projectApi');
                    await uploadBackgroundImage(parseInt(id), input.files[0]);
                    await fetchProject(parseInt(id));
                  } catch (err: any) {
                    setError('Failed to upload background image.');
                  } finally {
                    setLoading(false);
                  }
                }}
              >
                <input
                  type="file"
                  name="bgImage"
                  accept="image/*"
                  className="block text-sm text-foreground file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/80"
                  disabled={loading}
                />
                <button
                  type="submit"
                  className="ml-2 px-3 py-2 bg-primary text-primary-foreground rounded hover:bg-primary/90 disabled:opacity-50"
                  disabled={loading}
                >
                  {loading ? 'Uploading...' : 'Upload'}
                </button>
              </form>
            </div>
            <span className="block text-xs text-muted-foreground mt-1">Accepted: PNG, JPG, JPEG. For best results, use a 16:9 aspect ratio.</span>
          </div>
        </div>
      )}

      <div className="bg-card rounded-lg shadow-md p-6 border border-border">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Script</h2>
          <div className="space-x-2">
            {script.sections.length > 0 && (
              <button
                onClick={() => navigate(`/projects/${id}/edit-script`)}
                className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-bold py-2 px-4 rounded"
              >
                Edit Script
              </button>
            )}
           
             {/* Add Link to Timeline Editor */}
             {script.sections.length > 0 && (
               <>
                 <button
                   onClick={() => navigate(`/projects/${id}/timeline`)}
                   className="bg-accent hover:bg-accent/90 text-accent-foreground font-bold py-2 px-4 rounded"
                 >
                   Visual Timeline Editor
                 </button>
                 <button
                   onClick={() => navigate(`/projects/${id}/infocards`)}
                   className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
                   style={{ marginLeft: '0.5rem' }}
                 >
                   Infocard Generator
                 </button>
                 <button
                   onClick={() => navigate(`/projects/${id}/short`)}
                   className="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 rounded"
                   style={{ marginLeft: '0.5rem' }}
                 >
                   Generate Short
                 </button>
               </>
             )}
          </div>
        </div>

        {script.sections.length === 0 ? (
          <div className="text-center py-12">
            <h3 className="text-xl font-semibold mb-4">No script content yet</h3>
            <p className="mb-6">Start by generating a script or creating sections manually</p>
            <button
              onClick={() => navigate(`/projects/${id}/generate-script`)}
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded"
            >
              Generate Script
            </button>
          </div>
        ) : (
          <ProjectScriptViewer script={script} />
        )}
      </div>
    </Layout>
  );
};

export default ProjectDetail;
