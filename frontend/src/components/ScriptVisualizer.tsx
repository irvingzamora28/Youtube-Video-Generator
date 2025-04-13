import { useState } from 'react';

type ScriptSection = {
  id: string;
  title: string;
  content: string;
  visualNotes: string;
  duration: number;
};

type Script = {
  id: string;
  title: string;
  description: string;
  targetAudience: string;
  sections: ScriptSection[];
  createdAt: Date;
  updatedAt: Date;
};

type ScriptVisualizerProps = {
  script: Script;
  onClose: () => void;
};

export default function ScriptVisualizer({ script, onClose }: ScriptVisualizerProps) {
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  
  const currentSection = script.sections[currentSectionIndex];
  
  const goToNextSection = () => {
    if (currentSectionIndex < script.sections.length - 1) {
      setCurrentSectionIndex(currentSectionIndex + 1);
    }
  };
  
  const goToPreviousSection = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(currentSectionIndex - 1);
    }
  };

  // Generate a simple stickman visualization based on the section
  const getStickmanVisualization = (section: ScriptSection) => {
    // This would be replaced with actual visualization logic
    // For now, we'll return a placeholder SVG
    return (
      <div className="flex items-center justify-center h-64 bg-color-muted/20 rounded-lg">
        <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          {/* Head */}
          <circle cx="60" cy="30" r="15" stroke="currentColor" strokeWidth="2" />
          
          {/* Body */}
          <line x1="60" y1="45" x2="60" y2="85" stroke="currentColor" strokeWidth="2" />
          
          {/* Arms */}
          <line x1="60" y1="60" x2="30" y2="50" stroke="currentColor" strokeWidth="2" />
          <line x1="60" y1="60" x2="90" y2="50" stroke="currentColor" strokeWidth="2" />
          
          {/* Legs */}
          <line x1="60" y1="85" x2="40" y2="115" stroke="currentColor" strokeWidth="2" />
          <line x1="60" y1="85" x2="80" y2="115" stroke="currentColor" strokeWidth="2" />
          
          {/* Speech bubble */}
          <path d="M95 20C95 14.4772 99.4772 10 105 10H115C120.523 10 125 14.4772 125 20V30C125 35.5228 120.523 40 115 40H110L105 50L100 40H95C89.4772 40 85 35.5228 85 30V20Z" transform="translate(-30 -5) scale(0.8)" stroke="currentColor" strokeWidth="2" />
        </svg>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-color-card rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-color-border flex justify-between items-center">
          <h2 className="text-xl font-semibold text-color-foreground">Script Preview</h2>
          <button
            onClick={onClose}
            className="text-color-muted-foreground hover:text-color-foreground"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-color-foreground">
              {currentSectionIndex + 1}. {currentSection.title}
            </h3>
            <div className="text-sm text-color-muted-foreground">
              Duration: {currentSection.duration}s
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-color-muted-foreground mb-2">Visual Preview</h4>
              {getStickmanVisualization(currentSection)}
              <div className="mt-2 text-sm text-color-muted-foreground">
                <p>{currentSection.visualNotes}</p>
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-color-muted-foreground mb-2">Narration</h4>
              <div className="p-4 bg-color-muted/20 rounded-lg h-64 overflow-y-auto">
                <p className="text-color-foreground">{currentSection.content}</p>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-between items-center">
            <button
              onClick={goToPreviousSection}
              disabled={currentSectionIndex === 0}
              className="px-4 py-2 bg-color-secondary text-color-secondary-foreground rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous Section
            </button>
            
            <div className="text-sm text-color-muted-foreground">
              Section {currentSectionIndex + 1} of {script.sections.length}
            </div>
            
            <button
              onClick={goToNextSection}
              disabled={currentSectionIndex === script.sections.length - 1}
              className="px-4 py-2 bg-color-secondary text-color-secondary-foreground rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next Section
            </button>
          </div>
          
          <div className="mt-6 pt-6 border-t border-color-border">
            <button
              onClick={onClose}
              className="w-full px-4 py-2 bg-color-primary text-color-primary-foreground rounded-md"
            >
              Close Preview
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
