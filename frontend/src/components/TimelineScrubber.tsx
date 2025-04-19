import React, { useRef } from 'react';

interface TimelineScrubberProps {
  currentTime: number;
  totalDuration: number;
  onSeek: (seekTime: number) => void; // Callback function when user seeks
}

const TimelineScrubber: React.FC<TimelineScrubberProps> = ({
  currentTime,
  totalDuration,
  onSeek,
}) => {
  const timelineRef = useRef<HTMLDivElement>(null);

  const handleTimelineClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current || totalDuration <= 0) return;

    const timelineRect = timelineRef.current.getBoundingClientRect();
    const clickX = event.clientX - timelineRect.left;
    // Ensure click ratio is between 0 and 1
    const clickRatio = Math.max(0, Math.min(1, clickX / timelineRect.width));
    const seekTime = clickRatio * totalDuration;

    console.log(`[TimelineScrubber] Click detected. Ratio: ${clickRatio.toFixed(3)}, Seek time: ${seekTime.toFixed(2)}`);
    onSeek(seekTime); // Call the passed-in seek handler
  };

  // Calculate the percentage for the progress bar and handle position
  const progressPercent = totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0;
  // Clamp the percentage between 0 and 100 to avoid visual glitches
  const clampedProgressPercent = Math.max(0, Math.min(100, progressPercent));

  return (
    <div
      ref={timelineRef}
      className="flex-grow h-2 bg-muted rounded-full cursor-pointer relative group" // Added group for potential hover effects on handle
      onClick={handleTimelineClick}
      role="slider"
      aria-valuemin={0}
      aria-valuemax={totalDuration}
      aria-valuenow={currentTime}
      aria-label="Timeline Scrubber"
      tabIndex={0} // Make it focusable
      // Add keyboard interaction if needed (e.g., arrow keys)
    >
      {/* Progress Fill */}
      <div
        className="absolute top-0 left-0 h-full bg-primary rounded-full"
        style={{ width: `${clampedProgressPercent}%` }}
      />
      {/* Scrubber Handle */}
      <div
        className="absolute top-1/2 h-4 w-4 bg-primary rounded-full border-2 border-background -translate-y-1/2 -translate-x-1/2 pointer-events-none" // Prevent handle from interfering with clicks on the bar
        style={{ left: `${clampedProgressPercent}%` }}
        // Consider adding transition for smoother movement: transition-left duration-100 ease-linear
      />
    </div>
  );
};

export default TimelineScrubber;
