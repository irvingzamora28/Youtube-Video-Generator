import React, { useState, useRef, useEffect, MouseEvent } from 'react';
import { Script, ScriptSegment, Visual } from '../types/script';
import { Rnd } from 'react-rnd';
import { updateProjectScript } from '../services/projectApi';

interface VisualTimelineEditorProps {
  script: Script;
  onScriptUpdate?: (script: Script) => void;
  projectId: number;
  onSegmentSelectForEditor?: (segmentIndex: number) => void;
  scrollToSegmentIndex?: number | null;
}

// Timeline constants
const TIMELINE_HEIGHT = 120;
const SEGMENT_LANE_HEIGHT = 60;
const PIXELS_PER_SECOND_INITIAL = 80;
const MIN_DURATION = 0.1; // Minimum 0.1s duration

// Custom drag/resize types
type DragState = {
  active: boolean;
  type: 'move' | 'resizeLeft' | 'resizeRight' | null;
  segmentIdx: number | null;
  visualIdx: number | null;
  initialMouseX: number;
  initialTimestamp: number;
  initialDuration: number;
  rightEdgePosition: number;
};

const VisualTimelineEditor: React.FC<VisualTimelineEditorProps> = ({ script, onScriptUpdate, projectId, scrollToSegmentIndex }) => {
  const [pixelsPerSecond, setPixelsPerSecond] = useState(PIXELS_PER_SECOND_INITIAL);
  const [editingScript, setEditingScript] = useState<Script>(JSON.parse(JSON.stringify(script)));
  const timelineRef = useRef<HTMLDivElement>(null);
  const timelineContainerRef = useRef<HTMLDivElement>(null);
  
  // Custom drag/resize state
  const dragState = useRef<DragState>({
    active: false,
    type: null,
    segmentIdx: null,
    visualIdx: null,
    initialMouseX: 0,
    initialTimestamp: 0,
    initialDuration: 0,
    rightEdgePosition: 0
  });

  // Scroll to segment when scrollToSegmentIndex changes
  useEffect(() => {
    if (scrollToSegmentIndex == null) return;
    const tryScroll = (attempt = 0) => {
      const segmentLane = document.getElementById(`segment-lane-${scrollToSegmentIndex}`);
      const container = timelineContainerRef.current;
      console.log('[Scroll Effect] attempt', attempt, 'scrollToSegmentIndex:', scrollToSegmentIndex, 'segmentLane:', segmentLane, 'container:', container);
      if (segmentLane && container) {
        const laneRect = segmentLane.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        // Calculate offset relative to the scrollable container
        const scrollLeft = segmentLane.offsetLeft + segmentLane.clientWidth / 2 - container.clientWidth / 2;
        console.log('[Scroll Effect] Scrolling to', scrollLeft);
        container.scrollTo({ left: scrollLeft, behavior: 'smooth' });
      } else if (attempt < 5) {
        // Try again in 50ms (up to 5 times)
        setTimeout(() => tryScroll(attempt + 1), 50);
      } else {
        console.warn('[Scroll Effect] Failed to find segmentLane or container after retries');
      }
    };
    tryScroll();
  }, [scrollToSegmentIndex]);

  // Handle global mouse move and up events for drag operations
  useEffect(() => {
    const handleMouseMove = (e: globalThis.MouseEvent) => {
      if (!dragState.current.active || dragState.current.segmentIdx === null || dragState.current.visualIdx === null) {
        return;
      }

      const containerRect = timelineContainerRef.current?.getBoundingClientRect();
      if (!containerRect) return;

      // Calculate mouse position relative to container
      const mouseXRelative = e.clientX - containerRect.left;
      const deltaX = mouseXRelative - dragState.current.initialMouseX;
      const deltaTime = deltaX / pixelsPerSecond;

      // Get the current visual being manipulated
      const allSegments = editingScript.sections.flatMap(s => s.segments);
      const segment = allSegments[dragState.current.segmentIdx];
      const visual = segment.visuals[dragState.current.visualIdx];

      if (dragState.current.type === 'move') {
        // Moving the entire visual
        let newTimestamp = dragState.current.initialTimestamp + deltaTime;
        
        // Clamp to segment bounds
        newTimestamp = Math.max(0, Math.min(newTimestamp, segment.duration - visual.duration));
        
        // Update visual element position for immediate feedback
        const visualElement = document.getElementById(`visual-${visual.id}`);
        if (visualElement) {
          visualElement.style.left = `${newTimestamp * pixelsPerSecond}px`;
          
          // Update the timestamp text
          const infoElement = visualElement.querySelector('.visual-info');
          if (infoElement) {
            infoElement.textContent = `${newTimestamp.toFixed(1)}s - ${visual.duration.toFixed(1)}s`;
          }
        }
      } 
      else if (dragState.current.type === 'resizeLeft') {
        // Resizing from left edge (changes timestamp and duration)
        const rightEdge = dragState.current.rightEdgePosition;
        
        // Calculate new timestamp based on mouse position
        let newTimestamp = dragState.current.initialTimestamp + deltaTime;
        
        // Clamp to valid range
        newTimestamp = Math.max(0, Math.min(newTimestamp, rightEdge - MIN_DURATION));
        
        // Calculate new duration
        let newDuration = rightEdge - newTimestamp;
        
        // Apply min/max constraints
        newDuration = Math.max(MIN_DURATION, newDuration);
        
        // Update visual element for immediate feedback
        const visualElement = document.getElementById(`visual-${visual.id}`);
        if (visualElement) {
          visualElement.style.left = `${newTimestamp * pixelsPerSecond}px`;
          visualElement.style.width = `${newDuration * pixelsPerSecond}px`;
          
          // Update the info text
          const infoElement = visualElement.querySelector('.visual-info');
          if (infoElement) {
            infoElement.textContent = `${newTimestamp.toFixed(1)}s - ${newDuration.toFixed(1)}s`;
          }
        }
      } 
      else if (dragState.current.type === 'resizeRight') {
        // Resizing from right edge (only changes duration)
        let newDuration = dragState.current.initialDuration + deltaTime;
        
        // Clamp to valid range
        newDuration = Math.max(MIN_DURATION, Math.min(newDuration, segment.duration - visual.timestamp));
        
        // Update visual element for immediate feedback
        const visualElement = document.getElementById(`visual-${visual.id}`);
        if (visualElement) {
          visualElement.style.width = `${newDuration * pixelsPerSecond}px`;
          
          // Update the info text
          const infoElement = visualElement.querySelector('.visual-info');
          if (infoElement) {
            infoElement.textContent = `${visual.timestamp.toFixed(1)}s - ${newDuration.toFixed(1)}s`;
          }
        }
      }
    };

    const handleMouseUp = () => {
      if (!dragState.current.active || dragState.current.segmentIdx === null || dragState.current.visualIdx === null) {
        return;
      }

      // Get the current visual being manipulated
      const allSegments = editingScript.sections.flatMap(s => s.segments);
      const segment = allSegments[dragState.current.segmentIdx];
      const visual = segment.visuals[dragState.current.visualIdx];
      
      // Get the current visual element
      const visualElement = document.getElementById(`visual-${visual.id}`);
      if (!visualElement) {
        dragState.current.active = false;
        return;
      }
      
      // Extract final position and size from the element's style
      const left = parseFloat(visualElement.style.left) / pixelsPerSecond;
      const width = parseFloat(visualElement.style.width) / pixelsPerSecond;
      
      // Apply the changes to the actual state
      setEditingScript(prev => {
        const updated = { ...prev };
        const segments = updated.sections.flatMap(s => s.segments);
        const seg = segments[dragState.current.segmentIdx!];
        const vis = seg.visuals[dragState.current.visualIdx!];
        
        // Round to 1 decimal place for better UX
        vis.timestamp = Math.round(left * 10) / 10;
        vis.duration = Math.round(width * 10) / 10;
        
        return updated;
      });

      // Reset drag state
      dragState.current.active = false;
      dragState.current.type = null;
    };

    // Add global event listeners
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    // Clean up
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [editingScript, pixelsPerSecond]);

  // Zoom handlers
  const handleZoomIn = () => setPixelsPerSecond(p => Math.min(p * 1.25, 500));
  const handleZoomOut = () => setPixelsPerSecond(p => Math.max(p / 1.25, 10));

  // Custom handlers for drag and resize operations
  const startDrag = (e: MouseEvent, segmentIdx: number, visualIdx: number, type: 'move' | 'resizeLeft' | 'resizeRight') => {
    e.preventDefault();
    
    // Get container rect
    const containerRect = timelineContainerRef.current?.getBoundingClientRect();
    if (!containerRect) return;
    
    // Get the current visual
    const allSegments = editingScript.sections.flatMap(s => s.segments);
    const segment = allSegments[segmentIdx];
    const visual = segment.visuals[visualIdx];
    
    // Set the initial state for tracking
    dragState.current = {
      active: true,
      type: type,
      segmentIdx: segmentIdx,
      visualIdx: visualIdx,
      initialMouseX: e.clientX - containerRect.left,
      initialTimestamp: visual.timestamp,
      initialDuration: visual.duration,
      rightEdgePosition: visual.timestamp + visual.duration
    };
    
    // Prevent text selection during drag
    e.stopPropagation();
  };

  // Save to backend
  const handleSave = async () => {
    // Sort visuals in each segment by timestamp before saving
    const newScript = {
      ...editingScript,
      sections: editingScript.sections.map(section => ({
        ...section,
        segments: section.segments.map(segment => ({
          ...segment,
          visuals: [...segment.visuals].sort((a, b) => a.timestamp - b.timestamp)
        }))
      }))
    };
    await updateProjectScript(projectId, newScript);
    if (onScriptUpdate) onScriptUpdate(newScript);
    alert('Timeline changes saved!');
  };

  // Helper: get total timeline duration
  const allSegments = editingScript.sections.flatMap(s => s.segments);
  const totalDuration = editingScript.totalDuration || allSegments.reduce((sum, seg) => sum + (seg.duration || 0), 0);

  return (
    <div className="visual-timeline-editor w-full">
      <div className="timeline-toolbar flex items-center gap-2 p-2 bg-background border-b border-border">
        <button onClick={handleZoomOut} className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded mr-2">-</button>
        <span className="text-base font-semibold mr-2">Zoom</span>
        <button onClick={handleZoomIn} className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-2 px-4 rounded mr-2">+</button>
        <button className="save-btn bg-green-600 hover:bg-green-700 text-white font-semibold px-5 py-2 rounded ml-auto" onClick={handleSave}>Save</button>
      </div>
      <div 
        className="timeline-scroll-area overflow-x-auto overflow-y-hidden border border-border bg-background relative whitespace-nowrap w-full"
        ref={timelineContainerRef}
        style={{
          height: (SEGMENT_LANE_HEIGHT + 46) * allSegments.length + 40,
        }}
      >
        {/* Adaptive Timeline Ruler */}
        <div className="timeline-ruler" style={{ position: 'relative', height: 38, width: totalDuration * pixelsPerSecond, overflow: 'visible' }}>
          {(() => {
            // Calculate adaptive tick interval
            // Target: major ticks ~80px apart, minor ticks ~16-24px apart
            const minMajorPx = 70;
            const minMinorPx = 16;
            // Candidate intervals in seconds (descending for best fit)
            const intervals = [60, 30, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1];
            let majorInterval = 1;
            for (const int of intervals) {
              if (int * pixelsPerSecond >= minMajorPx) {
                majorInterval = int;
                break;
              }
            }
            // Minor interval: divide major by 5 or 2 (whichever gives > minMinorPx)
            let minorInterval = majorInterval / 5;
            if (minorInterval * pixelsPerSecond < minMinorPx) {
              minorInterval = majorInterval / 2;
            }
            if (minorInterval < 0.1) minorInterval = 0; // Don't draw if too small

            const ticks = [];
            for (let t = 0; t <= totalDuration + 0.0001; t += minorInterval || majorInterval) {
              // Improved isMajor logic: label all multiples of majorInterval (with tolerance)
              const isMajor = minorInterval && Math.abs(Math.round(t / majorInterval) * majorInterval - t) < 1e-6;
              ticks.push(
                <div
                  key={t.toFixed(2)}
                  className={isMajor ? 'timeline-tick-major' : 'timeline-tick-minor'}
                  style={{
                    position: 'absolute',
                    left: t * pixelsPerSecond,
                    height: isMajor ? 28 : 13,
                    borderLeft: isMajor ? '2px solid #666' : '1px solid #bbb',
                    color: '#888',
                    fontSize: 11,
                    opacity: isMajor ? 1 : 0.5,
                    zIndex: isMajor ? 2 : 1,
                    background: 'none',
                  }}
                >
                  <span style={{
                    position: 'absolute',
                    top: 30, // place label below the tick
                    left: -8, // center label under tick
                    minWidth: 24,
                    textAlign: 'center',
                    fontWeight: isMajor ? 500 : 400,
                    color: isMajor ? '#222' : '#555',
                    background: isMajor ? 'rgba(255,255,255,0.85)' : 'rgba(255,255,255,0.6)',
                    padding: '0 2px',
                    borderRadius: 2,
                    fontSize: 12,
                    pointerEvents: 'none',
                    zIndex: 10,
                  }}>
                    {(() => {
                      if (t === 0) return '0:00';
                      const mins = Math.floor(t / 60);
                      const secs = t % 60;
                      // Show sub-seconds if needed
                      if (secs % 1 === 0) {
                        // Integer seconds
                        return `${mins}:${secs.toString().padStart(2, '0')}`;
                      } else {
                        // Sub-second
                        return `${mins}:${secs.toFixed(1).padStart(4, '0')}`;
                      }
                    })()}
                  </span>
                </div>
              );
            }
            return ticks;
          })()}
        </div>
        
        {/* Timeline content */}
        <div className="timeline-container" style={{ position: 'relative' }}>
          {allSegments.map((segment, segmentIdx) => {
            const RULER_HEIGHT = 24;
          // Calculate the global start time for snapping
          const segmentStart = segment.startTime;
          const segmentEnd = segment.startTime + segment.duration;
          // Calculate min/max X for segment drag (no overlap)
          let minStart = 0;
          let maxStart = totalDuration - segment.duration;
          if (segmentIdx > 0) {
            minStart = allSegments[segmentIdx - 1].startTime + allSegments[segmentIdx - 1].duration;
          }
          if (segmentIdx < allSegments.length - 1) {
            maxStart = allSegments[segmentIdx + 1].startTime - segment.duration;
          }
            return (
            <div
              id={`segment-lane-${segmentIdx}`}
              style={{
                position: 'absolute',
                left: segment.startTime * pixelsPerSecond,
                top: RULER_HEIGHT + segmentIdx * (SEGMENT_LANE_HEIGHT + 46),
                width: segment.duration * pixelsPerSecond,
                height: SEGMENT_LANE_HEIGHT + 38,
                zIndex: 10,
              }}
              key={segment.id}
            >
              <Rnd
                key={segment.id}
                size={{ width: segment.duration * pixelsPerSecond, height: SEGMENT_LANE_HEIGHT + 38 }}
                position={{ x: 0, y: 0 }}
                bounds="parent"
                minWidth={segment.duration * pixelsPerSecond}
                maxWidth={segment.duration * pixelsPerSecond}
                enableResizing={false}
                dragAxis="x"
                dragGrid={[pixelsPerSecond / 10, SEGMENT_LANE_HEIGHT + 46]}
                cancel=".visual-draggable"
                onDragStop={(_, d) => {
                // Snap to previous/next segment end/start
                let newStart = Math.max(minStart, Math.min(d.x / pixelsPerSecond, maxStart));
                // Snap to grid (0.1s)
                newStart = Math.round(newStart * 10) / 10;
                // Update segment startTime and all visuals
                setEditingScript(prev => {
                  const updated = { ...prev };
                  // Find the segment in the nested structure
                  let segIdx = 0;
                  let found = false;
                  for (const section of updated.sections) {
                    for (let i = 0; i < section.segments.length; i++) {
                      if (section.segments[i].id === segment.id) {
                        segIdx = i;
                        // Calculate the delta
                        const delta = newStart - section.segments[i].startTime;
                        section.segments[i].startTime = newStart;
                        // Move all visuals by delta
                        section.segments[i].visuals = section.segments[i].visuals.map(v => ({
                          ...v,
                          timestamp: Math.max(0, Math.min(v.timestamp + delta, section.segments[i].duration - v.duration))
                        }));
                        found = true;
                        break;
                      }
                    }
                    if (found) break;
                  }
                  return updated;
                });
              }}
              style={{ zIndex: 10, position: 'absolute', transition: 'box-shadow 0.2s', boxShadow: '0 4px 16px #0004', border: '2px solid #4f8cff', borderRadius: 8, background: '#21232b' }}
              >
                {/* Segment Label and Audio Controls */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '2px 8px', background: '#262a36', borderRadius: '8px 8px 0 0' }}>
                  <span style={{ fontWeight: 700, color: '#8fd3ff' }}>Segment {segmentIdx + 1}</span>
                  <span style={{ fontSize: 12, color: '#b3b3b3' }}>{segment.narrationText.slice(0, 120)}...</span>
                  <span style={{ marginLeft: 'auto', fontSize: 12, color: '#aaa' }}>
                    {segment.duration.toFixed(1)}s
                  </span>
                </div>
                
                {/* Timeline visuals for this segment */}
                <div style={{ position: 'relative', height: SEGMENT_LANE_HEIGHT, width: segment.duration * pixelsPerSecond, marginTop: 4 }}>
                  {segment.visuals.map((visual, visualIdx) => (
                    <div
                      id={`visual-${visual.id}`}
                      key={visual.id}
                      className="visual-item"
                      style={{
                        position: 'absolute',
                        left: visual.timestamp * pixelsPerSecond,
                        top: 4,
                        width: visual.duration * pixelsPerSecond,
                        height: SEGMENT_LANE_HEIGHT - 8,
                        background: '#4f8cff',
                        border: '2px solid #2b6cb0',
                        borderRadius: 6,
                        display: 'flex',
                        alignItems: 'center',
                        padding: '0 8px',
                        color: '#fff',
                        opacity: 0.95,
                        boxShadow: '0 2px 6px #0003',
                        cursor: 'pointer',
                        userSelect: 'none',
                        overflow: 'hidden'
                      }}
                      onMouseDown={(e) => {
                        // Determine if clicked on edge or body
                        const rect = e.currentTarget.getBoundingClientRect();
                        const edgeWidth = 10; // Width of the resize handle area
                        
                        if (e.clientX - rect.left <= edgeWidth) {
                          // Left edge resize
                          startDrag(e, segmentIdx, visualIdx, 'resizeLeft');
                        } else if (rect.right - e.clientX <= edgeWidth) {
                          // Right edge resize
                          startDrag(e, segmentIdx, visualIdx, 'resizeRight');
                        } else {
                          // Body drag (move)
                          startDrag(e, segmentIdx, visualIdx, 'move');
                        }
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, width: '100%', height: '100%' }}>
                        {visual.imageUrl && (
                          <img 
                            src={visual.imageUrl} 
                            alt={visual.altText || ''} 
                            style={{ 
                              width: 36, 
                              height: 36, 
                              objectFit: 'cover', 
                              borderRadius: 4, 
                              marginRight: 6, 
                              border: '1px solid #222' 
                            }} 
                          />
                        )}
                        <div>
                          <div style={{ fontWeight: 700 }}>{visual.visualType}</div>
                          <div style={{ fontSize: 10 }}>{visual.description?.slice(0, 28) || ''}</div>
                          <div className="visual-info" style={{ fontSize: 10 }}>
                            {visual.timestamp.toFixed(1)}s - {visual.duration.toFixed(1)}s
                          </div>
                        </div>
                      </div>
                      
                      {/* Custom resize handles with visual indicators */}
                      <div 
                        className="resize-handle resize-left"
                        style={{
                          position: 'absolute',
                          left: 0,
                          top: 0,
                          width: 6,
                          height: '100%',
                          cursor: 'w-resize'
                        }}
                      />
                      <div 
                        className="resize-handle resize-right"
                        style={{
                          position: 'absolute',
                          right: 0,
                          top: 0,
                          width: 6,
                          height: '100%',
                          cursor: 'e-resize'
                        }}
                      />
                    </div>
                  ))}
                </div>
            </Rnd>
            </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default VisualTimelineEditor;