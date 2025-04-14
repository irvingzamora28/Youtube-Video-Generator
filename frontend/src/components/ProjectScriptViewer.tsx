import React from 'react';
import { Script, ScriptSection, ScriptSegment } from '../types/script';

type ProjectScriptViewerProps = {
  script: Script;
};

const ProjectScriptViewer: React.FC<ProjectScriptViewerProps> = ({ script }) => {
  // Format time in MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <div className="space-y-6">
        {script.sections.map((section, sectionIndex) => (
          <div key={section.id} className="border border-border rounded-lg overflow-hidden">
            <div className="bg-muted/30 px-4 py-3 flex justify-between items-center">
              <h3 className="font-medium text-foreground">
                {sectionIndex + 1}. {section.title}
              </h3>
              <span className="text-xs text-muted-foreground">
                Duration: {formatTime(section.totalDuration || 0)}
              </span>
            </div>
            
            <div className="p-4 space-y-4">
              {section.segments.map((segment, segmentIndex) => (
                <div key={segment.id} className="border border-border rounded-lg p-3">
                  <div className="flex justify-between mb-2">
                    <span className="text-xs text-muted-foreground">
                      Segment {sectionIndex + 1}.{segmentIndex + 1}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
                      {' '}({segment.duration}s)
                    </span>
                  </div>
                  
                  <p className="text-sm text-foreground mb-3">{segment.narrationText}</p>
                  
                  {segment.visuals.length > 0 && (
                    <div>
                      <h4 className="text-xs font-medium text-muted-foreground mb-2">
                        Visuals ({segment.visuals.length})
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {segment.visuals.map((visual) => (
                          <div key={visual.id} className="border border-border rounded p-2 bg-muted/10">
                            <div className="flex justify-between mb-1">
                              <span className="text-xs text-muted-foreground">
                                {formatTime(segment.startTime + visual.timestamp)}
                              </span>
                              <span className="text-xs text-muted-foreground">
                                {visual.duration}s
                              </span>
                            </div>
                            <p className="text-xs text-foreground">{visual.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectScriptViewer;
