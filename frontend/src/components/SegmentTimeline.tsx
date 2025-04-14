import { ScriptSection } from '../types/script';

type SegmentTimelineProps = {
  section: ScriptSection;
  onSegmentSelect: (segmentId: string) => void;
  selectedSegmentId: string | null;
};

export default function SegmentTimeline({ section, onSegmentSelect, selectedSegmentId }: SegmentTimelineProps) {
  // Calculate the total duration for scaling
  const totalDuration = section.totalDuration;

  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="mt-4">
      <h3 className="text-sm font-medium text-muted-foreground mb-2">Timeline</h3>

      {/* Timeline ruler */}
      <div className="relative h-8 mb-1 flex">
        {/* Time markers */}
        {Array.from({ length: Math.ceil(totalDuration / 15) + 1 }).map((_, i) => (
          <div key={i} className="absolute" style={{ left: `${(i * 15 / totalDuration) * 100}%` }}>
            <div className="h-2 border-l border-border"></div>
            <div className="text-xs text-muted-foreground">{formatTime(i * 15)}</div>
          </div>
        ))}
      </div>

      {/* Segments timeline */}
      <div className="relative h-16 bg-muted/20 rounded-md mb-4">
        {section.segments.map((segment) => {
          const segmentWidth = (segment.duration / totalDuration) * 100;
          const segmentLeft = (segment.startTime / totalDuration) * 100;

          return (
            <div
              key={segment.id}
              className={`absolute h-full rounded-md cursor-pointer transition-all hover:brightness-90 flex flex-col items-center justify-start overflow-hidden ${
                selectedSegmentId === segment.id
                  ? 'ring-2 ring-primary ring-offset-1'
                  : 'border border-border'
              }`}
              style={{
                left: `${segmentLeft}%`,
                width: `${segmentWidth}%`,
                backgroundColor: selectedSegmentId === segment.id ? 'var(--primary/20)' : 'var(--card)',
              }}
              onClick={() => onSegmentSelect(segment.id)}
            >
              <div className="text-xs truncate px-2 py-1 w-full text-foreground">
                {segment.narrationText.substring(0, 20)}...
              </div>

              <div className="text-[10px] text-muted-foreground px-2 w-full">
                {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
              </div>

              {/* Visual indicators with labels */}
              <div className="absolute bottom-0 left-0 right-0 h-6 flex">
                {segment.visuals.map((visual) => {
                  const visualWidth = (visual.duration / segment.duration) * 100;
                  const visualLeft = (visual.timestamp / segment.duration) * 100;
                  const visualType = visual.visualType.charAt(0).toUpperCase();

                  return (
                    <div
                      key={visual.id}
                      className={`absolute h-full flex items-center justify-center ${
                        visual.visualType === 'image' ? 'bg-blue-500/60' :
                        visual.visualType === 'animation' ? 'bg-green-500/60' :
                        visual.visualType === 'diagram' ? 'bg-purple-500/60' : 'bg-orange-500/60'
                      }`}
                      style={{
                        left: `${visualLeft}%`,
                        width: `${visualWidth}%`,
                        minWidth: '12px'
                      }}
                      title={`${visual.description} (${formatTime(segment.startTime + visual.timestamp)} - ${formatTime(segment.startTime + visual.timestamp + visual.duration)})`}
                    >
                      <span className="text-[9px] text-white font-bold">{visualType}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected segment details */}
      {selectedSegmentId && (
        <div className="bg-muted/10 p-3 rounded-md">
          <div className="text-sm text-foreground">
            {section.segments.find(s => s.id === selectedSegmentId)?.narrationText}
          </div>
        </div>
      )}
    </div>
  );
}
