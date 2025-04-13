import { useState } from 'react';

type ScriptSection = {
  id: string;
  title: string;
  content: string;
  visualNotes: string;
  duration: number;
};

type ScriptSectionEditorProps = {
  section: ScriptSection;
  onSave: (updatedSection: ScriptSection) => void;
  onCancel: () => void;
};

export default function ScriptSectionEditor({ section, onSave, onCancel }: ScriptSectionEditorProps) {
  const [title, setTitle] = useState(section.title);
  const [content, setContent] = useState(section.content);
  const [visualNotes, setVisualNotes] = useState(section.visualNotes);
  const [duration, setDuration] = useState(section.duration);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...section,
      title,
      content,
      visualNotes,
      duration,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-border">
          <h2 className="text-xl font-semibold text-foreground">Edit Section</h2>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6">
          <div className="space-y-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-foreground mb-1">
                Section Title
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>
            
            <div>
              <label htmlFor="content" className="block text-sm font-medium text-foreground mb-1">
                Narration Content
              </label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                rows={6}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>
            
            <div>
              <label htmlFor="visualNotes" className="block text-sm font-medium text-foreground mb-1">
                Visual Notes
              </label>
              <textarea
                id="visualNotes"
                value={visualNotes}
                onChange={(e) => setVisualNotes(e.target.value)}
                rows={4}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
              <p className="mt-1 text-sm text-muted-foreground">
                Describe what should be shown visually during this section (stickman actions, diagrams, etc.)
              </p>
            </div>
            
            <div>
              <label htmlFor="duration" className="block text-sm font-medium text-foreground mb-1">
                Duration (seconds)
              </label>
              <input
                type="number"
                id="duration"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                min={5}
                max={300}
                className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                required
              />
            </div>
            
            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-border text-foreground rounded-md hover:bg-muted/30"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
              >
                Save Changes
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
