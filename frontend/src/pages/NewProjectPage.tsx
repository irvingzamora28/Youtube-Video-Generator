import React, { useState } from 'react';
import Layout from '../components/Layout';
import { useNavigate } from 'react-router-dom';
import { createProject, ProjectCreateParams } from '../services/projectApi';

const NewProjectPage: React.FC = () => {

  const navigate = useNavigate();
  const [formData, setFormData] = useState<ProjectCreateParams>({
    title: '',
    description: '',
    targetAudience: 'general',
    visualStyle: '',
    style: 'educational',
    inspiration: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('Project title is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const project = await createProject(formData);
      navigate(`/projects/${project.id}`);
    } catch (err) {
      setError('Failed to create project. Please try again.');
      console.error('Error creating project:', err);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Layout>
      <div className="bg-card shadow rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-foreground mb-6">Create New Project</h1>
          {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded relative mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

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
          <label htmlFor="description" className="block text-sm font-medium mb-1 text-foreground">
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
          <label htmlFor="targetAudience" className="block text-sm font-medium mb-1 text-foreground">
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
          <label htmlFor="visualStyle" className="block text-sm font-medium mb-1 text-foreground">
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
          <label htmlFor="style" className="block text-sm font-medium mb-1 text-foreground">
            Style (optional)
          </label>
          <input
            type="text"
            id="style"
            name="style"
            value={formData.style}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
            placeholder="Describe desired style (e.g. educational, entertaining, etc.)"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="inspiration" className="block text-sm font-medium mb-1 text-foreground">
            Inspiration (optional)
          </label>
          <textarea
            id="inspiration"
            name="inspiration"
            rows={8}
            value={formData.inspiration}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring bg-background text-foreground"
            placeholder="Describe your inspiration or theme for the script"
          />
        </div>
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/projects')}
            className="px-4 py-2 border border-input rounded-md hover:bg-accent text-foreground"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Create Project'}
          </button>
        </div>
      </form>
        </div>
      </div>
    </Layout>
  );
};

export default NewProjectPage;
