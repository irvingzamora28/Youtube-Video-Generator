import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { getProjectFullScript } from "../services/projectApi";
import { getInfocardHighlights, generateInfocardHighlights, generateHighlightImages, addTextToHighlightImages, getProjectSocialPosts } from "../services/infocardHighlightApi";
import { keysToCamel } from "../utils/caseUtils";
import { InfocardHighlight } from "../types/infocardHighlight";
import { generateSocialPosts } from "../services/socialApi";

const normalizeUrl = (path?: string) => {
  if (!path) return undefined;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  // Default API URL for static files
  const base = import.meta?.env?.VITE_API_BASE_URL || 'http://localhost:8000';
  return `${base}${path}`;
};

const ProjectInfocards: React.FC = () => {
  const [socialPosts, setSocialPosts] = React.useState<any>(null);
  const [generatingPosts, setGeneratingPosts] = React.useState(false);

  const handleGenerateSocialPosts = async () => {
    setGeneratingPosts(true);
    setError(null);
    try {
      // Assuming you have projectId in scope, e.g. from route params or props
      const projectId = Number(window.location.pathname.split("/").find((v, i, arr) => arr[i - 1] === "projects"));
      const result = await generateSocialPosts(projectId);
      setSocialPosts(result.social_posts);
    } catch (e: any) {
      setError(e?.message || 'Failed to generate social posts');
    } finally {
      setGeneratingPosts(false);
    }
  };


  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [script, setScript] = useState<string | null>(null);
  const [loadingScript, setLoadingScript] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [highlights, setHighlights] = useState<InfocardHighlight[]>([]);
  const [loadingHighlights, setLoadingHighlights] = useState(false);
  const [loadingGenerate, setLoadingGenerate] = useState(false);
  const [loadingGenerateImages, setLoadingGenerateImages] = useState(false);
  const [loadingAddText, setLoadingAddText] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoadingScript(true);
    getProjectFullScript(Number(id))
      .then(setScript)
      .catch((err) => setError(err.message))
      .finally(() => setLoadingScript(false));
    // Fetch existing highlights
    getInfocardHighlights(Number(id))
      .then((res) => setHighlights(keysToCamel(res.highlights)))
      .catch(() => setHighlights([]));
    // Fetch project-level social posts
    getProjectSocialPosts(Number(id))
      .then((res) => setSocialPosts(res.social_posts))
      .catch(() => setSocialPosts(null));
  }, [id]);

  const handleGenerateHighlights = async () => {
    if (!id) return;
    setLoadingGenerate(true);
    setError(null);
    try {
      const res = await generateInfocardHighlights(Number(id));
      setHighlights(keysToCamel(res.highlights));
    } catch (err: any) {
      setError(err.message || 'Failed to generate highlights');
    } finally {
      setLoadingGenerate(false);
    }
  };

  const handleGenerateHighlightImages = async () => {
    if (!id) return;
    setLoadingGenerateImages(true);
    setError(null);
    try {
      const res = await generateHighlightImages(Number(id));
      setHighlights(keysToCamel(res.highlights));
    } catch (err: any) {
      setError(err.message || 'Failed to generate highlight images');
    } finally {
      setLoadingGenerateImages(false);
    }
  };

  const handleAddTextToHighlightImages = async () => {
    if (!id) return;
    setLoadingAddText(true);
    setError(null);
    try {
      const res = await addTextToHighlightImages(Number(id));
      setHighlights(keysToCamel(res.highlights));
    } catch (err: any) {
      setError(err.message || 'Failed to add text to highlight images');
    } finally {
      setLoadingAddText(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Infocard Generator</h1>
          <button
            className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-bold py-2 px-4 rounded"
            onClick={() => navigate(`/projects/${id}`)}
          >
            Back to Project
          </button>
        </div>
        <div className="bg-card rounded-lg shadow-md p-6 border border-border">
          <h2 className="text-xl font-semibold mb-4">Infocards for Project {id}</h2>
  
          {loadingScript && (
            <div className="text-muted-foreground">Loading script...</div>
          )}
  
          {error && (
            <div className="text-red-600 font-semibold mb-4">{error}</div>
          )}
  
          {script ? (
            <>
              <div className="mb-4">
                <button
                  className="bg-primary hover:bg-primary/90 text-white font-bold py-2 px-4 rounded mr-2"
                  onClick={handleGenerateHighlights}
                  disabled={loadingGenerate}
                >
                  {loadingGenerate ? "Generating Highlights..." : "Generate Highlights"}
                </button>
                <button
                  className="bg-accent hover:bg-accent/90 text-accent-foreground font-bold py-2 px-4 rounded mr-2"
                  onClick={handleGenerateHighlightImages}
                  disabled={loadingGenerateImages || loadingGenerate}
                >
                  {loadingGenerateImages ? "Generating Images..." : "Generate Highlight Images"}
                </button>
                <button
                  className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-bold py-2 px-4 rounded"
                  onClick={handleAddTextToHighlightImages}
                  disabled={loadingAddText || loadingGenerateImages || loadingGenerate}
                >
                  {loadingAddText ? "Adding Text..." : "Add Text to Highlight Images"}
                </button>
              </div>
  
              {highlights.length > 0 && (
                <div>
                  <h2 className="text-xl font-bold mb-2">Highlights</h2>
                  <button
                    className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                    onClick={handleGenerateSocialPosts}
                    disabled={generatingPosts}
                  >
                    {generatingPosts ? 'Generating Social Posts...' : 'Generate Social Posts'}
                  </button>

                  {socialPosts && (
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold mb-2">Social Post Options</h3>
                      <div className="flex flex-row gap-4">
                        {['twitter', 'youtube', 'facebook'].map(platform => (
                          <div key={platform} className="p-4 border rounded bg-card max-w-xs border-border">
                            <div className="font-bold mb-2 capitalize text-foreground">{platform}</div>
                            {Array.isArray(socialPosts[platform]) ? (
                              <ul>
                                {socialPosts[platform].map((postObj, idx) => (
                                  <li key={idx} className="mb-2 text-foreground">
                                    {postObj.post || JSON.stringify(postObj)}
                                  </li>
                                ))}
                              </ul>
                            ) : (
                              <div className="whitespace-pre-line text-foreground">{socialPosts[platform] || 'No posts available.'}</div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
  
                  <ul className="list-disc pl-6">
                    {highlights.map((hl, idx) => (
                      <li key={idx} className="mb-4">
                        <div className="font-semibold">{hl.text}</div>
                        {hl.postText && <div className="text-lg text-foreground">Post Text: {hl.postText}</div>}
                        <div className="text-sm text-foreground">Visual: {hl.visualDescription}</div>
                        {hl.storyContext && <div className="text-xs text-foreground">Context: {hl.storyContext}</div>}
                        <div className="mt-2 flex flex-row gap-4">
                          {hl.imageUrl && (
                            <div className="flex flex-col items-center">
                              <span className="text-xs text-foreground mb-1">Original</span>
                              <img
                                src={normalizeUrl(hl.imageUrl)}
                                alt={hl.visualDescription || hl.text}
                                className="rounded border border-border max-w-xs max-h-48"
                                loading="lazy"
                              />
                            </div>
                          )}
                          {hl.imageUrlWithText && (
                            <div className="flex flex-col items-center">
                              <span className="text-xs text-muted-foreground mb-1">With Text</span>
                              <img
                                src={normalizeUrl(hl.imageUrlWithText)}
                                alt={hl.visualDescription || hl.text}
                                className="rounded border border-border max-w-xs max-h-48"
                                loading="lazy"
                              />
                            </div>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <div className="text-muted-foreground">No script found for this project.</div>
          )}
        </div>
      </div>
    </Layout>
  );
  
};

export default ProjectInfocards;
