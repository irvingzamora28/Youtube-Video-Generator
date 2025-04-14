import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProjects, ProjectListItem, deleteProject } from '../services/projectApi';
import Layout from '../components/Layout';

const ProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<ProjectListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getProjects();
      setProjects(data);
    } catch (err) {
      setError('Failed to load projects. Please try again.');
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProject = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this project?')) {
      return;
    }

    try {
      await deleteProject(id);
      setProjects(projects.filter(project => project.id !== id));
    } catch (err) {
      setError('Failed to delete project. Please try again.');
      console.error('Error deleting project:', err);
    }
  };

  const formatDuration = (seconds: number): string => {
    if (!seconds) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const formatDate = (date: Date): string => {
    return new Date(date).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error!</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  return (
    <Layout>
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">My Projects</h1>

        {projects.length > 0 && (
        <Link
          to="/projects/new"
          className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded"
        >
          Create New Project
        </Link>
        )}
      </div>

      {projects.length === 0 ? (
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-4">No projects yet</h2>
          <p className="mb-6">Create your first video project to get started</p>
          <Link
            to="/projects/new"
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded"
          >
            Create New Project
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <div key={project.id} className="border border-border rounded-lg overflow-hidden shadow-lg bg-card">
              <div className="p-6">
                <h2 className="text-xl font-bold mb-2 text-foreground">{project.title}</h2>
                <p className="text-muted-foreground mb-4 line-clamp-2">{project.description}</p>

                <div className="flex justify-between text-sm text-muted-foreground mb-4">
                  <span>Duration: {formatDuration(project.totalDuration)}</span>
                  <span className="capitalize">Status: {project.status}</span>
                </div>

                <div className="text-sm text-muted-foreground mb-4">
                  <p>Created: {formatDate(project.createdAt)}</p>
                  <p>Last updated: {formatDate(project.updatedAt)}</p>
                </div>

                <div className="flex justify-between mt-4">
                  <Link
                    to={`/projects/${project.id}`}
                    className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDeleteProject(project.id)}
                    className="bg-destructive hover:bg-destructive/90 text-destructive-foreground font-bold py-2 px-4 rounded"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
    </Layout>
  );
};

export default ProjectsPage;
