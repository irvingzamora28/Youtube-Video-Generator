import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Script, ScriptSegment, ScriptSection } from '../types/script';
import SegmentEditor from '../components/SegmentEditor';
import SectionRegenerator from '../components/SectionRegenerator';
import ScriptVisualizer from '../components/ScriptVisualizer';
import SegmentTimeline from '../components/SegmentTimeline';
// Import the new API functions
import { generateScript, generateAllProjectAudio, generateAllProjectImages, organizeAllProjectVisuals } from '../services/api'; // Add organizeAllProjectVisuals
import { getProject, updateProjectScript } from '../services/projectApi';

export default function ScriptGenerator() {
  const { id: projectId } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [duration, setDuration] = useState('5');
  const [style, setStyle] = useState('educational');
  const [visualStyle, setVisualStyle] = useState('stick-man');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedScript, setGeneratedScript] = useState<Script | null>(null);
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null);
  const [activeSegmentId, setActiveSegmentId] = useState<string | null>(null);
  const [showSegmentEditor, setShowSegmentEditor] = useState(false);
  const [showSectionRegenerator, setShowSectionRegenerator] = useState(false);
  const [showScriptVisualizer, setShowScriptVisualizer] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [bulkAudioStatus, setBulkAudioStatus] = useState<string | null>(null);
  const [bulkImageStatus, setBulkImageStatus] = useState<string | null>(null);
  const [bulkOrganizeStatus, setBulkOrganizeStatus] = useState<string | null>(null); // For bulk organize status

  // Load project data if projectId is provided
  useEffect(() => {
    if (projectId) {
      loadProjectData(parseInt(projectId));
    }
  }, [projectId]);

  const loadProjectData = async (id: number) => {
    try {
      setIsLoading(true);
      setError(null);
      const project = await getProject(id);

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

        setGeneratedScript(project);
        setTopic(project.title || '');
        setStyle(project.style || 'educational');
        setAudience(project.targetAudience || 'general');
        setVisualStyle(project.visualStyle || 'stick-man');
      }
    } catch (err) {
      console.error('Error loading project:', err);
      setError('Failed to load project data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setError(null);

    try {
      // Call the API to generate the script
      const durationMinutes = parseFloat(duration);
      const script = await generateScript(topic, audience, durationMinutes, visualStyle, style);
      setGeneratedScript(script);

      // If we're editing a project, save the script to the project
      if (projectId) {
        await saveScriptToProject(script);
      }
    } catch (error) {
      console.error('Error generating script:', error);
      setError('Failed to generate script. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const saveScriptToProject = async (script: Script) => {
    if (!projectId) return;

    try {
      setIsSaving(true);
      await updateProjectScript(parseInt(projectId), script);
    } catch (error) {
      console.error('Error saving script to project:', error);
      setError('Failed to save script to project. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  // Function to trigger bulk image generation
  const handleGenerateAllImages = async () => {
    if (!projectId) return;
    setBulkImageStatus("Starting image generation...");
    setError(null); // Clear previous errors
    try {
      const result = await generateAllProjectImages(parseInt(projectId));
      setBulkImageStatus(result.message || "Image generation started in background.");
    } catch (err) {
      console.error("Error triggering bulk image generation:", err);
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(`Failed to start bulk image generation: ${message}`);
      setBulkImageStatus(null);
    }
  };

  // Function to trigger bulk visual organization
  const handleOrganizeAllVisuals = async () => {
    if (!projectId) return;
    setBulkOrganizeStatus("Starting visual organization...");
    setError(null); // Clear previous errors
    try {
      const result = await organizeAllProjectVisuals(parseInt(projectId));
      setBulkOrganizeStatus(result.message || "Visual organization started in background.");
    } catch (err) {
      console.error("Error triggering bulk visual organization:", err);
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(`Failed to start bulk visual organization: ${message}`);
      setBulkOrganizeStatus(null);
    }
  };

  // Function to trigger bulk audio generation
  const handleGenerateAllAudios = async () => {
    if (!projectId) return;
    setBulkAudioStatus("Starting audio generation...");
    setError(null);
    try {
      const result = await generateAllProjectAudio(parseInt(projectId));
      setBulkAudioStatus(result.message || "Audio generation started in background.");
      // Optionally disable button while running? Might need websockets or polling for status.
      // For now, just show the initial message.
    } catch (err) {
      console.error("Error triggering bulk audio generation:", err);
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(`Failed to start bulk audio generation: ${message}`);
      setBulkAudioStatus(null);
    }
  };

  const handleSaveAndReturn = async () => {
    if (!generatedScript || !projectId) return;

    try {
      setIsSaving(true);
      await updateProjectScript(parseInt(projectId), generatedScript);
      navigate(`/projects/${projectId}`);
    } catch (error) {
      console.error('Error saving script:', error);
      setError('Failed to save script. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };


  const handleSectionClick = (sectionId: string) => {
    setActiveSectionId(activeSectionId === sectionId ? null : sectionId);
    setActiveSegmentId(null);
  };

  const handleSegmentClick = (segmentId: string) => {
    setActiveSegmentId(activeSegmentId === segmentId ? null : segmentId);
  };

  const handleEditSegment = (segmentId: string) => {
    console.log('Editing segment with ID:', segmentId);

    if (!generatedScript) {
      console.error('No script available');
      return;
    }

    // Find the segment in the script
    let foundSegment: ScriptSegment | null = null;
    let sectionWithSegment: ScriptSection | null = null;

    for (const section of generatedScript.sections) {
      const segment = section.segments.find(seg => seg.id === segmentId);
      if (segment) {
        foundSegment = segment;
        sectionWithSegment = section;
        break;
      }
    }

    if (foundSegment) {
      console.log('Found segment to edit:', foundSegment);
      console.log('Segment narration text:', foundSegment.narrationText);
      console.log('In section:', sectionWithSegment?.title);
    } else {
      console.error('Segment not found with ID:', segmentId);
    }

    setActiveSegmentId(segmentId);
    setShowSegmentEditor(true);
  };

  const handleSaveSegment = (updatedSegment: ScriptSegment) => {
    if (!generatedScript) return;

    const updatedScript = { ...generatedScript };

    // Find the section containing the segment
    const sectionIndex = updatedScript.sections.findIndex(section =>
      section.segments.some(segment => segment.id === updatedSegment.id)
    );

    if (sectionIndex === -1) return;

    // Find the segment index
    const segmentIndex = updatedScript.sections[sectionIndex].segments.findIndex(
      segment => segment.id === updatedSegment.id
    );

    if (segmentIndex === -1) return;

    // Update the segment
    updatedScript.sections[sectionIndex].segments[segmentIndex] = updatedSegment;

    // Recalculate section duration
    updatedScript.sections[sectionIndex].totalDuration = updatedScript.sections[sectionIndex].segments.reduce(
      (total, segment) => total + segment.duration, 0
    );

    // Recalculate total script duration
    updatedScript.totalDuration = updatedScript.sections.reduce(
      (total, section) => total + section.totalDuration, 0
    );

    // Update local state first for immediate UI feedback
    setGeneratedScript(updatedScript);
    setShowSegmentEditor(false);

    // Now, persist the entire updated script to the backend
    if (projectId) {
      saveScriptToProject(updatedScript).catch(err => {
        // Handle potential save errors if needed, e.g., show an error message
        console.error("Error saving script after segment update:", err);
        setError("Failed to save segment changes to the server. Please try saving the entire script again.");
        // Optionally, revert local state or prompt user
      });
    }
  };

  const handleRegenerateSection = (sectionId: string) => {
    setActiveSectionId(sectionId);
    setShowSectionRegenerator(true);
  };

  const handleRegenerateSectionSubmit = (sectionId: string, prompt: string) => {
    // This would call the API to regenerate the section
    console.log(`Regenerating section ${sectionId} with prompt: ${prompt}`);
    setShowSectionRegenerator(false);
  };

  const getActiveSection = () => {
    if (!generatedScript || !activeSectionId) return null;
    return generatedScript.sections.find(section => section.id === activeSectionId) || null;
  };

  const getActiveSegment = () => {
    console.log('Getting active segment, ID:', activeSegmentId);

    if (!generatedScript) {
      console.log('No script available');
      return null;
    }

    if (!activeSegmentId) {
      console.log('No active segment ID');
      return null;
    }

    console.log('Searching for segment in sections:', generatedScript.sections.length);

    for (const section of generatedScript.sections) {
      console.log(`Checking section ${section.id} with ${section.segments.length} segments`);

      const segment = section.segments.find(segment => segment.id === activeSegmentId);

      if (segment) {
        console.log('Found segment:', segment);
        console.log('Segment narration text:', segment.narrationText);
        return segment;
      }
    }

    console.log('Segment not found');
    return null;
  };

  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Layout>
      {/* Show error message if there is one */}
      {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-md mb-4">
          {error}
        </div>
      )}

      {/* Show loading indicator */}
      {isLoading && (
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
      )}
      <div className="max-w-7xl mx-auto">
        {!generatedScript ? (
          <div className="bg-card shadow rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-bold text-foreground mb-2">
                {projectId ? 'Generate Script for Project' : 'Create Video Script'}
              </h1>
              {projectId && (
                <p className="text-muted-foreground mb-6">
                  Generate a script for your project based on the information below.
                  You can edit the script after generation.
                </p>
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

                <div className="pt-4">
                  <button
                    type="submit"
                    disabled={isGenerating || !topic}
                    className="w-full md:w-auto px-6 py-3 bg-primary text-primary-foreground rounded-md font-medium shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGenerating ? (
                      <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Generating Script...
                      </div>
                    ) : (
                      'Generate Script'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h1 className="text-2xl font-bold text-foreground">{generatedScript.title}</h1>
                    <p className="text-muted-foreground mt-1">{generatedScript.description}</p>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setShowScriptVisualizer(true)}
                      className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                    >
                      Preview
                    </button>
                    <button
                      onClick={() => setGeneratedScript(null)}
                      className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                    >
                      Create New Script
                    </button>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-2">
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Audience: {generatedScript.targetAudience}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Duration: {formatTime(generatedScript.totalDuration)}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Sections: {generatedScript.sections.length}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Status: {generatedScript.status.replace('_', ' ')}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <h2 className="text-xl font-semibold text-foreground mb-4">Script Sections</h2>

                <div className="space-y-4">
                  {generatedScript.sections.map((section) => (
                    <div key={section.id} className="border border-border rounded-lg overflow-hidden">
                      <div
                        className={`px-4 py-3 flex justify-between items-center cursor-pointer ${
                          activeSectionId === section.id ? 'bg-accent/50' : 'bg-card'
                        }`}
                        onClick={() => handleSectionClick(section.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-medium text-foreground">{section.title}</span>
                          <span className="ml-2 text-sm text-muted-foreground">({formatTime(section.totalDuration)})</span>
                        </div>
                        <svg
                          className={`h-5 w-5 text-muted-foreground transition-transform ${
                            activeSectionId === section.id ? 'transform rotate-180' : ''
                          }`}
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>

                      {activeSectionId === section.id && (
                        <div className="px-4 py-3 border-t border-border">
                          <div className="prose prose-sm max-w-none text-foreground">
                            <h4 className="text-sm font-medium text-muted-foreground mb-2">Overview</h4>
                            <div className="p-3 bg-muted/30 rounded-md mb-4">
                              <p>{section.content}</p>
                            </div>

                            {/* Section timeline */}
                            <SegmentTimeline
                              section={section}
                              onSegmentSelect={handleSegmentClick}
                              selectedSegmentId={activeSegmentId}
                            />

                            {/* Segments */}
                            <h4 className="text-sm font-medium text-muted-foreground mt-4 mb-2">Segments</h4>
                            <div className="space-y-3">
                              {section.segments.map((segment) => {
                                console.log('Rendering segment:', segment);
                                console.log('Segment narration text:', segment.narrationText);
                                return (
                                <div
                                  key={segment.id}
                                  className={`p-3 border rounded-md ${
                                    activeSegmentId === segment.id ? 'border-primary bg-primary/5' : 'border-border'
                                  }`}
                                  onClick={() => handleSegmentClick(segment.id)}
                                >
                                  <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-foreground">
                                        {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
                                      </span>
                                      <span className="ml-2 text-xs text-muted-foreground">
                                        ({segment.duration}s)
                                      </span>
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                      {segment.visuals.length} visual{segment.visuals.length !== 1 ? 's' : ''}
                                    </div>
                                  </div>

                                  <p className="text-sm text-foreground mb-2">
                                    {segment.narrationText ? segment.narrationText : 'No narration text available'}
                                  </p>
                                  {!segment.narrationText && (
                                    <div className="text-xs text-destructive mb-2">
                                      Warning: Narration text is missing for this segment
                                    </div>
                                  )}

                                  {activeSegmentId === segment.id && (
                                    <div className="mt-3">
                                      <h5 className="text-xs font-medium text-muted-foreground mb-2">Visuals</h5>
                                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                                        {segment.visuals.map((visual) => (
                                          <div key={visual.id} className="p-2 border border-border rounded-md bg-muted/10">
                                            <div className="text-xs text-muted-foreground mb-1">
                                              {formatTime(segment.startTime + visual.timestamp)} ({visual.duration}s)
                                            </div>
                                            <p className="text-xs text-foreground">{visual.description}</p>
                                          </div>
                                        ))}
                                      </div>

                                      <div className="flex justify-end mt-3 space-x-2">
                                        <button
                                          onClick={(e) => {
                                            e.stopPropagation(); // Prevent event from bubbling up to parent
                                            handleEditSegment(segment.id);
                                          }}
                                          className="px-3 py-1 bg-secondary text-secondary-foreground text-xs rounded-md hover:bg-secondary/90"
                                        >
                                          Edit Segment
                                        </button>
                                      </div>
                                    </div>
                                  )}
                                </div>
                              );
                              })}
                            </div>

                            <div className="mt-4 flex justify-end space-x-3">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation(); // Prevent event from bubbling up to parent
                                  handleRegenerateSection(section.id);
                                }}
                                className="px-3 py-1.5 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90"
                              >
                                Regenerate Section
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex justify-between">
                  <button
                    className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                    onClick={handleSubmit}
                  >
                    Regenerate Script
                  </button>

                  <div className="space-x-3">
                     {/* Button to generate all audios */}
                     {projectId && (
                       <button
                        className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                        onClick={handleGenerateAllAudios}
                        disabled={isSaving || isGenerating} // Disable if other actions are running
                        title="Generate audio narration for all segments"
                      >
                        Generate All Audios
                      </button>
                     )}
                     {/* Button to generate all images */}
                     {projectId && (
                       <button
                        className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                        onClick={handleGenerateAllImages}
                        disabled={isSaving || isGenerating} // Disable if other actions are running
                        title="Generate images for all visuals"
                      >
                        Generate All Images
                      </button>
                     )}
                     {/* Button to organize all visuals */}
                     {projectId && (
                       <button
                        className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                        onClick={handleOrganizeAllVisuals}
                        disabled={isSaving || isGenerating} // Disable if other actions are running
                        title="Organize timing for all visuals in all segments"
                      >
                        Organize All Visuals
                      </button>
                     )}
                    {projectId && (
                      <button
                        className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50"
                        onClick={handleSaveAndReturn}
                        disabled={isSaving}
                      >
                        {isSaving ? 'Saving...' : 'Save & Return to Project'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Segment Editor Modal */}
      {showSegmentEditor && getActiveSegment() && (
        <SegmentEditor
          segment={getActiveSegment()!}
          projectId={projectId ? parseInt(projectId) : 0}
          onSave={handleSaveSegment}
          onCancel={() => setShowSegmentEditor(false)}
        />
      )}

      {/* Section Regenerator Modal */}
      {showSectionRegenerator && getActiveSection() && (
        <SectionRegenerator
          section={getActiveSection()!}
          onRegenerate={handleRegenerateSectionSubmit}
          onCancel={() => setShowSectionRegenerator(false)}
        />
      )}

      {/* Script Visualizer Modal */}
      {showScriptVisualizer && generatedScript && (
        <ScriptVisualizer
          script={generatedScript}
          onClose={() => setShowScriptVisualizer(false)}
        />
      )}
    </Layout>
  );
}
