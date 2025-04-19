import React from 'react';

// Helper function to format time (seconds) to MM:SS
const formatTime = (seconds: number): string => {
  if (isNaN(seconds) || seconds < 0) {
    return '0:00';
  }
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

interface TimelineControlsProps {
  isPlaying: boolean;
  handlePlayPause: () => void;
  currentTime: number;
  totalDuration: number;
}

const TimelineControls: React.FC<TimelineControlsProps> = ({
  isPlaying,
  handlePlayPause,
  currentTime,
  totalDuration,
}) => {
  return (
    <div className="flex items-center gap-4">
      <button
        onClick={handlePlayPause}
        className="p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        aria-label={isPlaying ? 'Pause' : 'Play'}
      >
        {isPlaying ? (
          // Pause Icon
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
          </svg>
        ) : (
          // Play Icon
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
          </svg>
        )}
      </button>
      <div className="text-sm font-mono text-muted-foreground tabular-nums">
        {formatTime(currentTime)} / {formatTime(totalDuration)}
      </div>
    </div>
  );
};

export default TimelineControls;
// Export formatTime if it might be useful elsewhere, or move to a utils file
export { formatTime };
