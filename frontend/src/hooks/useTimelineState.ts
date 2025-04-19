import { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { ScriptSegment } from '../types/script'; // Assuming types are correctly placed

interface UseTimelineStateProps {
  allSegments: ScriptSegment[];
  totalDuration: number;
  initialTime?: number;
  initialSegmentIndex?: number;
  initialVisualIndex?: number;
}

interface UseTimelineStateReturn {
  currentTime: number;
  setCurrentTime: Dispatch<SetStateAction<number>>;
  currentSegmentIndex: number;
  setCurrentSegmentIndex: Dispatch<SetStateAction<number>>;
  currentVisualIndex: number;
  setCurrentVisualIndex: Dispatch<SetStateAction<number>>;
}

export const useTimelineState = ({
  allSegments,
  totalDuration,
  initialTime = 0,
  initialSegmentIndex = 0,
  initialVisualIndex = 0,
}: UseTimelineStateProps): UseTimelineStateReturn => {
  const [currentTime, setCurrentTime] = useState<number>(initialTime);
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState<number>(initialSegmentIndex);
  const [currentVisualIndex, setCurrentVisualIndex] = useState<number>(initialVisualIndex);

  // Effect to update current segment and visual based on time
  useEffect(() => {
    let elapsed = 0;
    let calculatedSegIdx = -1;
    let calculatedVisIdx = -1;
    let found = false;

    for (let i = 0; i < allSegments.length; i++) {
      const segment = allSegments[i];
      const segmentDuration = segment.duration || 0;
      const segmentStartTime = elapsed;
      const segmentEndTime = elapsed + segmentDuration;
      const isLastSegment = i === allSegments.length - 1;

      // Check if currentTime falls within this segment's time range
      // Add a small tolerance for the very end of the timeline
      if (currentTime >= segmentStartTime && (currentTime < segmentEndTime || (isLastSegment && currentTime <= segmentEndTime + 0.01))) {
        calculatedSegIdx = i;
        const timeWithinSegment = currentTime - segmentStartTime;

        // Find the best matching visual within the current segment based on timestamp
        let bestMatchIdx = -1;
        // Iterate backwards to find the *last* visual whose timestamp is <= timeWithinSegment
        for (let j = segment.visuals.length - 1; j >= 0; j--) {
          const visual = segment.visuals[j];
          const visualTimestamp = visual.timestamp ?? 0;
          if (timeWithinSegment >= visualTimestamp) {
            bestMatchIdx = j;
            break; // Found the latest applicable visual
          }
        }
        // If no visual timestamp is matched, default to the first visual if available
        calculatedVisIdx = bestMatchIdx >= 0 ? bestMatchIdx : (segment.visuals.length > 0 ? 0 : -1);
        found = true;
        break; // Found the correct segment, no need to check further
      }
      elapsed += segmentDuration;
    }

    // Handle edge case: currentTime is exactly 0, show the first visual of the first segment
    if (!found && currentTime === 0 && allSegments.length > 0 && allSegments[0].visuals.length > 0) {
        calculatedSegIdx = 0;
        calculatedVisIdx = 0;
        found = true;
    }

    // Update state only if calculated indices are valid and different from current state
    if (found) {
      if (calculatedSegIdx !== currentSegmentIndex) {
        // console.log(`[useTimelineState] Updating segment index from ${currentSegmentIndex} to ${calculatedSegIdx} based on time ${currentTime.toFixed(2)}`);
        setCurrentSegmentIndex(calculatedSegIdx);
      }
      // Ensure visual index is valid before updating
      if (calculatedVisIdx !== -1 && calculatedVisIdx !== currentVisualIndex) {
        // console.log(`[useTimelineState] Updating visual index from ${currentVisualIndex} to ${calculatedVisIdx} in segment ${calculatedSegIdx} based on time ${currentTime.toFixed(2)}`);
        setCurrentVisualIndex(calculatedVisIdx);
      }
    } else if (currentTime >= totalDuration && totalDuration > 0 && allSegments.length > 0) {
      // Handle edge case: currentTime is at or beyond the total duration
      const lastSegIdx = allSegments.length - 1;
      const lastVisIdx = allSegments[lastSegIdx].visuals.length - 1;
      if (currentSegmentIndex !== lastSegIdx) {
        // console.log(`[useTimelineState] Setting to last segment index ${lastSegIdx} as time ${currentTime.toFixed(2)} >= totalDuration ${totalDuration.toFixed(2)}`);
        setCurrentSegmentIndex(lastSegIdx);
      }
      if (lastVisIdx >= 0 && currentVisualIndex !== lastVisIdx) {
        // console.log(`[useTimelineState] Setting to last visual index ${lastVisIdx} as time ${currentTime.toFixed(2)} >= totalDuration ${totalDuration.toFixed(2)}`);
        setCurrentVisualIndex(lastVisIdx);
      }
    }
    // If no segment is found (e.g., empty script or negative time?), indices remain unchanged or at initial values.

  }, [currentTime, allSegments, totalDuration, currentSegmentIndex, currentVisualIndex]); // Dependencies ensure recalculation when relevant values change

  return {
    currentTime,
    setCurrentTime,
    currentSegmentIndex,
    setCurrentSegmentIndex,
    currentVisualIndex,
    setCurrentVisualIndex,
  };
};
