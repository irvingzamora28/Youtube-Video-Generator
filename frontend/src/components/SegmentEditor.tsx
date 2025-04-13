import { useState } from 'react';
import { ScriptSegment, Visual } from '../types/script';

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

  const handleAddVisual = () => {
    const newVisual: Visual = {
      id: `visual-${Date.now()}`,
      description: '',
      timestamp: 0,
      duration: Math.min(5, segment.duration),
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

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-card rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto border border-border">
        <div className="px-6 py-4 border-b border-border">
          <h2 className="text-xl font-semibold text-foreground">Edit Segment</h2>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          <div className="space-y-6">
            <div>
              <label htmlFor="narrationText" className="block text-sm font-medium text-foreground mb-1">
                Narration Text
              </label>
              <textarea
                id="narrationText"
                value={narrationText}
                onChange={(e) => setNarrationText(e.target.value)}
                rows={4}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
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
                    <div className="w-16 h-16 bg-muted/30 rounded flex items-center justify-center">
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
                    <button
                      type="button"
                      onClick={() => handleRemoveVisual(activeVisualIndex)}
                      className="text-destructive hover:text-destructive/90 text-sm"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="space-y-4">
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
