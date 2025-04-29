import { useState, useRef, useEffect } from 'react';
import { ScriptSection } from '../types/script';

type SectionRegeneratorProps = {
  section: ScriptSection;
  sections: ScriptSection[];
  inspiration: string;
  onRegenerate: (sectionId: string, regeneratedSection: ScriptSection) => void;
  onCancel: () => void;
};

export default function SectionRegenerator({ section, sections, inspiration, onRegenerate, onCancel }: SectionRegeneratorProps) {
  console.log('SectionRegenerator received section:', section);
  console.log('Section segments:', section.segments);
  if (section.segments && section.segments.length > 0) {
    console.log('First segment narration:', section.segments[0].narrationText);
  }

  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // Focus the textarea when the component mounts and handle escape key
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }

    // Add event listener for the Escape key
    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onCancel();
      }
    };

    document.addEventListener('keydown', handleEscapeKey);

    // Clean up the event listener when the component unmounts
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [onCancel]);

  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Make API call to regenerate the section
      const response = await fetch('/api/regenerate_section', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sectionId: section.id,
          sections: sections,
          inspiration: inspiration,
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to regenerate section');
      }
      const data = await response.json();
      // Assume backend returns the regenerated section as 'regeneratedSection'
      onRegenerate(section.id, data.regeneratedSection);
    } catch (error) {
      alert('Error regenerating section: ' + (error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };


  // Handle clicks outside the modal
  const handleOutsideClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onCancel();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
      onClick={handleOutsideClick}
    >
      <div
        ref={modalRef}
        className="bg-card rounded-lg shadow-xl w-full max-w-2xl border border-border"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-border">
          <h2 className="text-xl font-semibold text-foreground">Regenerate Section</h2>
        </div>

        <div className="p-6">
          <div className="mb-6">
            <h3 className="text-lg font-medium text-foreground mb-2">Current Section: {section.title}</h3>
            <div className="p-3 bg-muted/30 rounded-md text-foreground text-sm">
              <p>{section.content}</p>
              <div className="mt-2 text-xs text-muted-foreground">
                {section.segments.length} segments, {formatTime(section.totalDuration)} total
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="prompt" className="block text-sm font-medium text-foreground mb-1">
                Provide instructions for regenerating this section
              </label>
              <textarea
                id="prompt"
                ref={textareaRef}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g., Make it more engaging, simplify the explanation, add more technical details, etc."
                required
              />
              <p className="mt-1 text-sm text-muted-foreground">
                The AI will use your instructions to create a new version of this section while maintaining context with the rest of the script.
              </p>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-border text-foreground rounded-md hover:bg-muted/30"
                disabled={isLoading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={isLoading || !prompt.trim()}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Regenerating...
                  </div>
                ) : (
                  'Regenerate Section'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
