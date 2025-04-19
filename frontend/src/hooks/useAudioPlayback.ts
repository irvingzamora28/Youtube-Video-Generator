import { useState, useRef, useEffect, useCallback, Dispatch, SetStateAction, RefObject } from 'react';
import { ScriptSegment } from '../types/script';

interface UseAudioPlaybackProps {
  allSegments: ScriptSegment[];
  totalDuration: number;
  currentSegmentIndex: number;
  setCurrentSegmentIndex: Dispatch<SetStateAction<number>>;
  setCurrentTime: Dispatch<SetStateAction<number>>;
  normalizeUrl: (path?: string) => string | undefined; // Pass normalizeUrl as a prop
}

interface UseAudioPlaybackReturn {
  audioRef: RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  setIsPlaying: Dispatch<SetStateAction<boolean>>;
  isAudioReady: boolean;
  handlePlayPause: () => void;
  seekAudio: (newTime: number, targetSegmentIdx: number) => void;
}

export const useAudioPlayback = ({
  allSegments,
  totalDuration,
  currentSegmentIndex,
  setCurrentSegmentIndex,
  setCurrentTime,
  normalizeUrl,
}: UseAudioPlaybackProps): UseAudioPlaybackReturn => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isAudioReady, setIsAudioReady] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const playWhenReady = useRef(false); // Flag to play audio once loaded and isPlaying is true
  const internalPauseRef = useRef(false); // Ref to track if the component initiated the pause

  // --- Simulation Logic (Fallback for segments without audio) ---
  const runSimulation = useCallback((segmentIndex: number) => {
    if (segmentIndex >= allSegments.length || !isPlaying) return;

    const segment = allSegments[segmentIndex];
    const segmentDuration = segment.duration || 1; // Use 1s default if duration is 0 or undefined
    console.log(`[useAudioPlayback] Simulating segment ${segmentIndex + 1} duration ${segmentDuration}s`);

    const segmentStartTime = allSegments.slice(0, segmentIndex).reduce((sum, s) => sum + (s.duration || 0), 0);

    if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);

    let startTimestamp: number | null = null;
    const step = (timestamp: number) => {
      if (!isPlaying) {
        if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
        return;
      }
      if (startTimestamp === null) startTimestamp = timestamp;
      const elapsedMs = timestamp - startTimestamp;
      const currentGlobalTime = segmentStartTime + (elapsedMs / 1000);

      // Ensure simulation doesn't exceed segment duration or total duration
      if (currentGlobalTime < segmentStartTime + segmentDuration && currentGlobalTime < totalDuration) {
        setCurrentTime(currentGlobalTime);
        animationFrameRef.current = requestAnimationFrame(step);
      } else {
        // Simulation for this segment ended
        const nextIndex = segmentIndex + 1;
        if (nextIndex < allSegments.length) {
          console.log(`[useAudioPlayback] Simulation ended for segment ${segmentIndex + 1}, moving to ${nextIndex + 1}`);
          setCurrentSegmentIndex(nextIndex); // Trigger loading/simulation for the next segment
        } else {
          // End of all segments
          setIsPlaying(false);
          setCurrentTime(totalDuration); // Ensure time is set to the end
          console.log("[useAudioPlayback] Simulated playback finished.");
        }
      }
    };
    // Set initial time for the simulation step
    setCurrentTime(segmentStartTime);
    animationFrameRef.current = requestAnimationFrame(step);

  }, [allSegments, isPlaying, totalDuration, setCurrentTime, setCurrentSegmentIndex]);

  // --- Audio Loading Logic ---
  const loadAudioForSegment = useCallback((segmentIndex: number) => {
    if (segmentIndex >= allSegments.length) return;

    const segment = allSegments[segmentIndex];
    const audioSrc = segment?.audioUrl ? normalizeUrl(segment.audioUrl) : null;
    const audioElement = audioRef.current;

    // Stop any ongoing simulation
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }

    if (audioSrc && audioElement) {
      const currentFullSrc = audioElement.currentSrc;
      // Ensure target URL is absolute for comparison
      const targetFullSrc = new URL(audioSrc, window.location.origin).href;

      if (currentFullSrc !== targetFullSrc) {
        console.log(`[useAudioPlayback] Loading segment ${segmentIndex + 1} audio: ${audioSrc}`);
        setIsAudioReady(false);
        playWhenReady.current = isPlaying; // Store the intent to play if isPlaying is true
        audioElement.src = audioSrc;
        audioElement.load(); // Important: Trigger load for the new source
      } else {
        // Source is the same, check readiness and play if needed
        setIsAudioReady(audioElement.readyState >= 3); // HAVE_FUTURE_DATA or more
        if (isPlaying && audioElement.paused && isAudioReady) {
             console.log("[useAudioPlayback] Resuming play on same source (already loaded).");
             audioElement.play().catch(e => console.error("Error resuming play:", e));
        } else if (isPlaying && !isAudioReady) {
            // If playing but not ready (e.g., after seek on same src), set flag
            playWhenReady.current = true;
        }
      }
    } else {
      // No audio source for this segment
      setIsAudioReady(false); // Mark as not ready
      if (audioElement) audioElement.src = ''; // Clear src if no audio
      if (isPlaying) {
        // If playback is active, start simulation
        runSimulation(segmentIndex);
      } else {
         // If paused, ensure audio element is paused
         audioElement?.pause();
      }
    }
  }, [allSegments, isPlaying, runSimulation, normalizeUrl, isAudioReady]); // Added isAudioReady dependency


  // --- Effect to load audio when segment index changes ---
   useEffect(() => {
       console.log(`[useAudioPlayback Effect] Segment index changed to ${currentSegmentIndex}. Loading audio/starting sim.`);
       loadAudioForSegment(currentSegmentIndex);
   }, [currentSegmentIndex, loadAudioForSegment]); // Depends only on index and the loader function


  // --- Effect for Audio Element Event Listeners ---
  useEffect(() => {
    const audioElement = audioRef.current;
    if (!audioElement) return;

    const handleCanPlayThrough = () => {
      console.log(`[useAudioPlayback Event] canplaythrough for segment ${currentSegmentIndex + 1}`);
      setIsAudioReady(true);
      // If play was intended while loading, start playback now
      if (playWhenReady.current && isPlaying) {
        playWhenReady.current = false; // Reset flag
        console.log("[useAudioPlayback Event] Attempting play after canplaythrough");
        audioElement.play().catch(e => {
          console.error("Audio play failed after canplaythrough:", e);
          // If play fails (e.g., browser restrictions), update state
          setIsPlaying(false);
        });
      }
    };

    const handleAudioEnd = () => {
      console.log(`[useAudioPlayback Event] ended for segment ${currentSegmentIndex + 1}`);
      const nextIndex = currentSegmentIndex + 1;
      if (nextIndex < allSegments.length && isPlaying) {
        // Move to the next segment if still playing and segments remain
        setCurrentSegmentIndex(nextIndex);
      } else {
        // End of playback (last segment ended or was paused)
        setIsPlaying(false);
        if (nextIndex >= allSegments.length) {
          setCurrentTime(totalDuration); // Ensure time snaps to the end
          console.log("[useAudioPlayback Event] Audio playback finished naturally.");
        }
      }
    };

    const handleTimeUpdate = () => {
      // Update global time based on audio progress only if playing and not seeking
      if (isPlaying && !audioElement.seeking && !internalPauseRef.current) { // Check internalPauseRef too
        let elapsedGlobal = 0;
        // Calculate the start time of the current segment
        for (let i = 0; i < currentSegmentIndex; i++) {
          elapsedGlobal += allSegments[i].duration || 0;
        }
        // Calculate new global time, ensuring it doesn't exceed total duration
        const newTime = Math.min(elapsedGlobal + audioElement.currentTime, totalDuration);
        // Update state, potentially throttling updates slightly
        setCurrentTime(prevTime => Math.abs(newTime - prevTime) > 0.05 ? newTime : prevTime);
      }
    };

    const handleError = (e: Event) => {
      console.error(`[useAudioPlayback Event] Error loading audio source ${audioElement.src}:`, e);
      // Reset state on error
      setIsPlaying(false);
      setIsAudioReady(false);
      playWhenReady.current = false;
      // Potentially try to fallback to simulation or show an error
    };

     const handlePause = () => {
        // If pause was not initiated by our controls (e.g., external pause, end of src)
        // and we thought we were playing, update the state.
        if (!internalPauseRef.current && isPlaying) {
            console.log("[useAudioPlayback Event] Playback paused externally or unexpectedly. Setting isPlaying=false.");
            setIsPlaying(false); // Sync state with audio element
        }
    }

    const handleLoadedMetadata = () => {
        // Metadata loaded, we know the duration etc. Might be ready enough for seeking.
        console.log(`[useAudioPlayback Event] loadedmetadata for segment ${currentSegmentIndex + 1}`);
        // Consider ready if metadata is loaded, allows seeking earlier
        setIsAudioReady(audioElement.readyState >= 1); // HAVE_METADATA or more
    }

    // Add listeners
    audioElement.addEventListener('canplaythrough', handleCanPlayThrough);
    audioElement.addEventListener('ended', handleAudioEnd);
    audioElement.addEventListener('timeupdate', handleTimeUpdate);
    audioElement.addEventListener('error', handleError);
    audioElement.addEventListener('pause', handlePause);
    audioElement.addEventListener('loadedmetadata', handleLoadedMetadata);

    // Cleanup function to remove listeners
    return () => {
      audioElement.removeEventListener('canplaythrough', handleCanPlayThrough);
      audioElement.removeEventListener('ended', handleAudioEnd);
      audioElement.removeEventListener('timeupdate', handleTimeUpdate);
      audioElement.removeEventListener('error', handleError);
      audioElement.removeEventListener('pause', handlePause);
      audioElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
      // Also cancel any pending animation frame on cleanup
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
    };
  // Re-run this effect if the segment index changes (to apply listeners to potentially new audio src)
  // or if isPlaying status changes (relevant for handlePause logic)
  }, [currentSegmentIndex, allSegments, totalDuration, isPlaying, setCurrentTime, setCurrentSegmentIndex]);


  // --- UI Interaction Handlers ---
  const handlePlayPause = useCallback(() => {
    const targetIsPlaying = !isPlaying;
    setIsPlaying(targetIsPlaying); // Set state immediately for responsiveness

    if (targetIsPlaying) {
      playWhenReady.current = true; // Set intent to play
      const currentGlobalTime = allSegments.slice(0, currentSegmentIndex).reduce((sum, s) => sum + (s.duration || 0), 0) + (audioRef.current?.currentTime || 0);

      // If at the end, restart from beginning
      if (currentGlobalTime >= totalDuration && totalDuration > 0) {
        console.log("[useAudioPlayback Control] Restarting playback.");
        setCurrentTime(0); // Set time to 0
        setCurrentSegmentIndex(0); // This will trigger the effect to load segment 0
      } else {
        console.log("[useAudioPlayback Control] Resuming/Starting playback.");
        const audioElement = audioRef.current;
        const currentSegment = allSegments[currentSegmentIndex];

        if (currentSegment?.audioUrl && audioElement) {
          // If audio exists for the current segment
          if (isAudioReady && audioElement.paused) {
             // If ready and paused, just play
             audioElement.play().catch(e => {
                 console.error("Resume play failed:", e);
                 setIsPlaying(false); // Revert state if play fails
             });
          } else if (!isAudioReady) {
             // If not ready, ensure load is triggered (should already be loading via effect, but belt-and-suspenders)
             console.log("[useAudioPlayback Control] Audio not ready, ensuring load is triggered.");
             loadAudioForSegment(currentSegmentIndex);
             // playWhenReady flag is set, 'canplaythrough' handler will start playback
          }
          // If already playing and ready, do nothing
        } else if (!currentSegment?.audioUrl) {
             // If no audio for current segment, start simulation
             console.log("[useAudioPlayback Control] No audio for current segment, starting simulation.");
             runSimulation(currentSegmentIndex);
        }
      }
    } else {
      // Pause action
      console.log("[useAudioPlayback Control] Pausing playback.");
      playWhenReady.current = false; // Clear intent to play
      internalPauseRef.current = true; // Signal that pause is intentional
      audioRef.current?.pause();
      // Stop simulation if it's running
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      // Reset the internal pause flag shortly after, allowing external pause detection again
      queueMicrotask(() => internalPauseRef.current = false);
    }
  }, [isPlaying, currentSegmentIndex, totalDuration, allSegments, isAudioReady, loadAudioForSegment, runSimulation, setCurrentTime, setCurrentSegmentIndex]);

  const seekAudio = useCallback((newTime: number, targetSegmentIdx: number) => {
    console.log(`[useAudioPlayback Control] Seek requested to time: ${newTime.toFixed(2)}s, target segment index: ${targetSegmentIdx}`);

    // Pause playback immediately during seek
    internalPauseRef.current = true;
    setIsPlaying(false);
    playWhenReady.current = false;
    audioRef.current?.pause();
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    queueMicrotask(() => internalPauseRef.current = false);

    // Set the global time state
    setCurrentTime(newTime);

    // Determine if the segment needs to change
    if (targetSegmentIdx !== currentSegmentIndex) {
        console.log(`[useAudioPlayback Control] Segment change required for seek (${currentSegmentIndex} -> ${targetSegmentIdx}).`);
        // Change segment index, the useEffect will handle loading the new audio/simulation.
        // We need to handle seeking *after* the new audio is loaded.
        setCurrentSegmentIndex(targetSegmentIdx);

        // Add a listener to seek *once* the new audio is ready enough
        const audioElement = audioRef.current;
        if (audioElement) {
            const seekWhenMetadataLoaded = () => {
                const segmentStartTime = allSegments.slice(0, targetSegmentIdx).reduce((sum, s) => sum + (s.duration || 0), 0);
                const timeWithinTargetSegment = Math.max(0, newTime - segmentStartTime);
                try {
                    if (!isNaN(timeWithinTargetSegment) && audioElement.seekable.length > 0) {
                        const seekTime = Math.min(timeWithinTargetSegment, audioElement.duration);
                        console.log(`[useAudioPlayback Control] Seeking audio (after load) to ${seekTime.toFixed(2)} in segment ${targetSegmentIdx + 1}`);
                        audioElement.currentTime = seekTime;
                    } else {
                        console.warn("[useAudioPlayback Control] Audio not ready/seekable or invalid time after load.");
                    }
                } catch (e) {
                    console.error("Error seeking audio after load:", e);
                }
                audioElement.removeEventListener('loadedmetadata', seekWhenMetadataLoaded);
            };
            // Wait for 'loadedmetadata' which usually fires before 'canplaythrough'
            audioElement.addEventListener('loadedmetadata', seekWhenMetadataLoaded);
        }

    } else {
        // Seeking within the *same* segment
        console.log(`[useAudioPlayback Control] Seeking within the same segment (${targetSegmentIdx + 1}).`);
        const audioElement = audioRef.current;
        const targetSegment = allSegments[targetSegmentIdx];
        const targetAudioSrc = targetSegment?.audioUrl ? normalizeUrl(targetSegment.audioUrl) : null;

        if (targetAudioSrc && audioElement) {
            // Calculate the target time within the segment's audio file
            let segmentStartTime = 0;
            for (let i = 0; i < targetSegmentIdx; i++) { segmentStartTime += allSegments[i].duration || 0; }
            const timeWithinTargetSegment = Math.max(0, newTime - segmentStartTime);

            const doSeek = () => {
                 try {
                     // Check if audio is seekable and time is valid
                     if (!isNaN(timeWithinTargetSegment) && audioElement.seekable.length > 0) {
                         // Clamp seek time to the audio duration
                         const seekTime = Math.min(timeWithinTargetSegment, audioElement.duration);
                         console.log(`[useAudioPlayback Control] Seeking audio (same segment) to ${seekTime.toFixed(2)}`);
                         audioElement.currentTime = seekTime;
                     } else { console.warn("[useAudioPlayback Control] Audio not ready/seekable or invalid time for seek."); }
                 } catch (e) { console.error("Error seeking audio:", e); }
            };

            // Check if the audio element is ready enough to seek
            if (audioElement.readyState >= 1) { // HAVE_METADATA or more
                 doSeek();
            } else {
                 // If not ready, wait for metadata to load before seeking
                 console.log("[useAudioPlayback Control] Audio not ready for seek, waiting for loadedmetadata.");
                 audioElement.addEventListener('loadedmetadata', doSeek, { once: true });
                 // Ensure load is triggered if it hasn't been already
                 if(audioElement.networkState === audioElement.NETWORK_NO_SOURCE) {
                     loadAudioForSegment(targetSegmentIdx);
                 }
            }
        } else if (!targetAudioSrc) {
            // No audio, seeking within a simulated segment
            console.log("[useAudioPlayback Control] Seeking within a simulated segment.");
            // Simulation will naturally restart from the correct point
            // because runSimulation uses the current segment index and calculates start time.
            // No explicit action needed here other than setting currentTime.
        }
    }
  }, [allSegments, currentSegmentIndex, normalizeUrl, setCurrentTime, setCurrentSegmentIndex, loadAudioForSegment]);


  return {
    audioRef,
    isPlaying,
    setIsPlaying,
    isAudioReady,
    handlePlayPause,
    seekAudio,
  };
};
