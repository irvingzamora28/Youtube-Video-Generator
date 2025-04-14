import { useState, useRef, useEffect } from 'react';
import { ScriptSegment, Visual } from '../types/script';
import { generateImageForVisual } from '../services/api';

type SegmentEditorProps = {
  segment: ScriptSegment;
  onSave: (updatedSegment: ScriptSegment) => void;
  onCancel: () => void;
};

export default function SegmentEditor({ segment, onSave, onCancel }: SegmentEditorProps) {
  const [narrationText, setNarrationText] = useState(segment.narrationText);
  const [startTime, setStartTime] = useState(segment.startTime);
  const [duration, setDuration] = useState(segment.duration);
  const [visuals, setVisuals] = useState<Visual[]>(segment.visuals);
  const [activeVisualIndex, setActiveVisualIndex] = useState<number | null>(null);
  const [selectedTextRange, setSelectedTextRange] = useState<{start: number, end: number} | null>(null);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

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
      // Generate the image
      const imageUrl = await generateImageForVisual(visual);

      // Update the visual with the image URL
      handleUpdateVisual(activeVisualIndex, 'imageUrl', imageUrl);
    } catch (error) {
      console.error('Error generating image:', error);
      // Extract the error message if available
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setGenerationError(`Failed to generate image: ${errorMessage}`);
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
    onSave({
      ...segment,
      narrationText,
      startTime,
      duration,
      visuals,
    });
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
                <button
                  type="button"
                  onClick={handleAddVisual}
                  className="px-2 py-1 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90"
                >
                  Add Visual
                </button>
              </div>

              {/* Visual thumbnails */}
              <div className="flex flex-wrap gap-2 mb-4">
                {visuals.map((visual, index) => (
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
                    <div className="flex space-x-2">
                      <button
                        type="button"
                        onClick={handleGenerateImage}
                        disabled={isGeneratingImage}
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
                      <button
                        type="button"
                        onClick={() => handleRemoveVisual(activeVisualIndex)}
                        className="text-destructive hover:text-destructive/90 text-sm"
                      >
                        Remove
                      </button>
                    </div>
                  </div>

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
