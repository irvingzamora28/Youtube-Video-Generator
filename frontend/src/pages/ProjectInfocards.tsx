import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { getProjectFullScript } from "../services/projectApi";
import { getInfocardHighlights, generateInfocardHighlights } from "../services/infocardHighlightApi";
import { InfocardHighlight } from "../types/infocardHighlight";

const ProjectInfocards: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [script, setScript] = useState<string | null>(null);
  const [loadingScript, setLoadingScript] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [highlights, setHighlights] = useState<InfocardHighlight[]>([]);
  const [loadingHighlights, setLoadingHighlights] = useState(false);
  const [loadingGenerate, setLoadingGenerate] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoadingScript(true);
    getProjectFullScript(Number(id))
      .then(setScript)
      .catch((err) => setError(err.message))
      .finally(() => setLoadingScript(false));
    // Fetch existing highlights
    getInfocardHighlights(Number(id))
      .then((res) => setHighlights(res.highlights))
      .catch(() => setHighlights([]));
  }, [id]);

  const handleGenerateHighlights = async () => {
    if (!id) return;
    setLoadingGenerate(true);
    setError(null);
    try {
      const res = await generateInfocardHighlights(Number(id));
      setHighlights(res.highlights);
    } catch (err: any) {
      setError(err.message || 'Failed to generate highlights');
    } finally {
      setLoadingGenerate(false);
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
          {loadingScript ? (
            <div className="text-muted-foreground">Loading script...</div>
          ) : error ? (
            <div className="text-destructive">{error}</div>
          ) : script ? (
            <>
              <div className="mb-4">
                <button
                  className="bg-primary hover:bg-primary/90 text-white font-bold py-2 px-4 rounded"
                  onClick={handleGenerateHighlights}
                  disabled={loadingGenerate}
                >
                  {loadingGenerate ? "Generating Highlights..." : "Generate Highlights"}
                </button>
              </div>
              {highlights.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-2">Extracted Highlights</h3>
                  <ul className="list-disc pl-6">
                    {highlights.map((hl, idx) => (
                      <li key={idx} className="mb-2">
                        <div className="font-semibold">{hl.text}</div>
                        <div className="text-sm text-muted-foreground">Visual: {hl.visualDescription}</div>
                        {hl.storyContext && <div className="text-xs text-gray-500">Context: {hl.storyContext}</div>}
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
