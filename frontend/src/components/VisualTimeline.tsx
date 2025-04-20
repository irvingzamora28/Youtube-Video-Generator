import React, { useCallback, useImperativeHandle, forwardRef, useRef } from 'react';
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

const VisualTimeline = forwardRef(function VisualTimeline(
  { script }: VisualTimelineProps,
  ref: React.Ref<{ playAllSegments: () => void }>
) {
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

  // --- Full Audio Preload and Playback Orchestration ---
  const audioRefs = useRef<(HTMLAudioElement | null)[]>([]);
  const isFullPlaybackRef = useRef(false);
  const [fullPlaybackIndex, setFullPlaybackIndex] = React.useState<number | null>(null);

  // Preload all audios
  const playAllSegments = React.useCallback(() => {
    if (allSegments.length === 0) return;
    isFullPlaybackRef.current = true;
    setFullPlaybackIndex(0);
    setCurrentSegmentIndex(0);
    setCurrentTime(0);
    // Play the first audio and reset to start
    setTimeout(() => {
      const audio = audioRefs.current[0];
      if (audio) {
        audio.currentTime = 0;
        audio.play();
      }
    }, 0);
  }, [allSegments, setCurrentSegmentIndex, setCurrentTime]);

  // Sequential playback logic
  // Track last played segment index to detect new segment
  const lastPlaybackIndexRef = React.useRef<number | null>(null);
  React.useEffect(() => {
    if (fullPlaybackIndex === null) return;
    // Sync visuals/timeline
    setCurrentSegmentIndex(fullPlaybackIndex);
    // Attach timeupdate handler to update currentTime
    const audio = audioRefs.current[fullPlaybackIndex];
    if (audio) {
      const segmentStartTime = allSegments.slice(0, fullPlaybackIndex).reduce((sum, s) => sum + (s.duration || 0), 0);
      const handleTimeUpdate = () => {
        setCurrentTime(segmentStartTime + audio.currentTime);
      };
      audio.addEventListener('timeupdate', handleTimeUpdate);
      // Only track segment change, do not control playback here
      lastPlaybackIndexRef.current = fullPlaybackIndex;
      // Cleanup
      return () => {
        audio.removeEventListener('timeupdate', handleTimeUpdate);
      };
    }
  }, [fullPlaybackIndex, setCurrentSegmentIndex, setCurrentTime, allSegments]);

  // Handler for when an audio ends
  const handleAudioEnded = (idx: number) => {
    if (!isFullPlaybackRef.current) return;
    if (idx < allSegments.length - 1) {
      setFullPlaybackIndex(idx + 1);
      setTimeout(() => {
        const nextAudio = audioRefs.current[idx + 1];
        if (nextAudio) {
          nextAudio.currentTime = 0;
          nextAudio.play();
        }
      }, 0);
    } else {
      // End of playback
      isFullPlaybackRef.current = false;
      setFullPlaybackIndex(null);
    }
  };

  // Expose the playAllSegments method to parent via ref
  useImperativeHandle(ref, () => ({ playAllSegments }), [playAllSegments]);

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

  // Handler for selecting a segment directly
  const handleSegmentSelect = useCallback((selectedSegmentIndex: number) => {
    console.log(`[VisualTimeline] handleSegmentSelect called. Selected Segment Index: ${selectedSegmentIndex}`);
    // Calculate the start time of the selected segment
    const startTime = allSegments.slice(0, selectedSegmentIndex).reduce((sum, s) => sum + (s.duration || 0), 0);
    console.log(`[VisualTimeline] Calculated start time for segment ${selectedSegmentIndex + 1}: ${startTime.toFixed(2)}`);

    // Use seekAudio to jump to the beginning of the selected segment
    // Pass the selected index directly
    seekAudio(startTime, selectedSegmentIndex);

    // Optional: Pause playback if it was playing when a new segment is clicked
    if (isPlaying && audioRef.current) {
        handlePlayPause(); // Toggle to pause
    }

  }, [allSegments, seekAudio, isPlaying, handlePlayPause, audioRef]); // Include dependencies

  // --- Play/Pause logic for TimelineControls ---
  // Use a unified isPlaying state: true if either full playback audio or single audio is playing
  const unifiedIsPlaying =
    (fullPlaybackIndex !== null && audioRefs.current[fullPlaybackIndex]?.paused === false) ||
    (fullPlaybackIndex === null && isPlaying);

  // Unified play/pause handler
  const unifiedHandlePlayPause = () => {
    if (fullPlaybackIndex !== null) {
      // Full playback mode
      const audio = audioRefs.current[fullPlaybackIndex];
      if (audio) {
        if (audio.paused) {
          audio.play();
        } else {
          audio.pause();
        }
      }
    } else {
      // Single segment mode
      handlePlayPause();
    }
  };

  // --- Render ---
  return (
    <div className="space-y-4">
      {/* Hidden Audio Elements for Full Playback - preload all */}
      <div style={{ display: 'none' }}>
        {allSegments.map((segment, idx) => (
          <audio
            key={segment.id || `segment-audio-${idx}`}
            ref={el => { audioRefs.current[idx] = el; }}
            src={segment.audioUrl ? normalizeUrl(segment.audioUrl) : undefined}
            preload="auto"
            onEnded={() => handleAudioEnded(idx)}
          />
        ))}
      </div>
      {/* Single Audio Element for Individual Playback */}
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
          isPlaying={unifiedIsPlaying}
          handlePlayPause={unifiedHandlePlayPause}
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
        onSegmentSelect={handleSegmentSelect} // Pass the handler down
      />
    </div>
  );
});

export default VisualTimeline;
