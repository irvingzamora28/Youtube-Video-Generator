import React, { useCallback } from 'react';
import { Script, ScriptSegment, Visual } from '../types/script';
import { useTimelineState } from '../hooks/useTimelineState';
import { useAudioPlayback } from '../hooks/useAudioPlayback';
import VisualPreview from './VisualPreview';
import TimelineControls from './TimelineControls';
import TimelineScrubber from './TimelineScrubber';
import DetailedTimelineView from './DetailedTimelineView';

type VisualTimelineProps = {
  script: Script;
};

const VisualTimeline: React.FC<VisualTimelineProps> = ({ script }) => {
  // --- Prepare Data ---
  const allSegments = script.sections.flatMap(section => section.segments);
  const totalDuration = script.totalDuration || allSegments.reduce((sum, seg) => sum + (seg.duration || 0), 0);

  // --- Helper Functions ---
  // Normalize URL to ensure it points to the static path if needed
  const normalizeUrl = useCallback((path?: string): string | undefined => {
    // Check if path is valid, not empty, and doesn't already start with /static/
    if (path && path !== '' && !path.startsWith('/static/')) {
      return `/static/${path}`;
    }
    return path || undefined; // Return path as is (could be already correct or empty/undefined)
  }, []);

  // --- Hooks ---
  const {
    currentTime,
    setCurrentTime,
    currentSegmentIndex,
    setCurrentSegmentIndex,
    currentVisualIndex,
  } = useTimelineState({ allSegments, totalDuration });

  const {
    audioRef,
    isPlaying,
    handlePlayPause,
    seekAudio,
  } = useAudioPlayback({
    allSegments,
    totalDuration,
    currentSegmentIndex,
    setCurrentSegmentIndex,
    setCurrentTime,
    normalizeUrl, // Pass the memoized normalizeUrl
  });

  // --- Derived State ---
  const currentSegment: ScriptSegment | undefined = allSegments[currentSegmentIndex];
  const currentVisual: Visual | undefined | null = currentSegment?.visuals[currentVisualIndex];

  // --- Event Handlers ---
  // Handler for seek requests from the TimelineScrubber
  const handleSeek = useCallback((seekTime: number) => {
    // Find the target segment index based on the seek time
    let elapsed = 0;
    let targetSegmentIdx = 0;
    for (let i = 0; i < allSegments.length; i++) {
      const segmentDuration = allSegments[i].duration || 0;
      // If seekTime is within this segment or it's the last segment
      if (seekTime < elapsed + segmentDuration || i === allSegments.length - 1) {
        targetSegmentIdx = i;
        break;
      }
      elapsed += segmentDuration;
    }
    console.log(`[VisualTimeline] handleSeek called. Time: ${seekTime.toFixed(2)}, Target Segment: ${targetSegmentIdx + 1}`);
    // Call the seekAudio function from the hook
    seekAudio(seekTime, targetSegmentIdx);
  }, [allSegments, seekAudio]); // Dependencies: allSegments for calculation, seekAudio to call

  // --- Render ---
  return (
    <div className="space-y-4">
      {/* Hidden Audio Element - controlled by useAudioPlayback hook */}
      <audio ref={audioRef} />

      {/* Visual Preview Area - uses VisualPreview component */}
      <VisualPreview
        currentVisual={currentVisual}
        normalizeUrl={normalizeUrl}
      />

      {/* Timeline Controls & Scrubber */}
      <div className="flex items-center gap-4">
        {/* Uses TimelineControls component */}
        <TimelineControls
          isPlaying={isPlaying}
          handlePlayPause={handlePlayPause}
          currentTime={currentTime}
          totalDuration={totalDuration}
        />
        {/* Uses TimelineScrubber component */}
        <TimelineScrubber
          currentTime={currentTime}
          totalDuration={totalDuration}
          onSeek={handleSeek} // Pass the new handler
        />
      </div>

      {/* Detailed Timeline View - uses DetailedTimelineView component */}
      <DetailedTimelineView
        allSegments={allSegments}
        currentTime={currentTime}
        currentSegmentIndex={currentSegmentIndex}
        totalDuration={totalDuration}
      />
    </div>
  );
};

export default VisualTimeline;
