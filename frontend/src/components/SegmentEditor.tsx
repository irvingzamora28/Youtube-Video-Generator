import { useState, useRef, useEffect } from 'react';
import { ScriptSegment, Visual } from '../types/script';
// Import new API functions
import { generateImageForVisual, saveImageAsset, generateSegmentAudio, organizeSegmentVisuals, generateImageDescription, previewBackgroundRemoval, generateVisualsForSegment } from '../services/api';

type SegmentEditorProps = {
  segment: ScriptSegment;
  projectId: string;
  sectionId: string;
  onSave: (updatedSegment: ScriptSegment) => void;
  onCancel: () => void;
};

import { getProjectAssets } from '../services/projectApi';

export default function SegmentEditor({ segment, projectId, sectionId, onSave, onCancel }: SegmentEditorProps) {
  // State for generating all visuals
  const [isGeneratingAllVisuals, setIsGeneratingAllVisuals] = useState(false);
  const [generateAllVisualsError, setGenerateAllVisualsError] = useState<string | null>(null);

  console.log('SegmentEditor received segment:', segment);
  console.log('Project ID:', projectId);
  console.log('Section ID:', sectionId);
  
  console.log('Segment narration text:', segment.narrationText);

  const [narrationText, setNarrationText] = useState(segment.narrationText || '');
  const [startTime, setStartTime] = useState(segment.startTime);
  const [duration, setDuration] = useState(segment.duration);
  // Utility to ensure imageUrl always starts with /static/ if not empty
  const normalizeImageUrl = (path?: string) => path && path !== '' && !path.startsWith('/static/') ? `/static/${path}` : path || '';

  // Initialize visuals from segment, normalizing imageUrl
  const [visuals, setVisuals] = useState<Visual[]>(
    segment.visuals.map(v => ({
      ...v,
      imageUrl: normalizeImageUrl(v.imageUrl),
    }))
  );

  // Handler for "Generate All Visuals"
  const handleGenerateAllVisuals = async () => {
    setIsGeneratingAllVisuals(true);
    setGenerateAllVisualsError(null);
    try {
      const result = await generateVisualsForSegment({
        projectId: Number(projectId),
        segmentId: segment.id,
        narrationText: narrationText,
      }); // (no change, just context)
      if (result && Array.isArray(result.visuals)) {
        setVisuals(result.visuals.map((v: any) => ({
          ...v,
          imageUrl: normalizeImageUrl(v.imageUrl),
        })));
      } else {
        setGenerateAllVisualsError('Unexpected response from server.');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      setGenerateAllVisualsError(errorMessage);
    } finally {
      setIsGeneratingAllVisuals(false);
    }
  };


  const [activeVisualIndex, setActiveVisualIndex] = useState<number | null>(null);

  // Helper: Preview background removal for active visual
  const handlePreviewBgRemoval = async () => {
    if (activeVisualIndex === null) return;
    const visual = visuals[activeVisualIndex];
    if (!visual.imageUrl || !visual.removeBackground) return;
    setIsPreviewingBgRemoval(true);
    setGenerationError(null);
    try {
      const base64 = await previewBackgroundRemoval({
        imageUrl: visual.imageUrl,
        removeBackgroundMethod: visual.removeBackgroundMethod || 'color',
        projectId,
        // Optionally add backgroundUrl here if you want project background
      });
      setBgRemovalPreview(base64);
    } catch (err) {
      setGenerationError(err instanceof Error ? err.message : String(err));
      setBgRemovalPreview(null);
    } finally {
      setIsPreviewingBgRemoval(false);
    }
  };

  // Helper: Change method and auto-preview if valid
  const handleBgMethodChange = (method: 'color' | 'rembg') => {
    if (activeVisualIndex === null) return;
    const updatedVisuals = visuals.map((v, i) =>
      i === activeVisualIndex ? { ...v, removeBackgroundMethod: method } : v
    );
    setVisuals(updatedVisuals);
  };

  // Optionally: Clear preview if imageUrl or removeBackground changes
  useEffect(() => {
    if (activeVisualIndex === null) return;
    setBgRemovalPreview(null);
    setGenerationError(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeVisualIndex, activeVisualIndex !== null ? visuals[activeVisualIndex]?.imageUrl : undefined, activeVisualIndex !== null ? visuals[activeVisualIndex]?.removeBackground : undefined]);

  const [selectedTextRange, setSelectedTextRange] = useState<{start: number, end: number} | null>(null);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
const [isGeneratingImageDescription, setIsGeneratingImageDescription] = useState(false);
const [isPreviewingBgRemoval, setIsPreviewingBgRemoval] = useState(false);
const [bgRemovalPreview, setBgRemovalPreview] = useState<string | null>(null);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [isOrganizingVisuals, setIsOrganizingVisuals] = useState(false); // State for organizing visuals
  const [generationError, setGenerationError] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // Initialize audioUrl state from segment prop
  useEffect(() => {
    setAudioUrl(segment.audioUrl ? normalizeImageUrl(segment.audioUrl) : null);
  }, [segment.audioUrl]); // Depend on audioUrl from prop

  // Print all assets for this project on mount for debugging
  useEffect(() => {
    getProjectAssets(Number(projectId), 'image').then(assets => {
      console.log('All image assets for this project:', assets);
    }).catch(err => {
      console.error('Error fetching project assets:', err);
    });
  }, [projectId]);

  // Effect to re-sync internal state if the segment prop changes
  useEffect(() => {
    console.log("[SegmentEditor] Segment prop changed, re-initializing state.");
    setNarrationText(segment.narrationText || '');
    setStartTime(segment.startTime);
    setDuration(segment.duration);
    setVisuals(
      segment.visuals.map(v => ({
        ...v,
        imageUrl: normalizeImageUrl(v.imageUrl), // Re-normalize on prop change
      }))
    );
    // Optionally reset active index if desired when the whole segment changes
    // setActiveVisualIndex(null);
    // Also update audioUrl state when segment prop changes
    setAudioUrl(segment.audioUrl ? normalizeImageUrl(segment.audioUrl) : null);
  }, [segment]); // Re-run this effect if the segment object reference changes

  // Effect to focus the textarea when the component mounts
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();

      // Optional: Place cursor at the end of the text
      const textLength = textareaRef.current.value.length;
      textareaRef.current.setSelectionRange(textLength, textLength);
    }

    // Add event listener for the Escape key
    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onCancel();
      }
    };

    document.addEventListener('keydown', handleEscapeKey);

    // Clean up the event listener when the component unmounts
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, []); // Empty dependency array means this runs once on mount

  // Effect to highlight text when a visual is selected
  useEffect(() => {
    if (activeVisualIndex !== null && textareaRef.current) {
      const visual = visuals[activeVisualIndex];
      const visualTimestamp = visual.timestamp;
      const visualEndTime = visualTimestamp + visual.duration;

      // Estimate character positions based on timing
      // This is a simple approximation - in a real app, you'd need more sophisticated mapping
      const charsPerSecond = narrationText.length / duration;
      const startChar = Math.floor(visualTimestamp * charsPerSecond);
      const endChar = Math.min(Math.floor(visualEndTime * charsPerSecond), narrationText.length);

      setSelectedTextRange({ start: startChar, end: endChar });
    } else {
      setSelectedTextRange(null);
    }
  }, [activeVisualIndex, visuals, narrationText, duration]);

  const handleAddVisual = () => {
    // Get selected text from textarea if any
    let description = '';
    let visualTimestamp = 0;
    let visualDuration = Math.min(5, segment.duration);

    if (textareaRef.current) {
      const textarea = textareaRef.current;
      const selectionStart = textarea.selectionStart;
      const selectionEnd = textarea.selectionEnd;

      if (selectionStart !== selectionEnd) {
        // User has selected text, use it for the visual description
        description = narrationText.substring(selectionStart, selectionEnd);

        // Estimate timing based on text position
        const charsPerSecond = narrationText.length / duration;
        visualTimestamp = selectionStart / charsPerSecond;
        visualDuration = Math.min((selectionEnd - selectionStart) / charsPerSecond, segment.duration - visualTimestamp);
      }
    }

    const newVisual: Visual = {
      id: `visual-${Date.now()}`,
      description: description || 'New visual',
      timestamp: visualTimestamp,
      duration: visualDuration,
      visualType: 'image',
      position: 'center',
      transition: 'fade',
      removeBackground: false, // Ensure initialized
      removeBackgroundMethod: 'color', // Default method
    };

    setVisuals([...visuals, newVisual]);
    setActiveVisualIndex(visuals.length);
  };

  const handleUpdateVisual = (index: number, field: keyof Visual, value: any) => {
    const updatedVisuals = [...visuals];
    updatedVisuals[index] = {
      ...updatedVisuals[index],
      [field]: value,
    };
    setVisuals(updatedVisuals);
  };

  // Function to handle visual organization
  const handleOrganizeVisuals = async () => {
    setIsOrganizingVisuals(true);
    setGenerationError(null);
    try {
      // Construct the current segment state to send
      const currentSegmentState: ScriptSegment = {
        ...segment, // Base props
        narrationText,
        startTime,
        duration,
        visuals: visuals.map(v => ({ // Send current visuals state
            ...v,
            // Remove /static/ prefix before sending if it exists
            imageUrl: v.imageUrl?.startsWith('/static/') ? v.imageUrl.substring(8) : v.imageUrl
        })),
        audioUrl: audioUrl ? audioUrl.replace('/static/', '') : undefined,
        // Include audioAssetId if you track it in state
      };
      console.log("Sending segment data for visual organization:", currentSegmentState);
      console.log("Sending projectId and sectionId:", projectId, sectionId);
      
      // Pass projectId and sectionId explicitly to the API
      const result = await organizeSegmentVisuals({
        segment: currentSegmentState,
        projectId,
        sectionId,
      });

      if (result.organized_segment && result.organized_segment.visuals) {
        console.log("Received organized visuals:", result.organized_segment.visuals);
        // Update the visuals state with the reorganized ones
        setVisuals(
          result.organized_segment.visuals.map(v => ({
            ...v,
            imageUrl: normalizeImageUrl(v.imageUrl), // Re-normalize URLs
            removeBackground: !!v.removeBackground // Ensure all visuals have removeBackground
          }))
        );
        // Update duration if it was changed by the LLM (though prompt asks not to)
        if (result.organized_segment.duration !== duration) {
             console.log(`Segment duration updated by LLM from ${duration} to ${result.organized_segment.duration}`);
             setDuration(result.organized_segment.duration);
        }
      } else {
        throw new Error("Backend did not return organized visuals.");
      }
    } catch (error) {
      console.error('Error organizing visuals:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setGenerationError(`Failed to organize visuals: ${errorMessage}`);
    } finally {
      setIsOrganizingVisuals(false);
    }
  };

  // Function to handle audio generation
  const handleGenerateAudio = async () => {
    setIsGeneratingAudio(true);
    setGenerationError(null);
    try {
      console.log(`Generating audio for segment: ${segment.id}, project: ${projectId}`);
      const result = await generateSegmentAudio({
        projectId: Number(projectId),
        segmentId: segment.id,
      });

      console.log("Audio generation result:", result);

      if (result.success && result.asset?.path && result.updated_segment) {
        const normalizedPath = normalizeImageUrl(result.asset.path);
        const newDuration = result.updated_segment.duration; // Get duration from response

        setAudioUrl(normalizedPath); // Update state for preview

        // Update the duration state if it changed
        if (newDuration && newDuration !== duration) {
          console.log(`Updating segment duration from ${duration} to ${newDuration}`);
          setDuration(newDuration);
        }

        // We also need to store the audioAssetId if we want to pass it up on save
        // For now, just logging it. Add state if needed later.
        console.log(`Audio generated successfully: ${normalizedPath}, Asset ID: ${result.updated_segment.audioAssetId}, Duration: ${newDuration}`);

      } else {
        throw new Error(result.error || "Audio generation failed or backend did not return expected data.");
      }
    } catch (error) {
      console.error('Error generating audio:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setGenerationError(`Failed to generate audio: ${errorMessage}`);
      setAudioUrl(null); // Clear URL on error
    } finally {
      setIsGeneratingAudio(false);
    }
  };


  const handleGenerateImage = async () => {
    if (activeVisualIndex === null) return;

    const visual = visuals[activeVisualIndex];

    // Check if we have a description
    if (!visual.description.trim()) {
      setGenerationError('Please provide a description for the visual');
      return;
    }

    setIsGeneratingImage(true);
    setGenerationError(null);

    try {
      // Generate the image (base64 or URL)
      const imageData = await generateImageForVisual(visual);

      // Persist the image and metadata to backend
      const saveResult = await saveImageAsset({
        projectId: Number(projectId),
        segmentId: segment.id,
        visualId: visual.id,
        timestamp: visual.timestamp,
        duration: visual.duration,
        imageData,
        description: visual.description,
      });

      // Use the updated segment data returned from the backend
      if (saveResult?.updated_segment) {
        console.log("Received updated segment from backend:", saveResult.updated_segment);
        // Find the specific visual within the updated segment data
        const updatedVisual = saveResult.updated_segment.visuals.find(
          (v: Visual) => v.id === visual.id
        );
        if (updatedVisual && activeVisualIndex !== null) { // Ensure activeVisualIndex is not null
          console.log("Found updated visual in segment data:", updatedVisual);
          // Update the entire visual object in the local state at once
          const newVisuals = [...visuals];
          newVisuals[activeVisualIndex] = {
            ...newVisuals[activeVisualIndex], // Keep existing properties not returned by backend if any
            ...updatedVisual, // Spread the updated properties from backend response
            imageUrl: normalizeImageUrl(updatedVisual.imageUrl), // Ensure normalization after spreading
            removeBackground: !!updatedVisual.removeBackground // Ensure all visuals have removeBackground
          };
          // Define the visualToUpdate object
          const visualToUpdate = newVisuals[activeVisualIndex];

          // Add detailed logging before state update
          console.log("[SegmentEditor] Visual object prepared for state update:", visualToUpdate);
          console.log("[SegmentEditor] Full visuals array prepared for state update:", JSON.stringify(newVisuals)); // Stringify for better inspection

          setVisuals(newVisuals); // Single state update
          console.log("[SegmentEditor] setVisuals called."); // Confirm setVisuals was called
        } else {
           console.error("Updated visual not found in returned segment data or activeVisualIndex is null.");
           setGenerationError('Image saved, but failed to update preview.');
        }
      } else if (saveResult?.error) {
         console.error("Error reported from backend during content update:", saveResult.error);
         setGenerationError(`Image saved, but failed to update project content: ${saveResult.error}`);
      }
       else {
        console.error("Backend did not return updated segment data.");
        setGenerationError('Failed to get updated data from backend after saving asset.');
      }
    } catch (error) {
      console.error('Error generating or saving image:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setGenerationError(`Failed to generate or save image: ${errorMessage}`);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  const handleRemoveVisual = (index: number) => {
    const updatedVisuals = visuals.filter((_, i) => i !== index);
    setVisuals(updatedVisuals);
    setActiveVisualIndex(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Include the potentially updated audioUrl when saving
    // Note: This relies on the audioUrl state. If the backend updated the segment
    // object directly, we'd need a different approach or ensure the parent refetches.
    // For now, we pass the current state including the potentially updated visuals array
    // and the audioUrl state. The parent `handleSaveSegment` needs to merge this correctly.
    const segmentToSave: ScriptSegment = {
      ...segment, // Start with original segment data
      narrationText,
      startTime,
      duration,
      visuals: visuals.map(v => ({
        ...v,
        removeBackground: !!v.removeBackground, // Always send boolean
        removeBackgroundMethod: v.removeBackgroundMethod || 'color', // Always send method
      })), // Ensure all visuals have removeBackground and method
      audioUrl: audioUrl ? audioUrl.replace('/static/', '') : undefined, // Pass updated audioUrl (remove /static/ prefix for saving)
      // audioAssetId might need to be updated here too if the API returns it and we store it
    };
    console.log("Saving segment data:", segmentToSave);
    onSave(segmentToSave);
  };

  // Format seconds to MM:SS format for display
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Handle clicks outside the modal
  const handleOutsideClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onCancel();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
      onClick={handleOutsideClick}
    >
      <div
        ref={modalRef}
        className="bg-card rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto border border-border"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-border">
          <h2 className="text-xl font-semibold text-foreground">Edit Segment</h2>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          <div className="space-y-6">
            <div>
              <label htmlFor="narrationText" className="block text-sm font-medium text-foreground mb-1">
                Narration Text
              </label>
              <div className="relative">
                <textarea
                  id="narrationText"
                  ref={textareaRef}
                  value={narrationText}
                  onChange={(e) => setNarrationText(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  required
                />
                {selectedTextRange && (
                  <div className="absolute top-0 left-0 right-0 pointer-events-none">
                    <div className="px-4 py-2">
                      <span className="invisible">{narrationText.substring(0, selectedTextRange.start)}</span>
                      <span className="bg-primary/20 text-transparent">
                        {narrationText.substring(selectedTextRange.start, selectedTextRange.end)}
                      </span>
                    </div>
                  </div>
                )}
                {/* Word Timings Chips */}
                {Array.isArray(segment.wordTimings) && segment.wordTimings.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {segment.wordTimings.map((wt: { word: string; start: number }, idx: number) => (
                      <span
                        key={idx}
                        className="inline-flex items-center px-2 py-1 rounded bg-muted text-xs font-mono text-foreground border border-border hover:bg-primary/10 cursor-pointer transition"
                        title={`Start: ${wt.start.toFixed(2)}s`}
                      >
                        {wt.word}
                        <span className="ml-1 text-muted-foreground text-[10px]">({wt.start.toFixed(2)}s)</span>
                      </span>
                    ))}
                  </div>
                )}
                <div className="mt-1 text-xs text-muted-foreground">
                  Select text to create a visual for that specific part of the narration.
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="startTime" className="block text-sm font-medium text-foreground mb-1">
                  Start Time ({formatTime(startTime)})
                </label>
                <input
                  type="range"
                  id="startTime"
                  value={startTime}
                  onChange={(e) => setStartTime(Number(e.target.value))}
                  min={0}
                  max={300}
                  step={0.5}
                  className="w-full"
                />
              </div>

              <div>
                <label htmlFor="duration" className="block text-sm font-medium text-foreground mb-1">
                  Duration ({formatTime(duration)})
                </label>
                <input
                  type="range"
                  id="duration"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  min={1}
                  max={60}
                  step={0.5}
                  className="w-full"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-md font-medium text-foreground">Visuals</h3>
                <div className="flex flex-wrap gap-2 items-center">
                  <div className="flex items-center gap-2">
                  <button
                    type="button"
                    className="px-2 py-1 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90 disabled:opacity-50 flex items-center"
                    onClick={handleGenerateAllVisuals}
                    disabled={isGeneratingAllVisuals}
                    title="Automatically generate visuals for this segment based on narration"
                  >
                    {isGeneratingAllVisuals ? 'Generating Visuals...' : 'Generate All Visuals'}
                  </button>
                  {generateAllVisualsError && (
                    <span className="text-xs text-red-600 ml-2">{generateAllVisualsError}</span>
                  )}  
                  </div>
                {/* Organize Visuals Button */}
                <button
                        type="button"
                        onClick={handleOrganizeVisuals}
                        disabled={isOrganizingVisuals || visuals.length < 2}
                        title={visuals.length < 2 ? "Need at least 2 visuals to organize" : "Automatically adjust visual timing"}
                        className="px-2 py-1 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90 disabled:opacity-50 flex items-center"
                      >
                        {isOrganizingVisuals ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-secondary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Organizing...
                          </>
                        ) : (
                          'Organize Visuals'
                        )}
                      </button>
                <button
                  type="button"
                  onClick={handleAddVisual}
                  className="px-2 py-1 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90"
                >
                  Add Visual
                </button>
              </div>
              </div>

              {/* Visual thumbnails */}
              <div className="flex flex-wrap gap-2 mb-4">
                {visuals
                  .slice()
                  .sort((a, b) => (a.timestamp ?? 0) - (b.timestamp ?? 0))
                  .map((visual, index) => (
                    <div
                      key={visual.id}
                    className={`relative p-2 border rounded-md cursor-pointer ${
                      activeVisualIndex === index
                        ? 'border-primary bg-primary/10'
                        : 'border-border'
                    }`}
                    onClick={() => setActiveVisualIndex(index)}
                  >
                    <div className="w-16 h-16 bg-muted/30 rounded flex items-center justify-center overflow-hidden">
                      {visual.imageUrl ? (
                        <img
                          src={visual.imageUrl}
                          alt={visual.altText || 'Visual'}
                          className="max-w-full max-h-full object-contain"
                        />
                      ) : (
                        <div className="text-muted-foreground text-xs text-center">
                          {visual.visualType}
                        </div>
                      )}
                    </div>
                    <div className="text-xs text-muted-foreground mt-1 text-center">
                      {formatTime(visual.timestamp)}
                    </div>
                  </div>
                ))}

                {visuals.length === 0 && (
                  <div className="w-full p-4 border border-dashed border-border rounded-md text-center text-muted-foreground">
                    No visuals added yet. Click "Add Visual" to create one.
                  </div>
                )}
              </div>

              {/* Active visual editor */}
              {activeVisualIndex !== null && (
                <div className="border border-border rounded-md p-4">
                  <div className="flex justify-between items-center mb-4">
                    <h4 className="text-sm font-medium text-foreground">
                      Edit Visual {activeVisualIndex + 1}
                    </h4>
                    <div className="flex flex-wrap gap-2 items-center">
                       {/* Generate Audio Button */}
                       <button
                        type="button"
                        onClick={handleGenerateAudio}
                        disabled={isGeneratingAudio || !narrationText.trim()}
                        title={!narrationText.trim() ? "Narration text is required to generate audio" : "Generate audio for this segment"}
                        className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded-md hover:bg-secondary/90 disabled:opacity-50 flex items-center"
                      >
                        {isGeneratingAudio ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-secondary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating Audio...
                          </>
                        ) : (
                          'Generate Audio'
                        )}
                      </button>
                      {/* Generate Image Button */}
                      <button
                        type="button"
                        onClick={handleGenerateImage}
                        disabled={isGeneratingImage || activeVisualIndex === null}
                        title={activeVisualIndex === null ? "Select a visual first" : "Generate image for the selected visual"}
                        className="px-2 py-1 bg-primary text-primary-foreground text-xs rounded-md hover:bg-primary/90 disabled:opacity-50 flex items-center"
                      >
                        {isGeneratingImage ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating...
                          </>
                        ) : (
                          'Generate Image'
                        )}
                      </button>
                      {/* Generate Image Description Button */}
                      <button
                        type="button"
                        onClick={async () => {
                          if (activeVisualIndex === null) return;
                          // Find the narration textarea and get selection
                          const textarea = textareaRef.current;
                          if (!textarea) return;
                          const selectionStart = textarea.selectionStart;
                          const selectionEnd = textarea.selectionEnd;
                          if (selectionStart === selectionEnd) {
                            window.alert('Please select the part of the narration you want the image to represent.');
                            return;
                          }
                          setIsGeneratingImageDescription(true);
                          setGenerationError(null);
                          try {
                            // Get the full script as a string (concatenate all segments)
                            // If you have the full script available as a prop, use that instead
                            let script = '';
                            if (segment.fullScript) {
                              script = segment.fullScript;
                            } else if (segment.script) {
                              script = segment.script;
                            } else {
                              script = narrationText; // fallback: just use current narration
                            }
                            const selectedText = narrationText.substring(selectionStart, selectionEnd);
                            const narration = narrationText;
                            const description = await generateImageDescription({
                              script,
                              narration,
                              selectedText,
                            });
                            setVisuals(prev => prev.map((v, i) => i === activeVisualIndex ? { ...v, description } : v));
                          } catch (err: any) {
                            setGenerationError(err.message || 'Failed to generate image description');
                          } finally {
                            setIsGeneratingImageDescription(false);
                          }
                        }}
                        disabled={isGeneratingImageDescription || activeVisualIndex === null}
                        title={activeVisualIndex === null ? "Select a visual first" : "Generate an improved image description for the selected narration text"}
                        className="px-2 py-1 bg-accent text-accent-foreground text-xs rounded-md hover:bg-accent/90 disabled:opacity-50 flex items-center"
                      >
                        {isGeneratingImageDescription ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-accent-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating Description...
                          </>
                        ) : (
                          'Generate Image Description'
                        )}
                      </button>
                      <button
                        type="button"
                        onClick={() => handleRemoveVisual(activeVisualIndex)}
                        className="text-destructive hover:text-destructive/90 text-sm"
                      >
                        Remove Visual
                      </button>
                    </div>
                  </div>

                  {/* Display Audio Player if URL exists */}
                  {audioUrl && (
                    <div className="my-4">
                       <label className="block text-sm font-medium text-foreground mb-1">
                          Segment Audio Preview
                        </label>
                      <audio controls src={audioUrl} className="w-full">
                        Your browser does not support the audio element.
                      </audio>
                    </div>
                  )}

                  {generationError && (
                    <div className="mb-4 p-2 bg-destructive/10 border border-destructive/20 rounded-md text-sm text-destructive">
                      {generationError}
                    </div>
                  )}


                  <div className="space-y-4">
                    {/* Preview the generated image */}
                    {visuals[activeVisualIndex].imageUrl && (
                      <div className="mb-4">
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Preview
                        </label>
                        <div className="border border-border rounded-md p-2 flex justify-center">
                          <img
                            src={visuals[activeVisualIndex].imageUrl}
                            alt={visuals[activeVisualIndex].altText || 'Generated visual'}
                            className="max-h-48 object-contain"
                          />
                        </div>
                      </div>
                    )}

                    <div>
                      <label className="block text-sm font-medium text-foreground mb-1">
                        Visual Description
                      </label>
                      <textarea
                        value={visuals[activeVisualIndex].description}
                        onChange={(e) => handleUpdateVisual(activeVisualIndex, 'description', e.target.value)}
                        rows={3}
                        className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        placeholder="Describe what should be shown in this visual..."
                        required
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Timestamp ({formatTime(visuals[activeVisualIndex].timestamp)})
                        </label>
                        <input
                          type="range"
                          value={visuals[activeVisualIndex].timestamp}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'timestamp', Number(e.target.value))}
                          min={0}
                          max={duration}
                          step={0.1}
                          className="w-full"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Duration ({formatTime(visuals[activeVisualIndex].duration)})
                        </label>
                        <input
                          type="range"
                          value={visuals[activeVisualIndex].duration}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'duration', Number(e.target.value))}
                          min={0.5}
                          max={Math.min(30, duration)}
                          step={0.5}
                          className="w-full"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Visual Type
                        </label>
                        <select
                          value={visuals[activeVisualIndex].visualType}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'visualType', e.target.value)}
                          className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                          <option value="image">Image</option>
                          <option value="animation">Animation</option>
                          <option value="diagram">Diagram</option>
                          <option value="text">Text Overlay</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Position
                        </label>
                        <select
                          value={visuals[activeVisualIndex].position}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'position', e.target.value)}
                          className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                          <option value="center">Center</option>
                          <option value="left">Left</option>
                          <option value="right">Right</option>
                          <option value="full">Full Screen</option>
                        </select>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Transition
                        </label>
                        <select
                          value={visuals[activeVisualIndex].transition}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'transition', e.target.value)}
                          className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                        >
                          <option value="fade">Fade</option>
                          <option value="slide">Slide</option>
                          <option value="zoom">Zoom</option>
                          <option value="none">None</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Style Guidance
                        </label>
                        <input
                          type="text"
                          value={visuals[activeVisualIndex].visualStyle || ''}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'visualStyle', e.target.value)}
                          className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                          placeholder="e.g., cartoon, realistic, minimalist"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-foreground mb-1">
                          Reference Text
                        </label>
                        <textarea
                          value={visuals[activeVisualIndex].referenceText || ''}
                          onChange={(e) => handleUpdateVisual(activeVisualIndex, 'referenceText', e.target.value)}
                          className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary resize-y min-h-[40px]"
                          placeholder="Reference to narration text, e.g., 'This visual illustrates the process described above.'"
                        />
                      </div>
                    </div>

                    <div className="mt-4 flex items-center">
                      <input
                        id="remove-background-toggle"
                        type="checkbox"
                        className="mr-2 h-4 w-4 text-primary border-border rounded focus:ring-primary"
                        checked={!!visuals[activeVisualIndex].removeBackground}
                        onChange={e => handleUpdateVisual(activeVisualIndex, 'removeBackground', e.target.checked)}
                      />
                      <label htmlFor="remove-background-toggle" className="text-sm text-foreground select-none cursor-pointer">
                        Remove background from this visual (use project background image)
                      </label>
                    </div>
                    {/* Remove Background Method Radio Group */}
                    <div className="mt-2 flex items-center space-x-4">
                      <span className="text-sm text-foreground">Method:</span>
                      <label className={`flex items-center space-x-1 text-sm ${!visuals[activeVisualIndex].removeBackground ? 'opacity-60 cursor-not-allowed' : ''}`}>
                        <input
                          type="radio"
                          name={`remove-bg-method-${activeVisualIndex}`}
                          value="color"
                          disabled={!visuals[activeVisualIndex].removeBackground}
                          checked={(visuals[activeVisualIndex].removeBackgroundMethod || 'color') === 'color'}
                          onChange={() => handleBgMethodChange('color')}
                        />
                        <span>Color</span>
                      </label>
                      <label className={`flex items-center space-x-1 text-sm ${!visuals[activeVisualIndex].removeBackground ? 'opacity-60 cursor-not-allowed' : ''}`}>
                        <input
                          type="radio"
                          name={`remove-bg-method-${activeVisualIndex}`}
                          value="rembg"
                          disabled={!visuals[activeVisualIndex].removeBackground}
                          checked={visuals[activeVisualIndex].removeBackgroundMethod === 'rembg'}
                          onChange={() => handleBgMethodChange('rembg')}
                        />
                        <span>Rembg</span>
                      </label>
                      <button
                        type="button"
                        className="ml-4 px-2 py-1 border border-border rounded text-xs hover:bg-muted/40 disabled:opacity-50"
                        disabled={!visuals[activeVisualIndex].removeBackground || !visuals[activeVisualIndex].imageUrl}
                        onClick={handlePreviewBgRemoval}
                      >
                        Preview
                      </button>
                      {isPreviewingBgRemoval && <span className="ml-2 text-xs text-muted-foreground">Loading...</span>}
                      {generationError && <span className="ml-2 text-xs text-red-600">{generationError}</span>}
                    </div>
                    {bgRemovalPreview && visuals[activeVisualIndex].removeBackground && (
                      <div className="mt-3">
                        <div className="text-xs text-muted-foreground mb-1">Preview:</div>
                        <img
                          src={`data:image/png;base64,${bgRemovalPreview}`}
                          alt="Background Removal Preview"
                          className="rounded border border-border max-w-full max-h-48"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-border text-foreground rounded-md hover:bg-muted/30"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
              >
                Save Changes
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
