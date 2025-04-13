import { useState } from 'react';
import { ScriptSection, ScriptSegment, Visual } from '../types/script';

type SegmentTimelineProps = {
  section: ScriptSection;
  onSegmentSelect: (segmentId: string) => void;
  selectedSegmentId: string | null;
};

export default function SegmentTimeline({ section, onSegmentSelect, selectedSegmentId }: SegmentTimelineProps) {
  // Calculate the total duration for scaling
  const totalDuration = section.totalDuration;
  
  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="mt-4">
      <h3 className="text-sm font-medium text-color-muted-foreground mb-2">Timeline</h3>
      
      {/* Timeline ruler */}
      <div className="relative h-8 mb-1 flex">
        {/* Time markers */}
        {Array.from({ length: Math.ceil(totalDuration / 15) + 1 }).map((_, i) => (
          <div key={i} className="absolute" style={{ left: `${(i * 15 / totalDuration) * 100}%` }}>
            <div className="h-2 border-l border-color-border"></div>
            <div className="text-xs text-color-muted-foreground">{formatTime(i * 15)}</div>
          </div>
        ))}
      </div>
      
      {/* Segments timeline */}
      <div className="relative h-12 bg-color-muted/20 rounded-md mb-4">
        {section.segments.map((segment) => {
          const segmentWidth = (segment.duration / totalDuration) * 100;
          const segmentLeft = (segment.startTime / totalDuration) * 100;
          
          return (
            <div
              key={segment.id}
              className={`absolute h-full rounded-md cursor-pointer transition-all hover:brightness-90 flex items-center justify-center overflow-hidden ${
                selectedSegmentId === segment.id 
                  ? 'ring-2 ring-color-primary ring-offset-1' 
                  : 'border border-color-border'
              }`}
              style={{
                left: `${segmentLeft}%`,
                width: `${segmentWidth}%`,
                backgroundColor: selectedSegmentId === segment.id ? 'var(--color-primary/20)' : 'var(--color-card)',
              }}
              onClick={() => onSegmentSelect(segment.id)}
            >
              <div className="text-xs truncate px-2 text-color-foreground">
                {segment.narrationText.substring(0, 20)}...
              </div>
              
              {/* Visual indicators */}
              <div className="absolute bottom-0 left-0 right-0 h-2 flex">
                {segment.visuals.map((visual, index) => {
                  const visualWidth = (visual.duration / segment.duration) * 100;
                  const visualLeft = (visual.timestamp / segment.duration) * 100;
                  
                  return (
                    <div
                      key={visual.id}
                      className="absolute h-full bg-color-primary/60"
                      style={{
                        left: `${visualLeft}%`,
                        width: `${visualWidth}%`,
                      }}
                      title={visual.description}
                    />
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Selected segment details */}
      {selectedSegmentId && (
        <div className="bg-color-muted/10 p-3 rounded-md">
          <div className="text-sm text-color-foreground">
            {section.segments.find(s => s.id === selectedSegmentId)?.narrationText}
          </div>
        </div>
      )}
    </div>
  );
}
