import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Script, ScriptSegment, Visual } from '../types/script';

type VisualTimelineProps = {
  script: Script;
};

const VisualTimeline: React.FC<VisualTimelineProps> = ({ script }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);
  const [currentVisualIndex, setCurrentVisualIndex] = useState(0);
  const [isAudioReady, setIsAudioReady] = useState(false); // Track if audio element is ready to play

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const timelineRef = useRef<HTMLDivElement>(null);
  const animationFrameRef = useRef<number | null>(null);
  const playWhenReady = useRef(false); // Flag to play audio once loaded and isPlaying is true
  const internalPauseRef = useRef(false); // Ref to track if the component initiated the pause
  const isSeekingRef = useRef(false); // Ref to track if user is currently seeking via timeline click

  const allSegments = script.sections.flatMap(section => section.segments);
  const totalDuration = script.totalDuration || allSegments.reduce((sum, seg) => sum + (seg.duration || 0), 0);

  const normalizeUrl = (path?: string) => path && path !== '' && !path.startsWith('/static/') ? `/static/${path}` : path || '';

  // --- Simulation Logic ---
  const runSimulation = useCallback((segmentIndex: number) => {
    if (segmentIndex >= allSegments.length || !isPlaying) return;

    const segment = allSegments[segmentIndex];
    const segmentDuration = segment.duration || 1;
    console.log(`[Timeline] Simulating segment ${segmentIndex + 1} duration ${segmentDuration}s`);

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

      if (currentGlobalTime < segmentStartTime + segmentDuration && currentGlobalTime < totalDuration) {
        setCurrentTime(currentGlobalTime);
        animationFrameRef.current = requestAnimationFrame(step);
      } else {
        const nextIndex = segmentIndex + 1;
        if (nextIndex < allSegments.length) {
          setCurrentSegmentIndex(nextIndex);
        } else {
          setIsPlaying(false);
          setCurrentTime(totalDuration);
          console.log("[Timeline] Simulated playback finished.");
        }
      }
    };
    setCurrentTime(segmentStartTime);
    animationFrameRef.current = requestAnimationFrame(step);

  }, [allSegments, isPlaying, totalDuration]);

  // --- Audio Loading Logic ---
  const loadAudioForSegment = useCallback((segmentIndex: number) => {
    if (segmentIndex >= allSegments.length) return;

    const segment = allSegments[segmentIndex];
    const audioSrc = segment?.audioUrl ? normalizeUrl(segment.audioUrl) : null;
    const audioElement = audioRef.current;

    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }

    if (audioSrc && audioElement) {
      const currentFullSrc = audioElement.currentSrc;
      const targetFullSrc = new URL(audioSrc, window.location.origin).href;
      if (currentFullSrc !== targetFullSrc) {
        console.log(`[Timeline] Loading segment ${segmentIndex + 1} audio: ${audioSrc}`);
        setIsAudioReady(false);
        playWhenReady.current = isPlaying;
        audioElement.src = audioSrc;
        audioElement.load();
      } else {
        setIsAudioReady(audioElement.readyState >= 3); // HAVE_FUTURE_DATA
        if (isPlaying && audioElement.paused && isAudioReady) {
             console.log("[Timeline] Resuming play on same source (already loaded).");
             audioElement.play().catch(e => console.error("Error resuming play:", e));
        }
      }
    } else {
      setIsAudioReady(false);
      if (isPlaying) {
        runSimulation(segmentIndex);
      } else {
         audioElement?.pause();
      }
    }
  }, [allSegments, isPlaying, runSimulation, isAudioReady]); // Added isAudioReady


  // --- Effect to load audio when segment index changes ---
   useEffect(() => {
       console.log(`[Timeline Effect] Segment index changed to ${currentSegmentIndex}. Loading audio/starting sim.`);
       loadAudioForSegment(currentSegmentIndex);
   }, [currentSegmentIndex, loadAudioForSegment]);


  // --- Effect for Audio Element Event Listeners ---
  useEffect(() => {
    const audioElement = audioRef.current;
    if (!audioElement) return;

    const handleCanPlayThrough = () => {
      console.log(`[Timeline Event] canplaythrough for segment ${currentSegmentIndex + 1}`);
      setIsAudioReady(true);
      if (playWhenReady.current && isPlaying) {
        playWhenReady.current = false;
        console.log("[Timeline Event] Attempting play after canplaythrough");
        audioElement.play().catch(e => {
          console.error("Audio play failed after canplaythrough:", e);
          setIsPlaying(false);
        });
      }
    };

    const handleAudioEnd = () => {
      console.log(`[Timeline Event] ended for segment ${currentSegmentIndex + 1}`);
      const nextIndex = currentSegmentIndex + 1;
      if (nextIndex < allSegments.length && isPlaying) {
        setCurrentSegmentIndex(nextIndex);
      } else {
        setIsPlaying(false);
        if (nextIndex >= allSegments.length) {
          setCurrentTime(totalDuration);
          console.log("[Timeline Event] Audio playback finished naturally.");
        }
      }
    };

    const handleTimeUpdate = () => {
      if (isPlaying && !audioElement.seeking && !isSeekingRef.current) {
        let elapsedGlobal = 0;
        for (let i = 0; i < currentSegmentIndex; i++) {
          elapsedGlobal += allSegments[i].duration || 0;
        }
        const newTime = Math.min(elapsedGlobal + audioElement.currentTime, totalDuration);
        setCurrentTime(prevTime => Math.abs(newTime - prevTime) > 0.05 ? newTime : prevTime);
      }
    };

    const handleError = (e: Event) => {
      console.error(`[Timeline Event] Error loading audio source ${audioElement.src}:`, e);
      setIsPlaying(false);
      setIsAudioReady(false);
      playWhenReady.current = false;
    };

     const handlePause = () => {
        if (!internalPauseRef.current && isPlaying) {
            console.log("[Timeline Event] Playback paused externally or unexpectedly. Setting isPlaying=false.");
            setIsPlaying(false);
        }
    }

    const handleLoadedMetadata = () => {
        console.log(`[Event] loadedmetadata for segment ${currentSegmentIndex + 1}`);
        setIsAudioReady(audioElement.readyState >= 1); // HAVE_METADATA or more
    }

    // Add listeners
    audioElement.addEventListener('canplaythrough', handleCanPlayThrough);
    audioElement.addEventListener('ended', handleAudioEnd);
    audioElement.addEventListener('timeupdate', handleTimeUpdate);
    audioElement.addEventListener('error', handleError);
    audioElement.addEventListener('pause', handlePause);
    audioElement.addEventListener('loadedmetadata', handleLoadedMetadata);

    // Cleanup function
    return () => {
      audioElement.removeEventListener('canplaythrough', handleCanPlayThrough);
      audioElement.removeEventListener('ended', handleAudioEnd);
      audioElement.removeEventListener('timeupdate', handleTimeUpdate);
      audioElement.removeEventListener('error', handleError);
      audioElement.removeEventListener('pause', handlePause);
      audioElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
    };
  }, [currentSegmentIndex, allSegments, totalDuration, isPlaying, currentTime]); // Added currentTime


  // --- Effect to update current visual based on time ---
  useEffect(() => {
    let elapsed = 0;
    let currentSegIdx = -1;
    let currentVisIdx = -1;
    let found = false;

    for (let i = 0; i < allSegments.length; i++) {
      const segment = allSegments[i];
      const segmentDuration = segment.duration || 0;
      const segmentStartTime = elapsed;
      const segmentEndTime = elapsed + segmentDuration;
      const isLastSegment = i === allSegments.length - 1;

      if (currentTime >= segmentStartTime && (currentTime < segmentEndTime || (isLastSegment && currentTime <= segmentEndTime + 0.01))) {
        currentSegIdx = i;
        const timeWithinSegment = currentTime - segmentStartTime;
        let bestMatchIdx = -1;
        for (let j = segment.visuals.length - 1; j >= 0; j--) {
          const visual = segment.visuals[j];
          const visualTimestamp = visual.timestamp ?? 0;
          if (timeWithinSegment >= visualTimestamp) {
            bestMatchIdx = j;
            break;
          }
        }
        currentVisIdx = bestMatchIdx >= 0 ? bestMatchIdx : (segment.visuals.length > 0 ? 0 : -1);
        found = true;
        break;
      }
      elapsed += segmentDuration;
    }

     if (currentTime === 0 && allSegments.length > 0 && allSegments[0].visuals.length > 0) {
         currentSegIdx = 0;
         currentVisIdx = 0;
         found = true;
     }

    if (found) {
        if (currentSegIdx !== currentSegmentIndex) setCurrentSegmentIndex(currentSegIdx);
        if (currentVisIdx !== -1 && currentVisIdx !== currentVisualIndex) setCurrentVisualIndex(currentVisIdx);
    } else if (currentTime >= totalDuration && allSegments.length > 0) {
         const lastSegIdx = allSegments.length - 1;
         const lastVisIdx = allSegments[lastSegIdx].visuals.length - 1;
         if (currentSegmentIndex !== lastSegIdx) setCurrentSegmentIndex(lastSegIdx);
         if (lastVisIdx >= 0 && currentVisualIndex !== lastVisIdx) setCurrentVisualIndex(lastVisIdx);
    }

  }, [currentTime, allSegments, currentSegmentIndex, currentVisualIndex]);


  // --- UI Event Handlers ---
  const handlePlayPause = () => {
    const targetIsPlaying = !isPlaying;
    setIsPlaying(targetIsPlaying); // Set state first

    if (targetIsPlaying) {
      playWhenReady.current = true; // Set intent to play
      if (currentTime >= totalDuration && totalDuration > 0) {
        console.log("[Timeline Control] Restarting playback.");
        setCurrentTime(0);
        setCurrentSegmentIndex(0); // Triggers effect to load segment 0
      } else {
        console.log("[Timeline Control] Resuming/Starting playback.");
        const audioElement = audioRef.current;
        // If audio is ready, play. Otherwise, the 'canplaythrough' listener will handle it.
        if (audioElement && isAudioReady && audioElement.paused) {
             audioElement.play().catch(e => console.error("Resume play failed:", e));
        } else if (!allSegments[currentSegmentIndex]?.audioUrl) {
             // If no audio for current segment, start simulation
             runSimulation(currentSegmentIndex);
        } else if (audioElement && !isAudioReady) {
             // If audio exists but isn't ready, ensure load is triggered
             loadAudioForSegment(currentSegmentIndex);
        }
      }
    } else {
      // Pause
      console.log("[Timeline Control] Pausing playback.");
      playWhenReady.current = false; // Clear intent
      internalPauseRef.current = true;
      audioRef.current?.pause();
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      queueMicrotask(() => internalPauseRef.current = false);
    }
  };

  const handleTimelineClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current || totalDuration <= 0) return;

    // Pause playback immediately
    internalPauseRef.current = true;
    setIsPlaying(false);
    playWhenReady.current = false;
    audioRef.current?.pause();
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    queueMicrotask(() => internalPauseRef.current = false);

    // Calculate new time
    const timelineRect = timelineRef.current.getBoundingClientRect();
    const clickX = event.clientX - timelineRect.left;
    const clickRatio = Math.max(0, Math.min(1, clickX / timelineRect.width));
    const newTime = clickRatio * totalDuration;

    // Find the segment index for the clicked time
    let elapsed = 0;
    let targetSegmentIdx = 0;
    for (let i = 0; i < allSegments.length; i++) {
      const segmentDuration = allSegments[i].duration || 0;
      if (newTime < elapsed + segmentDuration || i === allSegments.length - 1) {
        targetSegmentIdx = i;
        break;
      }
      elapsed += segmentDuration;
    }

    console.log(`[Timeline Control] Seek to time: ${newTime.toFixed(2)}s, segment index: ${targetSegmentIdx}`);
    setCurrentTime(newTime); // Set time first

    // If segment index changed, useEffect will handle loading.
    // If same segment, manually seek if audio exists.
    if (targetSegmentIdx === currentSegmentIndex) {
        const audioElement = audioRef.current;
        const targetSegment = allSegments[targetSegmentIdx];
        const targetAudioSrc = targetSegment?.audioUrl ? normalizeUrl(targetSegment.audioUrl) : null;

        if (targetAudioSrc && audioElement) {
            let segmentStartTime = 0;
            for (let i = 0; i < targetSegmentIdx; i++) { segmentStartTime += allSegments[i].duration || 0; }
            const timeWithinTargetSegment = Math.max(0, newTime - segmentStartTime);

            const doSeek = () => {
                 try {
                     if (!isNaN(timeWithinTargetSegment) && audioElement.seekable.length > 0) {
                         const seekTime = Math.min(timeWithinTargetSegment, audioElement.duration);
                         console.log(`[Timeline Control] Seeking audio to ${seekTime.toFixed(2)}`);
                         audioElement.currentTime = seekTime;
                     } else { console.warn("[Timeline Control] Audio not ready/seekable or invalid time."); }
                 } catch (e) { console.error("Error seeking audio:", e); }
            };

            const currentFullSrc = audioElement.currentSrc;
            const targetFullSrc = new URL(targetAudioSrc, window.location.origin).href;
            if(currentFullSrc === targetFullSrc) {
                 if (audioElement.readyState >= 1) { doSeek(); } // HAVE_METADATA
                 else { audioElement.addEventListener('loadedmetadata', doSeek, { once: true }); }
            } else {
                 console.log("[Timeline Control] Src mismatch on seek, loading required.");
                 loadAudioForSegment(targetSegmentIdx);
                 const seekWhenReady = () => {
                     doSeek();
                     audioElement.removeEventListener('loadedmetadata', seekWhenReady);
                 };
                 audioElement.addEventListener('loadedmetadata', seekWhenReady);
            }
        }
    } else {
         setCurrentSegmentIndex(targetSegmentIdx); // Trigger useEffect to load
    }
  };


  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Calculate current visual's details
  const currentSegment = allSegments[currentSegmentIndex];
  const currentVisual = currentSegment?.visuals[currentVisualIndex];

  return (
    <div className="space-y-4">
       {/* Audio Element (Hidden) */}
       <audio ref={audioRef} />

       {/* Visual Preview Area */}
       <div className="aspect-video bg-muted rounded-lg flex items-center justify-center text-muted-foreground overflow-hidden relative border border-border">
         {currentVisual?.imageUrl ? (
           <img
             src={normalizeUrl(currentVisual.imageUrl)}
             alt={currentVisual.description}
             className="max-w-full max-h-full object-contain"
           />
         ) : (
           <span>{currentVisual?.description || 'Select a point on the timeline'}</span>
         )}
         {currentVisual?.visualType === 'text' && (
            <div className="absolute inset-0 flex items-center justify-center p-8 bg-black/50">
                <p className="text-white text-2xl text-center">{currentVisual.description}</p>
            </div>
         )}
       </div>

       {/* Timeline Controls */}
       <div className="flex items-center gap-4">
         <button
           onClick={handlePlayPause}
           className="p-2 bg-primary text-primary-foreground rounded-full hover:bg-primary/90"
         >
           {isPlaying ? (
             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
               <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
             </svg>
           ) : (
             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
               <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
             </svg>
           )}
         </button>
         <div className="text-sm font-mono text-muted-foreground">
           {formatTime(currentTime)} / {formatTime(totalDuration)}
         </div>
         <div
            ref={timelineRef}
            className="flex-grow h-2 bg-muted rounded-full cursor-pointer relative"
            onClick={handleTimelineClick}
          >
            <div
              className="absolute top-0 left-0 h-full bg-primary rounded-full"
              style={{ width: `${totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0}%` }}
            />
             <div
              className="absolute top-1/2 left-0 h-4 w-4 bg-primary rounded-full border-2 border-background -translate-y-1/2 -translate-x-1/2"
              style={{ left: `${totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0}%` }}
            />
          </div>
       </div>

       {/* Detailed Timeline View */}
       <div className="relative h-24 bg-muted/20 rounded-md border border-border overflow-hidden">
         {allSegments.map((segment, segIdx) => {
           const segmentDuration = segment.duration || 0.1;
           const segmentWidth = totalDuration > 0 ? (segmentDuration / totalDuration) * 100 : 0;
           const segmentLeft = totalDuration > 0 ? (allSegments.slice(0, segIdx).reduce((sum, s) => sum + (s.duration || 0), 0) / totalDuration) * 100 : 0;
           const timeWithinSegmentForVisuals = currentSegmentIndex === segIdx ? currentTime - allSegments.slice(0, segIdx).reduce((sum, s) => sum + (s.duration || 0), 0) : -1;

           return (
             <div
               key={segment.id}
               className={`absolute h-full border-r border-border/50 ${segIdx === currentSegmentIndex ? 'bg-primary/10' : ''}`}
               style={{ left: `${segmentLeft}%`, width: `${segmentWidth}%` }}
               title={`Segment ${segIdx + 1}: ${segment.narrationText.substring(0, 50)}...`}
             >
               {segment.visuals.map((visual) => {
                 const visualDuration = Math.max(visual.duration, 0.1);
                 const segmentEffectiveDuration = Math.max(segmentDuration, 0.1);
                 const visualWidth = segmentEffectiveDuration > 0 ? (visualDuration / segmentEffectiveDuration) * 100 : 0;
                 const visualLeft = segmentEffectiveDuration > 0 ? ((visual.timestamp || 0) / segmentEffectiveDuration) * 100 : 0;
                 const isActiveVisual = segIdx === currentSegmentIndex && timeWithinSegmentForVisuals >= (visual.timestamp || 0) && timeWithinSegmentForVisuals < (visual.timestamp || 0) + visual.duration;

                 return (
                   <div
                     key={visual.id}
                     className={`absolute bottom-0 h-1/2 ${isActiveVisual ? 'ring-1 ring-primary' : ''} ${
                        visual.visualType === 'image' ? 'bg-blue-500/50' :
                        visual.visualType === 'animation' ? 'bg-green-500/50' :
                        visual.visualType === 'diagram' ? 'bg-purple-500/50' : 'bg-orange-500/50'
                      }`}
                     style={{ left: `${visualLeft}%`, width: `${visualWidth}%` }}
                     title={`${visual.description} (${formatTime(segment.startTime + (visual.timestamp || 0))} - ${formatTime(segment.startTime + (visual.timestamp || 0) + visual.duration)})`}
                   />
                 );
               })}
                <div className="absolute top-1 left-1 text-[10px] text-muted-foreground bg-background/50 px-1 rounded">
                    Seg {segIdx + 1}
                </div>
             </div>
           );
         })}
         <div
            className="absolute top-0 bottom-0 w-0.5 bg-destructive z-10"
            style={{ left: `${totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0}%` }}
          />
       </div>
    </div>
  );
};

export default VisualTimeline;
