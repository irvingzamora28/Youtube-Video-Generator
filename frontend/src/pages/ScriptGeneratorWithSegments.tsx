import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { Script, ScriptSegment, ScriptSection } from '../types/script';
import SegmentEditor from '../components/SegmentEditor';
import SectionRegenerator from '../components/SectionRegenerator';
import ScriptVisualizer from '../components/ScriptVisualizer';
import SegmentTimeline from '../components/SegmentTimeline';
// Import the new API functions
import { generateAllProjectAudio, organizeSegmentVisuals, generateAllProjectImages, organizeAllProjectVisuals, generateVisualsForSegment, saveImageAsset, generateScript } from '../services/api';
import { getProjectContent, updateProjectScript, getProjectFullScript, getProject } from '../services/projectApi';

export default function ScriptGenerator() {
  const { id: projectId } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [duration, setDuration] = useState('5');
  const [style, setStyle] = useState('educational');
  const [visualStyle, setVisualStyle] = useState('stick-man');
  const [inspiration, setInspiration] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedScript, setGeneratedScript] = useState<Script | null>(null);
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null);
  const [activeSegmentId, setActiveSegmentId] = useState<string | null>(null);
  const [showSegmentEditor, setShowSegmentEditor] = useState(false);
  const [showSectionRegenerator, setShowSectionRegenerator] = useState(false);
  const [showScriptVisualizer, setShowScriptVisualizer] = useState(false);
  const [showScriptTextModal, setShowScriptTextModal] = useState(false);
  const [scriptText, setScriptText] = useState<string | null>(null);
  const [isScriptTextLoading, setIsScriptTextLoading] = useState(false);
  const [scriptTextError, setScriptTextError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isGeneratingVisuals, setIsGeneratingVisuals] = useState(false);
  const [generatingSectionId, setGeneratingSectionId] = useState<string | null>(null);
  const [bulkAudioStatus, setBulkAudioStatus] = useState<string | null>(null);
  const [bulkImageStatus, setBulkImageStatus] = useState<string | null>(null);
  const [bulkOrganizeStatus, setBulkOrganizeStatus] = useState<string | null>(null); // For bulk organize status

    // Build a map from segment id to global index (global segment number)
    let segmentGlobalIndexMap: Record<string, number> = {};
    if (generatedScript) {
      let counter = 1;
      generatedScript.sections.forEach(section => {
        section.segments.forEach(segment => {
          segmentGlobalIndexMap[segment.id] = counter++;
        });
      });
    }  

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
      const projectContent = await getProjectContent(id);

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

        setGeneratedScript(projectContent);
        setTopic(project.title || '');
        setAudience(project.targetAudience || 'general');
        setDuration(projectContent.totalDuration.toString() || '5');
        setVisualStyle(project.visualStyle || 'stick-man');
        setInspiration(project.inspiration || '');
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
      const script = await generateScript(topic, audience, durationMinutes, visualStyle, style, inspiration);
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

    // Handler for organizing all visuals in a section (segment by segment)
const handleOrganizeAllVisualsInSection = async (sectionId: string) => {
  if (!projectId || !generatedScript) return;
  setIsGeneratingVisuals(true);
  setGeneratingSectionId(sectionId);
  setError(null);
  let updatedScript = { ...generatedScript };
  try {
    // Find the section
    const sectionIdx = updatedScript.sections.findIndex(sec => sec.id === sectionId);
    if (sectionIdx === -1) throw new Error('Section not found');
    const section = updatedScript.sections[sectionIdx];
    for (let segIdx = 0; segIdx < section.segments.length; segIdx++) {
      const segment = section.segments[segIdx];
      try {
        // Organize visuals for this segment
        const result = await organizeSegmentVisuals({
          segment,
          projectId,
          sectionId,
        });
        if (result.organized_segment) {
          section.segments[segIdx] = { ...result.organized_segment };
        }
      } catch (segmentError) {
        console.error(`Error organizing visuals for segment ${segment.id}:`, segmentError);
        // Optionally, set an error field on the segment or notify the user
      }
    }
    // After all segments, update section in script
    updatedScript.sections[sectionIdx] = { ...section };
    setGeneratedScript(updatedScript);
    setBulkOrganizeStatus('All visuals organized for this section.');
  } catch (err) {
    console.error('Error organizing visuals for section:', err);
    const message = err instanceof Error ? err.message : 'Unknown error';
    setError(`Failed to organize visuals for section: ${message}`);
    setBulkOrganizeStatus(null);
  } finally {
    setIsGeneratingVisuals(false);
    setGeneratingSectionId(null);
  }
};

// Handler for generating all visuals in a section
const handleGenerateAllVisuals = async (sectionId: string) => {
  if (!projectId || !generatedScript) return;
  setIsGeneratingVisuals(true);
  setGeneratingSectionId(sectionId);
  setError(null);
  let updatedScript = { ...generatedScript };
  try {
    // Find the section
    const sectionIdx = updatedScript.sections.findIndex(sec => sec.id === sectionId);
    if (sectionIdx === -1) throw new Error('Section not found');
    const section = updatedScript.sections[sectionIdx];
    // Iterate through each segment
    for (let segIdx = 0; segIdx < section.segments.length; segIdx++) {
      const segment = section.segments[segIdx];

      try {
        const result = await generateVisualsForSegment({
          projectId: Number(projectId),
          segmentId: segment.id,
          narrationText: segment.narrationText,
        }); // (no change, just context)
        if (result && Array.isArray(result.visuals)) {
          segment.visuals = result.visuals.map((v: any) => ({
            ...v,
            imageUrl: v.imageUrl,
          }));
        } else {
          console.error(`Unexpected response from server for segment ${segment.id}, narration text: ${segment.narrationText}`);
          console.log(result);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error(`Error generating visuals for segment ${segment.id}, narration text: ${segment.narrationText}:`, errorMessage);
      }
      // After all visuals in segment, update segment in section
      section.segments[segIdx] = { ...segment };
    }
    // After all segments, update section in script
    updatedScript.sections[sectionIdx] = { ...section };
    setGeneratedScript(updatedScript);
    setBulkImageStatus('All visuals generated and saved for this section.');
  } catch (err) {
    console.error('Error generating visuals for section:', err);
    const message = err instanceof Error ? err.message : 'Unknown error';
    setError(`Failed to generate visuals for section: ${message}`);
    setBulkImageStatus(null);
  } finally {
    setIsGeneratingVisuals(false);
    setGeneratingSectionId(null);
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

  const handleRegenerateSectionSubmit = (sectionId: string, regeneratedSection: ScriptSection) => {
    // Update the relevant section in generatedScript
    if (!generatedScript) return;
    const updatedSections = generatedScript.sections.map(section =>
      section.id === sectionId ? regeneratedSection : section
    );
    setGeneratedScript({ ...generatedScript, sections: updatedSections });
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

  // Helper function to determine segment border color based on visuals' referenceFound property
  function getSegmentBorderColor(segment: ScriptSegment) {
    if (!Array.isArray(segment.visuals) || segment.visuals.length === 0) {
      return 'border-border';
    }
    // If any visual does not have referenceFound property, keep default
    if (segment.visuals.some(v => typeof v.referenceFound === 'undefined')) {
      return 'border-border';
    }
    // If all visuals have referenceFound true
    if (segment.visuals.every(v => v.referenceFound === true)) {
      return 'border-success';
    }
    // If at least one visual has referenceFound false (and all have the property)
    if (segment.visuals.some(v => v.referenceFound === false)) {
      return 'border-error';
    }
    // Fallback
    return 'border-border';
  }

  return (
    <Layout>
      {/* Show error message if there is one */}
      {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-md mb-4">
          {error}
        </div>
      )}

     
      <div className="max-w-7xl mx-auto">
        {!generatedScript || isLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
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
                      className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 disabled:opacity-50"
                      onClick={async () => {
                        if (!projectId) return;
                        setShowScriptTextModal(true);
                        setIsScriptTextLoading(true);
                        setScriptTextError(null);
                        try {
                          const text = await getProjectFullScript(parseInt(projectId));
                          setScriptText(text);
                        } catch (err) {
                          setScriptTextError(err instanceof Error ? err.message : 'Failed to load script text');
                        } finally {
                          setIsScriptTextLoading(false);
                        }
                      }}
                      disabled={!projectId}
                      title="Show only the script text"
                    >
                      View Script
                    </button>
                    <button
                      onClick={() => setShowScriptVisualizer(true)}
                      className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                    >
                      Preview
                    </button>
                    <button
                      className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                      onClick={() => navigate(`/projects/${projectId}/create-edit`)}
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
                          {
                            (() => {
                              if (!section.segments.length) return null;
                              const firstSegmentId = section.segments[0]?.id;
                              const lastSegmentId = section.segments[section.segments.length - 1]?.id;
                              const firstIndex = segmentGlobalIndexMap[firstSegmentId];
                              const lastIndex = segmentGlobalIndexMap[lastSegmentId];
                              if (firstIndex && lastIndex) {
                                return (
                                  <span className="ml-2 text-md text-muted-foreground">(segments {firstIndex}-{lastIndex})</span>
                                );
                              }
                              return null;
                            })()
                          }
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
                                  className={`p-3 border rounded-md ${getSegmentBorderColor(segment)} ${activeSegmentId === segment.id ? 'bg-primary/5' : ''}`}

                                  onClick={() => handleSegmentClick(segment.id)}
                                >
                                  <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-foreground">
                                        Segment # {segmentGlobalIndexMap[segment.id]}
                                      </span>
                                      <span className="ml-2 text-sm font-medium text-foreground">
                                        {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
                                      </span>
                                      <span className="ml-2 text-xs text-muted-foreground">
                                        ({segment.duration}s)
                                      </span>
                                      <span className="ml-2 text-sm text-neutral-800">
                                        Segment ID: {segment.id}
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
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleGenerateAllVisuals(section.id);
                                }}
                                className="px-3 py-1.5 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90 disabled:opacity-50"
                                disabled={isGeneratingVisuals && generatingSectionId === section.id}
                              >
                                Generate All Visuals
                              </button>
                              {/* Button to organize all visuals in section (segment by segment) */}
                              {activeSectionId && (
                                <button
                                  className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                                  onClick={() => handleOrganizeAllVisualsInSection(activeSectionId)}
                                  disabled={isSaving || isGeneratingVisuals}
                                  title="Organize visuals for all segments in this section"
                                >
                                  {isGeneratingVisuals && generatingSectionId === activeSectionId ? 'Organizing...' : 'Organize All Visuals'}
                                </button>
                              )}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex justify-between">
                  <button
                    className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                    disabled={isSaving || isGenerating || isGeneratingVisuals}
                    onClick={handleSubmit}
                  >
                    {isGenerating ? 'Generating...' : 'Regenerate Script'}
                  </button>

                  <div className="space-x-3 flex items-center">
                     {/* Button to generate all audios */}
                     {projectId && (
                       <button
                        className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90 disabled:opacity-50"
                        onClick={handleGenerateAllAudios}
                        disabled={isSaving || isGenerating || isGeneratingVisuals} // Disable if other actions are running
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
                        disabled={isSaving || isGenerating || isGeneratingVisuals} // Disable if other actions are running
                        title="Generate images for all visuals"
                      >
                        {isGeneratingVisuals ? 'Generating...' : 'Generate All Images'}
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
          projectId={projectId || ''}
          sectionId={(() => {
            // Find the section containing the active segment
            const seg = getActiveSegment();
            console.log('|||||||||||||||||||||||||||||| Active segment:', seg);
            console.log('|||||||||||||||||||||||||||||| Generated script:', generatedScript);
            
            if (!seg || !generatedScript) return '';
            const section = generatedScript.sections.find(sec => sec.segments.some(s => s.id === seg.id));
            console.log('|||||||||||||||||||||||||||||| Section found:', section);
            return section ? section.id : '';
          })()}
          onSave={handleSaveSegment}
          onCancel={() => setShowSegmentEditor(false)}
        />
      )}

      {/* Section Regenerator Modal */}
      {showSectionRegenerator && getActiveSection() && (
        <SectionRegenerator
          section={getActiveSection()!}
          sections={generatedScript ? generatedScript.sections : []}
          inspiration={''}
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

      {/* Script Text Modal */}
      {showScriptTextModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 ">
          <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full p-6 relative">
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-lg"
              onClick={() => setShowScriptTextModal(false)}
              aria-label="Close"
            >
              &times;
            </button>
            <h2 className="text-lg font-semibold mb-4">Full Script Text</h2>
            {isScriptTextLoading ? (
              <div className="text-center py-6">Loading...</div>
            ) : scriptTextError ? (
              <div className="text-red-600">{scriptTextError}</div>
            ) : (
              <pre className="whitespace-pre-wrap break-words max-h-96 overflow-y-auto bg-gray-100 p-4 rounded text-sm">{scriptText}</pre>
            )}
          </div>
        </div>
      )}
    </Layout>
  );
}

