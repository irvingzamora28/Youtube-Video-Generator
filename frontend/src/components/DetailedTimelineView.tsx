import React, { useState, useRef, useEffect } from 'react';
import { ScriptSegment } from '../types/script';
import { formatTime } from './TimelineControls';

interface DetailedTimelineViewProps {
  allSegments: ScriptSegment[];
  currentTime: number;
  currentSegmentIndex: number;
  totalDuration: number;
  onSegmentSelect: (segmentIndex: number) => void;
}

const DetailedTimelineView: React.FC<DetailedTimelineViewProps> = ({
  allSegments,
  currentTime,
  currentSegmentIndex,
  totalDuration,
  onSegmentSelect,
}) => {
  // Keyboard navigation state
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const timelineRef = useRef<HTMLDivElement>(null);
  const segmentRefs = useRef<Array<HTMLDivElement | null>>([]);

  // Helper to determine visual block color (can be customized)
  const getVisualColor = (visualType: string | undefined): string => {
    switch (visualType) {
      case 'image': return 'bg-blue-500/50';
      case 'animation': return 'bg-green-500/50';
      case 'diagram': return 'bg-purple-500/50';
      case 'text': return 'bg-orange-500/50';
      default: return 'bg-gray-500/50';
    }
  };

  // Focus timeline on segment click
  const handleSegmentClick = (idx: number) => {
    setSelectedIdx(idx);
    onSegmentSelect(idx);
    timelineRef.current?.focus();
  };

  // Keyboard navigation handler
  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (selectedIdx === null) return;
    if (e.key === 'ArrowLeft') {
      if (selectedIdx > 0) {
        setSelectedIdx(selectedIdx - 1);
        onSegmentSelect(selectedIdx - 1);
      }
      e.preventDefault();
    } else if (e.key === 'ArrowRight') {
      if (selectedIdx < allSegments.length - 1) {
        setSelectedIdx(selectedIdx + 1);
        onSegmentSelect(selectedIdx + 1);
      }
      e.preventDefault();
    }
  };

  // Scroll selected segment into view
  useEffect(() => {
    if (selectedIdx !== null && segmentRefs.current[selectedIdx]) {
      segmentRefs.current[selectedIdx]?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }, [selectedIdx]);

  // If currentSegmentIndex changes from parent, update selectedIdx
  useEffect(() => {
    setSelectedIdx(currentSegmentIndex);
  }, [currentSegmentIndex]);

  return (
    <div
      className="relative h-24 bg-muted/20 rounded-md border border-border overflow-hidden focus:outline-none"
      ref={timelineRef}
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-label="Detailed Timeline View"
      role="listbox"
    >
      {allSegments.map((segment, segIdx) => {
        const segmentDuration = segment.duration || 0.1; // Use min duration to prevent division by zero
        const segmentWidthPercent = totalDuration > 0 ? (segmentDuration / totalDuration) * 100 : 0;
        // Calculate the start time of this segment
        const segmentStartTime = allSegments.slice(0, segIdx).reduce((sum, s) => sum + (s.duration || 0), 0);
        const segmentLeftPercent = totalDuration > 0 ? (segmentStartTime / totalDuration) * 100 : 0;

        // Determine if the current time falls within this segment for highlighting visuals
        const timeWithinSegmentForVisuals = currentSegmentIndex === segIdx
          ? currentTime - segmentStartTime
          : -1; // -1 indicates time is not within this segment

        return (
          <div
            ref={el => { segmentRefs.current[segIdx] = el; }}
            key={segment.id || `segment-${segIdx}`}
            className={`absolute h-full border-r border-border/50 cursor-pointer hover:bg-primary/5 ${segIdx === selectedIdx ? 'bg-primary/20 ring-2 ring-primary ring-offset-2 z-20' : segIdx === currentSegmentIndex ? 'bg-primary/10 ring-1 ring-primary' : ''}`}
            style={{ left: `${segmentLeftPercent}%`, width: `${segmentWidthPercent}%` }}
            title={`Segment ${segIdx + 1}: ${segment.narrationText?.substring(0, 50) ?? ''}... (Click to select)`}
            tabIndex={-1}
            aria-selected={segIdx === selectedIdx}
            onClick={() => handleSegmentClick(segIdx)}
          >
            {/* Render Visuals within the Segment */}
            {segment.visuals.map((visual, visIdx) => {
              const visualTimestamp = visual.timestamp ?? 0;
              // Ensure visual duration is at least a small positive number for rendering
              const visualDuration = Math.max(visual.duration ?? 0, 0.05);
              // Use segment duration for calculating relative position/width, ensure it's positive
              const segmentEffectiveDuration = Math.max(segmentDuration, 0.1);

              const visualLeftPercent = segmentEffectiveDuration > 0 ? (visualTimestamp / segmentEffectiveDuration) * 100 : 0;
              const visualWidthPercent = segmentEffectiveDuration > 0 ? (visualDuration / segmentEffectiveDuration) * 100 : 0;

              // Determine if this specific visual is the currently active one
              const isActiveVisual = segIdx === currentSegmentIndex &&
                                     timeWithinSegmentForVisuals >= visualTimestamp &&
                                     timeWithinSegmentForVisuals < (visualTimestamp + visualDuration);

              // Calculate absolute start and end times for the title tooltip
              const visualStartTimeAbsolute = segmentStartTime + visualTimestamp;
              const visualEndTimeAbsolute = visualStartTimeAbsolute + visualDuration;

              return (
                <div
                  key={visual.id || `visual-${segIdx}-${visIdx}`} // Use visual.id if available
                  className={`absolute bottom-0 h-1/2 ${isActiveVisual ? 'ring-2 ring-primary ring-offset-1 ring-offset-background' : ''} ${getVisualColor(visual.visualType)}`}
                  style={{
                    left: `${Math.max(0, Math.min(100, visualLeftPercent))}%`, // Clamp values
                    width: `${Math.max(0, Math.min(100 - visualLeftPercent, visualWidthPercent))}%` // Clamp width
                   }}
                  title={`${visual.description || 'Visual'} (${formatTime(visualStartTimeAbsolute)} - ${formatTime(visualEndTimeAbsolute)})`}
                />
              );
            })}
             {/* Segment Number Label */}
             <div className="absolute top-1 left-1 text-[10px] text-muted-foreground bg-background/50 px-1 rounded pointer-events-none">
                 Seg {segIdx + 1}
             </div>
          </div>
        );
      })}

      {/* Playhead Indicator */}
      <div
         className="absolute top-0 bottom-0 w-0.5 bg-destructive z-10 pointer-events-none"
         style={{ left: `${totalDuration > 0 ? Math.max(0, Math.min(100, (currentTime / totalDuration) * 100)) : 0}%` }} // Clamp playhead position
       />
    </div>
  );
};

export default DetailedTimelineView;
