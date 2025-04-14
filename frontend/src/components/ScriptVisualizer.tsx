import { useState, useRef, useEffect } from 'react';
import { Script, Visual } from '../types/script';
import SegmentTimeline from './SegmentTimeline';

type ScriptVisualizerProps = {
  script: Script;
  onClose: () => void;
};

export default function ScriptVisualizer({ script, onClose }: ScriptVisualizerProps) {
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [currentSegmentId, setCurrentSegmentId] = useState<string | null>(null);
  const [currentVisualIndex, setCurrentVisualIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const modalRef = useRef<HTMLDivElement>(null);

  // Handle escape key press
  useEffect(() => {
    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscapeKey);

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [onClose]);

  const currentSection = script.sections[currentSectionIndex];

  // Initialize the current segment if not set
  if (!currentSegmentId && currentSection.segments.length > 0) {
    setCurrentSegmentId(currentSection.segments[0].id);
  }

  const currentSegment = currentSection.segments.find(s => s.id === currentSegmentId) || currentSection.segments[0];
  const currentVisual = currentSegment?.visuals[currentVisualIndex] || null;

  const goToNextSection = () => {
    if (currentSectionIndex < script.sections.length - 1) {
      setCurrentSectionIndex(currentSectionIndex + 1);
      setCurrentSegmentId(null);
      setCurrentVisualIndex(0);
    }
  };

  const goToPreviousSection = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(currentSectionIndex - 1);
      setCurrentSegmentId(null);
      setCurrentVisualIndex(0);
    }
  };

  const goToNextSegment = () => {
    const currentSegmentIndex = currentSection.segments.findIndex(s => s.id === currentSegmentId);
    if (currentSegmentIndex < currentSection.segments.length - 1) {
      setCurrentSegmentId(currentSection.segments[currentSegmentIndex + 1].id);
      setCurrentVisualIndex(0);
    } else {
      goToNextSection();
    }
  };

  const goToPreviousSegment = () => {
    const currentSegmentIndex = currentSection.segments.findIndex(s => s.id === currentSegmentId);
    if (currentSegmentIndex > 0) {
      setCurrentSegmentId(currentSection.segments[currentSegmentIndex - 1].id);
      setCurrentVisualIndex(0);
    } else {
      goToPreviousSection();
    }
  };

  const goToNextVisual = () => {
    if (currentSegment && currentVisualIndex < currentSegment.visuals.length - 1) {
      setCurrentVisualIndex(currentVisualIndex + 1);
    } else {
      goToNextSegment();
    }
  };

  const goToPreviousVisual = () => {
    if (currentVisualIndex > 0) {
      setCurrentVisualIndex(currentVisualIndex - 1);
    } else {
      goToPreviousSegment();
    }
  };

  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Generate a visualization based on the current visual
  const getVisualization = (visual: Visual | null) => {
    if (!visual) {
      return (
        <div className="flex items-center justify-center h-64 bg-muted/20 rounded-lg">
          <p className="text-muted-foreground">No visual available</p>
        </div>
      );
    }

    // If we have an image URL, show it
    if (visual.imageUrl) {
      return (
        <div className="flex items-center justify-center h-64 bg-muted/20 rounded-lg">
          <img
            src={visual.imageUrl}
            alt={visual.altText || visual.description}
            className="max-h-full max-w-full object-contain"
          />
        </div>
      );
    }

    // Otherwise show a placeholder based on the visual type
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-muted/20 rounded-lg">
        {visual.visualType === 'image' && (
          <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Stickman figure */}
            <circle cx="60" cy="30" r="15" stroke="currentColor" strokeWidth="2" />
            <line x1="60" y1="45" x2="60" y2="85" stroke="currentColor" strokeWidth="2" />
            <line x1="60" y1="60" x2="30" y2="50" stroke="currentColor" strokeWidth="2" />
            <line x1="60" y1="60" x2="90" y2="50" stroke="currentColor" strokeWidth="2" />
            <line x1="60" y1="85" x2="40" y2="115" stroke="currentColor" strokeWidth="2" />
            <line x1="60" y1="85" x2="80" y2="115" stroke="currentColor" strokeWidth="2" />
          </svg>
        )}

        {visual.visualType === 'animation' && (
          <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Animation placeholder */}
            <circle cx="60" cy="60" r="40" stroke="currentColor" strokeWidth="2" strokeDasharray="5 5">
              <animateTransform
                attributeName="transform"
                attributeType="XML"
                type="rotate"
                from="0 60 60"
                to="360 60 60"
                dur="10s"
                repeatCount="indefinite"
              />
            </circle>
            <circle cx="60" cy="30" r="10" fill="currentColor">
              <animate
                attributeName="cy"
                values="30;40;30"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>
          </svg>
        )}

        {visual.visualType === 'diagram' && (
          <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            {/* Diagram placeholder */}
            <rect x="20" y="20" width="30" height="30" stroke="currentColor" strokeWidth="2" />
            <rect x="70" y="20" width="30" height="30" stroke="currentColor" strokeWidth="2" />
            <rect x="45" y="70" width="30" height="30" stroke="currentColor" strokeWidth="2" />
            <line x1="35" y1="50" x2="50" y2="70" stroke="currentColor" strokeWidth="2" />
            <line x1="85" y1="50" x2="70" y2="70" stroke="currentColor" strokeWidth="2" />
          </svg>
        )}

        {visual.visualType === 'text' && (
          <div className="text-center p-4 border border-border rounded-md">
            <p className="text-foreground font-medium">Text Overlay</p>
            <p className="text-muted-foreground text-sm mt-2">{visual.description}</p>
          </div>
        )}

        <p className="text-muted-foreground text-sm mt-4">{visual.description}</p>
      </div>
    );
  };

  // Handle clicks outside the modal
  const handleOutsideClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
      onClick={handleOutsideClick}
    >
      <div
        ref={modalRef}
        className="bg-card rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] overflow-y-auto border border-border"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-border flex justify-between items-center">
          <h2 className="text-xl font-semibold text-foreground">Script Preview</h2>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-foreground">
              {currentSectionIndex + 1}. {currentSection.title}
            </h3>
            <div className="text-sm text-muted-foreground">
              Duration: {formatTime(currentSection.totalDuration)}
            </div>
          </div>

          {/* Segment timeline */}
          <SegmentTimeline
            section={currentSection}
            onSegmentSelect={setCurrentSegmentId}
            selectedSegmentId={currentSegmentId}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <h4 className="text-sm font-medium text-muted-foreground">Visual Preview</h4>
                {currentSegment && currentSegment.visuals.length > 1 && (
                  <div className="text-xs text-muted-foreground">
                    Visual {currentVisualIndex + 1} of {currentSegment.visuals.length}
                  </div>
                )}
              </div>

              {getVisualization(currentVisual)}

              {currentVisual && (
                <div className="mt-2">
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Time: {formatTime(currentSegment.startTime + currentVisual.timestamp)}</span>
                    <span>Duration: {formatTime(currentVisual.duration)}</span>
                  </div>

                  {/* Visual navigation */}
                  {currentSegment && currentSegment.visuals.length > 1 && (
                    <div className="flex justify-center mt-2 space-x-2">
                      <button
                        onClick={goToPreviousVisual}
                        disabled={currentVisualIndex === 0 && currentSection.segments.findIndex(s => s.id === currentSegmentId) === 0}
                        className="px-2 py-1 bg-muted text-muted-foreground rounded-md text-xs disabled:opacity-50"
                      >
                        Previous Visual
                      </button>
                      <button
                        onClick={goToNextVisual}
                        disabled={currentVisualIndex === currentSegment.visuals.length - 1 && currentSection.segments.findIndex(s => s.id === currentSegmentId) === currentSection.segments.length - 1}
                        className="px-2 py-1 bg-muted text-muted-foreground rounded-md text-xs disabled:opacity-50"
                      >
                        Next Visual
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div>
              <h4 className="text-sm font-medium text-muted-foreground mb-2">Narration</h4>
              <div className="p-4 bg-muted/20 rounded-lg h-64 overflow-y-auto">
                {currentSegment ? (
                  <div className="relative">
                    <p className="text-foreground">{currentSegment.narrationText}</p>

                    {/* Highlight the text that corresponds to the current visual */}
                    {currentVisual && (
                      <div className="absolute top-0 left-0 right-0 pointer-events-none">
                        <p>
                          {/* Calculate the approximate text range for the current visual */}
                          {(() => {
                            const charsPerSecond = currentSegment.narrationText.length / currentSegment.duration;
                            const startChar = Math.floor(currentVisual.timestamp * charsPerSecond);
                            const endChar = Math.min(
                              Math.floor((currentVisual.timestamp + currentVisual.duration) * charsPerSecond),
                              currentSegment.narrationText.length
                            );

                            return (
                              <>
                                <span className="invisible">{currentSegment.narrationText.substring(0, startChar)}</span>
                                <span className="bg-primary/30 text-transparent">
                                  {currentSegment.narrationText.substring(startChar, endChar)}
                                </span>
                              </>
                            );
                          })()}
                        </p>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-muted-foreground">No segment selected</p>
                )}
              </div>

              {/* Segment navigation */}
              {currentSection.segments.length > 1 && (
                <div className="flex justify-center mt-4 space-x-2">
                  <button
                    onClick={goToPreviousSegment}
                    disabled={currentSection.segments.findIndex(s => s.id === currentSegmentId) === 0 && currentSectionIndex === 0}
                    className="px-3 py-1 bg-secondary text-secondary-foreground rounded-md text-sm disabled:opacity-50"
                  >
                    Previous Segment
                  </button>
                  <button
                    onClick={goToNextSegment}
                    disabled={currentSection.segments.findIndex(s => s.id === currentSegmentId) === currentSection.segments.length - 1 && currentSectionIndex === script.sections.length - 1}
                    className="px-3 py-1 bg-secondary text-secondary-foreground rounded-md text-sm disabled:opacity-50"
                  >
                    Next Segment
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Section navigation */}
          <div className="mt-6 flex justify-between items-center">
            <button
              onClick={goToPreviousSection}
              disabled={currentSectionIndex === 0}
              className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous Section
            </button>

            <div className="text-sm text-muted-foreground">
              Section {currentSectionIndex + 1} of {script.sections.length}
            </div>

            <button
              onClick={goToNextSection}
              disabled={currentSectionIndex === script.sections.length - 1}
              className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next Section
            </button>
          </div>

          {/* Playback controls */}
          <div className="mt-4 flex justify-center">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
            >
              {isPlaying ? (
                <span className="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Pause Preview
                </span>
              ) : (
                <span className="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                  </svg>
                  Play Preview
                </span>
              )}
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-border">
            <button
              onClick={onClose}
              className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md"
            >
              Close Preview
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
