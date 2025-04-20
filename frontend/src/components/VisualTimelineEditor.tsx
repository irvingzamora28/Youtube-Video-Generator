import React, { useState, useRef, useCallback } from 'react';
import { Script, ScriptSegment, Visual } from '../types/script';
import { Rnd } from 'react-rnd';
import { updateProjectScript } from '../services/projectApi';

interface VisualTimelineEditorProps {
  script: Script;
  onScriptUpdate?: (script: Script) => void;
  projectId: number;
}

// Timeline constants
const TIMELINE_HEIGHT = 120;
const SEGMENT_LANE_HEIGHT = 60;
const PIXELS_PER_SECOND_INITIAL = 80;
const MIN_DURATION = 0.1; // Minimum 0.1s duration

const VisualTimelineEditor: React.FC<VisualTimelineEditorProps> = ({ script, onScriptUpdate, projectId }) => {
  const [zoom, setZoom] = useState(1);
  const [pixelsPerSecond, setPixelsPerSecond] = useState(PIXELS_PER_SECOND_INITIAL);
  const [editingScript, setEditingScript] = useState<Script>(JSON.parse(JSON.stringify(script)));
  const timelineRef = useRef<HTMLDivElement>(null);
  
  // Zoom handlers
  const handleZoomIn = () => setPixelsPerSecond(p => Math.min(p * 1.25, 500));
  const handleZoomOut = () => setPixelsPerSecond(p => Math.max(p / 1.25, 10));

  // Drag/resize logic
  const onVisualChange = (segmentIdx: number, visualIdx: number, newTimestamp: number, newDuration: number) => {
    setEditingScript(prev => {
      const updated = { ...prev };
      const seg = updated.sections.flatMap(s => s.segments)[segmentIdx];
      seg.visuals[visualIdx] = {
        ...seg.visuals[visualIdx],
        timestamp: parseFloat(newTimestamp.toFixed(1)),
        duration: Math.max(parseFloat(newDuration.toFixed(1)), MIN_DURATION)
      };
      return updated;
    });
  };

  // Save to backend
  const handleSave = async () => {
    await updateProjectScript(projectId, editingScript);
    if (onScriptUpdate) onScriptUpdate(editingScript);
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
        ref={timelineRef}
        style={{
          height: (SEGMENT_LANE_HEIGHT + 46) * allSegments.length + 40,
        }}
      >
        <div className="timeline-ruler" style={{ position: 'relative', height: 24, width: totalDuration * pixelsPerSecond }}>
          {[...Array(Math.ceil(totalDuration * 10) + 1)].map((_, i) => {
            const t = i / 10;
            return (
              <div
                key={t}
                className="timeline-tick"
                style={{ position: 'absolute', left: t * pixelsPerSecond, height: t % 1 === 0 ? 24 : 12, borderLeft: '1px solid #555', color: '#aaa', fontSize: 10 }}
              >
                {t % 1 === 0 ? <span style={{ position: 'absolute', top: 0, left: 2 }}>{t}s</span> : null}
              </div>
            );
          })}
        </div>
        {/* RULER_HEIGHT ensures segments start below the ruler */}
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
            <Rnd
              key={segment.id}
              size={{ width: segment.duration * pixelsPerSecond, height: SEGMENT_LANE_HEIGHT + 38 }}
              position={{ x: segment.startTime * pixelsPerSecond, y: RULER_HEIGHT + segmentIdx * (SEGMENT_LANE_HEIGHT + 46) }}
              bounds=".timeline-scroll-area"
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
                {segment.visuals.map((visual, visualIdx) => {
                  return (
                    <Rnd
                      key={visual.id}
                      className="visual-draggable"
                      size={{ width: visual.duration * pixelsPerSecond, height: SEGMENT_LANE_HEIGHT - 8 }}
                      position={{ x: visual.timestamp * pixelsPerSecond, y: 4 }}
                      bounds="parent"
                      minWidth={MIN_DURATION * pixelsPerSecond}
                      maxWidth={segment.duration * pixelsPerSecond}
                      enableResizing={{ left: true, right: true, top: false, bottom: false, topLeft: false, topRight: false, bottomLeft: false, bottomRight: false }}
                      onDragStop={(_, d) => {
                        let newTimestamp = Math.max(0, Math.min(d.x / pixelsPerSecond, segment.duration - visual.duration));
                        // Snap to other visuals in segment
                        const snapPoints = [0, ...segment.visuals.filter((v, i) => i !== visualIdx).flatMap(v => [v.timestamp, v.timestamp + v.duration]), segment.duration - visual.duration];
                        const SNAP_THRESHOLD = 0.12;
                        let snapTo = newTimestamp;
                        let minDist = SNAP_THRESHOLD;
                        for (const pt of snapPoints) {
                          const dist = Math.abs(pt - newTimestamp);
                          if (dist < minDist) {
                            minDist = dist;
                            snapTo = pt;
                          }
                        }
                        onVisualChange(segmentIdx, visualIdx, snapTo, visual.duration);
                      }}
                      onResizeStop={(_, dir, ref, delta, pos) => {
                        let newDuration = Math.max(MIN_DURATION, Math.min(ref.offsetWidth / pixelsPerSecond, segment.duration - (visual.timestamp)));
                        let newTimestamp = Math.max(0, Math.min(pos.x / pixelsPerSecond, segment.duration - newDuration));
                        // Snap edges to other visuals or segment bounds
                        const snapPoints = [0, ...segment.visuals.filter((v, i) => i !== visualIdx).flatMap(v => [v.timestamp, v.timestamp + v.duration]), segment.duration];
                        // Snap left
                        let snapLeft = newTimestamp;
                        let minDistLeft = 0.12;
                        for (const pt of snapPoints) {
                          const dist = Math.abs(pt - newTimestamp);
                          if (dist < minDistLeft) {
                            minDistLeft = dist;
                            snapLeft = pt;
                          }
                        }
                        // Snap right
                        let snapRight = newTimestamp + newDuration;
                        let minDistRight = 0.12;
                        for (const pt of snapPoints) {
                          const dist = Math.abs(pt - (newTimestamp + newDuration));
                          if (dist < minDistRight) {
                            minDistRight = dist;
                            snapRight = pt;
                          }
                        }
                        // Adjust duration if snapped
                        if (snapLeft !== newTimestamp) {
                          newDuration += (newTimestamp - snapLeft);
                          newTimestamp = snapLeft;
                        }
                        if (snapRight !== newTimestamp + newDuration) {
                          newDuration = snapRight - newTimestamp;
                        }
                        // Clamp to segment
                        newTimestamp = Math.max(0, Math.min(newTimestamp, segment.duration - newDuration));
                        newDuration = Math.max(MIN_DURATION, Math.min(newDuration, segment.duration - newTimestamp));
                        onVisualChange(segmentIdx, visualIdx, newTimestamp, newDuration);
                      }}
                      dragAxis="x"
                      resizeGrid={[pixelsPerSecond / 10, 0]}
                      dragGrid={[pixelsPerSecond / 10, SEGMENT_LANE_HEIGHT]}
                      style={{ background: '#4f8cff', borderRadius: 6, opacity: 0.95, border: '2px solid #2b6cb0', color: '#fff', display: 'flex', alignItems: 'center', padding: '0 8px', cursor: 'pointer', overflow: 'hidden', boxShadow: '0 2px 6px #0003' }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {visual.imageUrl && <img src={visual.imageUrl} alt={visual.altText || ''} style={{ width: 36, height: 36, objectFit: 'cover', borderRadius: 4, marginRight: 6, border: '1px solid #222' }} />}
                        <div>
                          <div style={{ fontWeight: 700 }}>{visual.visualType}</div>
                          <div style={{ fontSize: 10 }}>{visual.description?.slice(0, 28) || ''}</div>
                          <div style={{ fontSize: 10 }}>
                            {visual.timestamp.toFixed(1)}s - {visual.duration.toFixed(1)}s
                          </div>
                        </div>
                      </div>
                    </Rnd>
                  );
                })}
              </div>
            </Rnd>
          );
        })}
      </div>
    </div>
  );
};

export default VisualTimelineEditor;
