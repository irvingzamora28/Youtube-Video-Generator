import { useState } from 'react';

type ScriptSection = {
  id: string;
  title: string;
  content: string;
  visualNotes: string;
  duration: number;
};

type SectionRegeneratorProps = {
  section: ScriptSection;
  onRegenerate: (sectionId: string, prompt: string) => void;
  onCancel: () => void;
};

export default function SectionRegenerator({ section, onRegenerate, onCancel }: SectionRegeneratorProps) {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      onRegenerate(section.id, prompt);
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-color-card rounded-lg shadow-xl w-full max-w-2xl">
        <div className="px-6 py-4 border-b border-color-border">
          <h2 className="text-xl font-semibold text-color-foreground">Regenerate Section</h2>
        </div>
        
        <div className="p-6">
          <div className="mb-6">
            <h3 className="text-lg font-medium text-color-foreground mb-2">Current Section: {section.title}</h3>
            <div className="p-3 bg-color-muted/30 rounded-md text-color-foreground text-sm">
              <p>{section.content}</p>
            </div>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="prompt" className="block text-sm font-medium text-color-foreground mb-1">
                Provide instructions for regenerating this section
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
                className="w-full px-4 py-2 border border-color-border rounded-md bg-color-background text-color-foreground focus:outline-none focus:ring-2 focus:ring-color-primary"
                placeholder="e.g., Make it more engaging, simplify the explanation, add more technical details, etc."
                required
              />
              <p className="mt-1 text-sm text-color-muted-foreground">
                The AI will use your instructions to create a new version of this section while maintaining context with the rest of the script.
              </p>
            </div>
            
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-color-border text-color-foreground rounded-md hover:bg-color-muted/30"
                disabled={isLoading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-color-primary text-color-primary-foreground rounded-md hover:bg-color-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={isLoading || !prompt.trim()}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-color-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
