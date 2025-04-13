import { useState } from 'react';
import Layout from '../components/Layout';

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

export default function ScriptGenerator() {
  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [duration, setDuration] = useState('5');
  const [style, setStyle] = useState('educational');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedScript, setGeneratedScript] = useState<Script | null>(null);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    
    // Simulate API call to generate script
    setTimeout(() => {
      const mockScript: Script = {
        id: 'script-' + Date.now(),
        title: `Understanding ${topic}`,
        description: `A comprehensive explanation of ${topic} for ${audience} audiences.`,
        targetAudience: audience,
        sections: [
          {
            id: 'section-1',
            title: 'Introduction',
            content: `Welcome to this video about ${topic}. Today we'll explore the key concepts and applications.`,
            visualNotes: 'Stickman waving and pointing to a title card.',
            duration: 20,
          },
          {
            id: 'section-2',
            title: 'What is ' + topic + '?',
            content: `${topic} is a fascinating subject that involves... [AI-generated explanation would go here]`,
            visualNotes: 'Stickman explaining with thought bubbles and diagrams appearing.',
            duration: 45,
          },
          {
            id: 'section-3',
            title: 'Key Concepts',
            content: 'The most important aspects to understand are... [AI-generated content]',
            visualNotes: 'Stickman pointing to bullet points that appear one by one.',
            duration: 60,
          },
          {
            id: 'section-4',
            title: 'Real-world Applications',
            content: 'In the real world, we see these concepts applied in... [AI-generated examples]',
            visualNotes: 'Stickman demonstrating practical examples with props.',
            duration: 50,
          },
          {
            id: 'section-5',
            title: 'Conclusion',
            content: `That concludes our overview of ${topic}. We've covered the fundamentals and applications.`,
            visualNotes: 'Stickman summarizing with a recap diagram.',
            duration: 25,
          },
        ],
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      
      setGeneratedScript(mockScript);
      setIsGenerating(false);
    }, 3000);
  };

  const handleSectionClick = (sectionId: string) => {
    setActiveSection(activeSection === sectionId ? null : sectionId);
  };

  const handleRegenerateSection = (sectionId: string) => {
    // This would call the AI to regenerate just this section
    console.log('Regenerating section:', sectionId);
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {!generatedScript ? (
          <div className="bg-card shadow rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-bold text-foreground mb-6">Create Video Script</h1>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="topic" className="block text-sm font-medium text-foreground mb-1">
                    What topic would you like to create a video about?
                  </label>
                  <input
                    type="text"
                    id="topic"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="e.g., Quantum Computing, Climate Change, Financial Literacy"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label htmlFor="audience" className="block text-sm font-medium text-foreground mb-1">
                      Target Audience
                    </label>
                    <select
                      id="audience"
                      value={audience}
                      onChange={(e) => setAudience(e.target.value)}
                      className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="beginners">Beginners</option>
                      <option value="general">General Audience</option>
                      <option value="students">Students</option>
                      <option value="professionals">Professionals</option>
                      <option value="experts">Experts</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="duration" className="block text-sm font-medium text-foreground mb-1">
                      Approximate Duration (minutes)
                    </label>
                    <select
                      id="duration"
                      value={duration}
                      onChange={(e) => setDuration(e.target.value)}
                      className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="2">2 minutes</option>
                      <option value="5">5 minutes</option>
                      <option value="10">10 minutes</option>
                      <option value="15">15 minutes</option>
                      <option value="20">20+ minutes</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="style" className="block text-sm font-medium text-foreground mb-1">
                      Presentation Style
                    </label>
                    <select
                      id="style"
                      value={style}
                      onChange={(e) => setStyle(e.target.value)}
                      className="w-full px-4 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    >
                      <option value="educational">Educational</option>
                      <option value="entertaining">Entertaining</option>
                      <option value="professional">Professional</option>
                      <option value="casual">Casual</option>
                      <option value="storytelling">Storytelling</option>
                    </select>
                  </div>
                </div>
                
                <div className="pt-4">
                  <button
                    type="submit"
                    disabled={isGenerating || !topic}
                    className="w-full md:w-auto px-6 py-3 bg-primary text-primary-foreground rounded-md font-medium shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGenerating ? (
                      <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Generating Script...
                      </div>
                    ) : (
                      'Generate Script'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h1 className="text-2xl font-bold text-foreground">{generatedScript.title}</h1>
                    <p className="text-muted-foreground mt-1">{generatedScript.description}</p>
                  </div>
                  <button
                    onClick={() => setGeneratedScript(null)}
                    className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                  >
                    Create New Script
                  </button>
                </div>
                
                <div className="mt-6 flex flex-wrap gap-2">
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Audience: {generatedScript.targetAudience}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Duration: ~{generatedScript.sections.reduce((acc, section) => acc + section.duration, 0) / 60} minutes
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Sections: {generatedScript.sections.length}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <h2 className="text-xl font-semibold text-foreground mb-4">Script Sections</h2>
                
                <div className="space-y-4">
                  {generatedScript.sections.map((section) => (
                    <div key={section.id} className="border border-border rounded-lg overflow-hidden">
                      <div 
                        className={`px-4 py-3 flex justify-between items-center cursor-pointer ${
                          activeSection === section.id ? 'bg-accent/50' : 'bg-card'
                        }`}
                        onClick={() => handleSectionClick(section.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-medium text-foreground">{section.title}</span>
                          <span className="ml-2 text-sm text-muted-foreground">({section.duration}s)</span>
                        </div>
                        <svg 
                          className={`h-5 w-5 text-muted-foreground transition-transform ${
                            activeSection === section.id ? 'transform rotate-180' : ''
                          }`} 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                      
                      {activeSection === section.id && (
                        <div className="px-4 py-3 border-t border-border">
                          <div className="prose prose-sm max-w-none text-foreground">
                            <h4 className="text-sm font-medium text-muted-foreground mb-2">Narration</h4>
                            <div className="p-3 bg-muted/30 rounded-md">
                              <p>{section.content}</p>
                            </div>
                            
                            <h4 className="text-sm font-medium text-muted-foreground mt-4 mb-2">Visual Notes</h4>
                            <div className="p-3 bg-muted/30 rounded-md">
                              <p>{section.visualNotes}</p>
                            </div>
                            
                            <div className="mt-4 flex justify-end space-x-3">
                              <button
                                onClick={() => handleRegenerateSection(section.id)}
                                className="px-3 py-1.5 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90"
                              >
                                Regenerate Section
                              </button>
                              <button
                                className="px-3 py-1.5 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90"
                              >
                                Edit Manually
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="mt-6 flex justify-between">
                  <button
                    className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                  >
                    Regenerate Entire Script
                  </button>
                  <button
                    className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                  >
                    Proceed to Video Creation
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
