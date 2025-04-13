import { useState } from 'react';
import Layout from '../components/Layout';
import { Script, ScriptSection, ScriptSegment, Visual } from '../types/script';
import SegmentEditor from '../components/SegmentEditor';
import SectionRegenerator from '../components/SectionRegenerator';
import ScriptVisualizer from '../components/ScriptVisualizer';
import SegmentTimeline from '../components/SegmentTimeline';

export default function ScriptGenerator() {
  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [duration, setDuration] = useState('5');
  const [style, setStyle] = useState('educational');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedScript, setGeneratedScript] = useState<Script | null>(null);
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null);
  const [activeSegmentId, setActiveSegmentId] = useState<string | null>(null);
  const [showSegmentEditor, setShowSegmentEditor] = useState(false);
  const [showSectionRegenerator, setShowSectionRegenerator] = useState(false);
  const [showScriptVisualizer, setShowScriptVisualizer] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    
    // Simulate API call to generate script
    setTimeout(() => {
      // Create a mock script with sections and segments
      const mockScript: Script = {
        id: 'script-' + Date.now(),
        title: `Understanding ${topic}`,
        description: `A comprehensive explanation of ${topic} for ${audience} audiences.`,
        targetAudience: audience,
        sections: [
          {
            id: 'section-1',
            title: 'Introduction',
            content: `An introduction to ${topic} and why it matters.`,
            segments: [
              {
                id: 'segment-1-1',
                narrationText: `Are you struggling with understanding ${topic}? In this video, we'll break down the key concepts and show you how it all works.`,
                startTime: 0,
                duration: 10,
                visuals: [
                  {
                    id: 'visual-1-1-1',
                    description: `A stickman looking confused with a thought bubble containing a question mark and the text "${topic}?"`,
                    timestamp: 0,
                    duration: 5,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  },
                  {
                    id: 'visual-1-1-2',
                    description: `The stickman brightens up as a lightbulb appears above their head.`,
                    timestamp: 5,
                    duration: 5,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              },
              {
                id: 'segment-1-2',
                narrationText: `${topic} has become increasingly important in today's world. Let's explore why it matters and how it affects our daily lives.`,
                startTime: 10,
                duration: 15,
                visuals: [
                  {
                    id: 'visual-1-2-1',
                    description: `A stickman standing in front of a world map with highlighted areas showing the impact of ${topic}.`,
                    timestamp: 0,
                    duration: 8,
                    visualType: 'image',
                    position: 'full',
                    transition: 'slide',
                  },
                  {
                    id: 'visual-1-2-2',
                    description: `The stickman in daily life scenarios where ${topic} is relevant.`,
                    timestamp: 8,
                    duration: 7,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              }
            ],
            totalDuration: 25,
          },
          {
            id: 'section-2',
            title: `Key Concepts of ${topic}`,
            content: `The fundamental principles and concepts that make up ${topic}.`,
            segments: [
              {
                id: 'segment-2-1',
                narrationText: `Let's start with the basics. At its core, ${topic} consists of several key principles that work together.`,
                startTime: 0,
                duration: 12,
                visuals: [
                  {
                    id: 'visual-2-1-1',
                    description: `A stickman teacher pointing at a blackboard with the title "${topic} Fundamentals".`,
                    timestamp: 0,
                    duration: 12,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              },
              {
                id: 'segment-2-2',
                narrationText: `The first important concept is [concept 1]. This forms the foundation upon which everything else is built.`,
                startTime: 12,
                duration: 15,
                visuals: [
                  {
                    id: 'visual-2-2-1',
                    description: `A stickman building a foundation labeled "[concept 1]".`,
                    timestamp: 0,
                    duration: 8,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  },
                  {
                    id: 'visual-2-2-2',
                    description: `A close-up diagram showing how [concept 1] works.`,
                    timestamp: 8,
                    duration: 7,
                    visualType: 'diagram',
                    position: 'full',
                    transition: 'zoom',
                  }
                ]
              },
              {
                id: 'segment-2-3',
                narrationText: `Next, we have [concept 2], which builds upon [concept 1] and extends its capabilities.`,
                startTime: 27,
                duration: 13,
                visuals: [
                  {
                    id: 'visual-2-3-1',
                    description: `The stickman adding a second level to the structure, labeled "[concept 2]".`,
                    timestamp: 0,
                    duration: 7,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  },
                  {
                    id: 'visual-2-3-2',
                    description: `An animation showing the relationship between [concept 1] and [concept 2].`,
                    timestamp: 7,
                    duration: 6,
                    visualType: 'animation',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              }
            ],
            totalDuration: 40,
          },
          {
            id: 'section-3',
            title: 'Practical Applications',
            content: `How ${topic} is applied in real-world scenarios.`,
            segments: [
              {
                id: 'segment-3-1',
                narrationText: `Now that we understand the theory, let's look at how ${topic} is applied in practice.`,
                startTime: 0,
                duration: 10,
                visuals: [
                  {
                    id: 'visual-3-1-1',
                    description: `A stickman transitioning from a classroom to a workshop environment.`,
                    timestamp: 0,
                    duration: 10,
                    visualType: 'animation',
                    position: 'full',
                    transition: 'slide',
                  }
                ]
              },
              {
                id: 'segment-3-2',
                narrationText: `In industry, ${topic} is used to solve complex problems such as [example 1].`,
                startTime: 10,
                duration: 15,
                visuals: [
                  {
                    id: 'visual-3-2-1',
                    description: `Stickman in an industrial setting working with machinery related to ${topic}.`,
                    timestamp: 0,
                    duration: 8,
                    visualType: 'image',
                    position: 'left',
                    transition: 'fade',
                  },
                  {
                    id: 'visual-3-2-2',
                    description: `A diagram showing how ${topic} solves [example 1].`,
                    timestamp: 8,
                    duration: 7,
                    visualType: 'diagram',
                    position: 'right',
                    transition: 'fade',
                  }
                ]
              },
              {
                id: 'segment-3-3',
                narrationText: `In everyday life, you might encounter ${topic} when [example 2].`,
                startTime: 25,
                duration: 15,
                visuals: [
                  {
                    id: 'visual-3-3-1',
                    description: `Stickman in a daily life scenario encountering ${topic}.`,
                    timestamp: 0,
                    duration: 15,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              }
            ],
            totalDuration: 40,
          },
          {
            id: 'section-4',
            title: 'Conclusion',
            content: `Summary of what we've learned about ${topic} and next steps.`,
            segments: [
              {
                id: 'segment-4-1',
                narrationText: `To summarize, we've explored the key concepts of ${topic}, including [concept 1] and [concept 2].`,
                startTime: 0,
                duration: 12,
                visuals: [
                  {
                    id: 'visual-4-1-1',
                    description: `A stickman standing next to a summary board with bullet points of the key concepts.`,
                    timestamp: 0,
                    duration: 12,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              },
              {
                id: 'segment-4-2',
                narrationText: `We've also seen how ${topic} is applied in both industrial settings and everyday life.`,
                startTime: 12,
                duration: 10,
                visuals: [
                  {
                    id: 'visual-4-2-1',
                    description: `Split screen showing the industrial and everyday applications of ${topic}.`,
                    timestamp: 0,
                    duration: 10,
                    visualType: 'image',
                    position: 'full',
                    transition: 'fade',
                  }
                ]
              },
              {
                id: 'segment-4-3',
                narrationText: `Thank you for watching! If you'd like to learn more about ${topic}, check out the resources in the description below.`,
                startTime: 22,
                duration: 8,
                visuals: [
                  {
                    id: 'visual-4-3-1',
                    description: `A stickman waving goodbye with a speech bubble saying "Thanks for watching!"`,
                    timestamp: 0,
                    duration: 8,
                    visualType: 'image',
                    position: 'center',
                    transition: 'fade',
                  }
                ]
              }
            ],
            totalDuration: 30,
          }
        ],
        createdAt: new Date(),
        updatedAt: new Date(),
        totalDuration: 135, // Sum of all section durations
        status: 'draft',
      };
      
      setGeneratedScript(mockScript);
      setIsGenerating(false);
    }, 3000);
  };

  const handleSectionClick = (sectionId: string) => {
    setActiveSectionId(activeSectionId === sectionId ? null : sectionId);
    setActiveSegmentId(null);
  };

  const handleSegmentClick = (segmentId: string) => {
    setActiveSegmentId(activeSegmentId === segmentId ? null : segmentId);
  };

  const handleEditSegment = (segmentId: string) => {
    setActiveSegmentId(segmentId);
    setShowSegmentEditor(true);
  };

  const handleSaveSegment = (updatedSegment: ScriptSegment) => {
    if (!generatedScript) return;
    
    const updatedScript = { ...generatedScript };
    
    // Find the section containing the segment
    const sectionIndex = updatedScript.sections.findIndex(section => 
      section.segments.some(segment => segment.id === updatedSegment.id)
    );
    
    if (sectionIndex === -1) return;
    
    // Find the segment index
    const segmentIndex = updatedScript.sections[sectionIndex].segments.findIndex(
      segment => segment.id === updatedSegment.id
    );
    
    if (segmentIndex === -1) return;
    
    // Update the segment
    updatedScript.sections[sectionIndex].segments[segmentIndex] = updatedSegment;
    
    // Recalculate section duration
    updatedScript.sections[sectionIndex].totalDuration = updatedScript.sections[sectionIndex].segments.reduce(
      (total, segment) => total + segment.duration, 0
    );
    
    // Recalculate total script duration
    updatedScript.totalDuration = updatedScript.sections.reduce(
      (total, section) => total + section.totalDuration, 0
    );
    
    setGeneratedScript(updatedScript);
    setShowSegmentEditor(false);
  };

  const handleRegenerateSection = (sectionId: string) => {
    setActiveSectionId(sectionId);
    setShowSectionRegenerator(true);
  };

  const handleRegenerateSectionSubmit = (sectionId: string, prompt: string) => {
    // This would call the API to regenerate the section
    console.log(`Regenerating section ${sectionId} with prompt: ${prompt}`);
    setShowSectionRegenerator(false);
  };

  const getActiveSection = () => {
    if (!generatedScript || !activeSectionId) return null;
    return generatedScript.sections.find(section => section.id === activeSectionId) || null;
  };

  const getActiveSegment = () => {
    if (!generatedScript || !activeSegmentId) return null;
    
    for (const section of generatedScript.sections) {
      const segment = section.segments.find(segment => segment.id === activeSegmentId);
      if (segment) return segment;
    }
    
    return null;
  };

  // Format time (seconds) to MM:SS format
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {!generatedScript ? (
          <div className="bg-color-card shadow rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-bold text-color-foreground mb-6">Create Video Script</h1>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="topic" className="block text-sm font-medium text-color-foreground mb-1">
                    What topic would you like to create a video about?
                  </label>
                  <input
                    type="text"
                    id="topic"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="w-full px-4 py-2 border border-color-border rounded-md bg-color-background text-color-foreground focus:outline-none focus:ring-2 focus:ring-color-primary"
                    placeholder="e.g., Quantum Computing, Climate Change, Financial Literacy"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label htmlFor="audience" className="block text-sm font-medium text-color-foreground mb-1">
                      Target Audience
                    </label>
                    <select
                      id="audience"
                      value={audience}
                      onChange={(e) => setAudience(e.target.value)}
                      className="w-full px-4 py-2 border border-color-border rounded-md bg-color-background text-color-foreground focus:outline-none focus:ring-2 focus:ring-color-primary"
                    >
                      <option value="beginners">Beginners</option>
                      <option value="general">General Audience</option>
                      <option value="students">Students</option>
                      <option value="professionals">Professionals</option>
                      <option value="experts">Experts</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="duration" className="block text-sm font-medium text-color-foreground mb-1">
                      Approximate Duration (minutes)
                    </label>
                    <select
                      id="duration"
                      value={duration}
                      onChange={(e) => setDuration(e.target.value)}
                      className="w-full px-4 py-2 border border-color-border rounded-md bg-color-background text-color-foreground focus:outline-none focus:ring-2 focus:ring-color-primary"
                    >
                      <option value="2">2 minutes</option>
                      <option value="5">5 minutes</option>
                      <option value="10">10 minutes</option>
                      <option value="15">15 minutes</option>
                      <option value="20">20+ minutes</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="style" className="block text-sm font-medium text-color-foreground mb-1">
                      Presentation Style
                    </label>
                    <select
                      id="style"
                      value={style}
                      onChange={(e) => setStyle(e.target.value)}
                      className="w-full px-4 py-2 border border-color-border rounded-md bg-color-background text-color-foreground focus:outline-none focus:ring-2 focus:ring-color-primary"
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
                    className="w-full md:w-auto px-6 py-3 bg-color-primary text-color-primary-foreground rounded-md font-medium shadow-sm hover:bg-color-primary/90 focus:outline-none focus:ring-2 focus:ring-color-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGenerating ? (
                      <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-color-primary-foreground" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
            <div className="bg-color-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h1 className="text-2xl font-bold text-color-foreground">{generatedScript.title}</h1>
                    <p className="text-color-muted-foreground mt-1">{generatedScript.description}</p>
                  </div>
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setShowScriptVisualizer(true)}
                      className="px-4 py-2 bg-color-primary text-color-primary-foreground rounded-md text-sm font-medium hover:bg-color-primary/90"
                    >
                      Preview
                    </button>
                    <button
                      onClick={() => setGeneratedScript(null)}
                      className="px-4 py-2 bg-color-secondary text-color-secondary-foreground rounded-md text-sm font-medium hover:bg-color-secondary/90"
                    >
                      Create New Script
                    </button>
                  </div>
                </div>
                
                <div className="mt-6 flex flex-wrap gap-2">
                  <div className="px-3 py-1 bg-color-muted rounded-full text-sm text-color-muted-foreground">
                    Audience: {generatedScript.targetAudience}
                  </div>
                  <div className="px-3 py-1 bg-color-muted rounded-full text-sm text-color-muted-foreground">
                    Duration: {formatTime(generatedScript.totalDuration)}
                  </div>
                  <div className="px-3 py-1 bg-color-muted rounded-full text-sm text-color-muted-foreground">
                    Sections: {generatedScript.sections.length}
                  </div>
                  <div className="px-3 py-1 bg-color-muted rounded-full text-sm text-color-muted-foreground">
                    Status: {generatedScript.status.replace('_', ' ')}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="bg-color-card shadow rounded-lg overflow-hidden">
              <div className="px-4 py-5 sm:p-6">
                <h2 className="text-xl font-semibold text-color-foreground mb-4">Script Sections</h2>
                
                <div className="space-y-4">
                  {generatedScript.sections.map((section) => (
                    <div key={section.id} className="border border-color-border rounded-lg overflow-hidden">
                      <div 
                        className={`px-4 py-3 flex justify-between items-center cursor-pointer ${
                          activeSectionId === section.id ? 'bg-color-accent/50' : 'bg-color-card'
                        }`}
                        onClick={() => handleSectionClick(section.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-medium text-color-foreground">{section.title}</span>
                          <span className="ml-2 text-sm text-color-muted-foreground">({formatTime(section.totalDuration)})</span>
                        </div>
                        <svg 
                          className={`h-5 w-5 text-color-muted-foreground transition-transform ${
                            activeSectionId === section.id ? 'transform rotate-180' : ''
                          }`} 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                      
                      {activeSectionId === section.id && (
                        <div className="px-4 py-3 border-t border-color-border">
                          <div className="prose prose-sm max-w-none text-color-foreground">
                            <h4 className="text-sm font-medium text-color-muted-foreground mb-2">Overview</h4>
                            <div className="p-3 bg-color-muted/30 rounded-md mb-4">
                              <p>{section.content}</p>
                            </div>
                            
                            {/* Section timeline */}
                            <SegmentTimeline 
                              section={section}
                              onSegmentSelect={handleSegmentClick}
                              selectedSegmentId={activeSegmentId}
                            />
                            
                            {/* Segments */}
                            <h4 className="text-sm font-medium text-color-muted-foreground mt-4 mb-2">Segments</h4>
                            <div className="space-y-3">
                              {section.segments.map((segment) => (
                                <div 
                                  key={segment.id} 
                                  className={`p-3 border rounded-md ${
                                    activeSegmentId === segment.id ? 'border-color-primary bg-color-primary/5' : 'border-color-border'
                                  }`}
                                  onClick={() => handleSegmentClick(segment.id)}
                                >
                                  <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-color-foreground">
                                        {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
                                      </span>
                                      <span className="ml-2 text-xs text-color-muted-foreground">
                                        ({segment.duration}s)
                                      </span>
                                    </div>
                                    <div className="text-xs text-color-muted-foreground">
                                      {segment.visuals.length} visual{segment.visuals.length !== 1 ? 's' : ''}
                                    </div>
                                  </div>
                                  
                                  <p className="text-sm text-color-foreground mb-2">{segment.narrationText}</p>
                                  
                                  {activeSegmentId === segment.id && (
                                    <div className="mt-3">
                                      <h5 className="text-xs font-medium text-color-muted-foreground mb-2">Visuals</h5>
                                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                                        {segment.visuals.map((visual) => (
                                          <div key={visual.id} className="p-2 border border-color-border rounded-md bg-color-muted/10">
                                            <div className="text-xs text-color-muted-foreground mb-1">
                                              {formatTime(segment.startTime + visual.timestamp)} ({visual.duration}s)
                                            </div>
                                            <p className="text-xs text-color-foreground">{visual.description}</p>
                                          </div>
                                        ))}
                                      </div>
                                      
                                      <div className="flex justify-end mt-3 space-x-2">
                                        <button
                                          onClick={() => handleEditSegment(segment.id)}
                                          className="px-3 py-1 bg-color-secondary text-color-secondary-foreground text-xs rounded-md hover:bg-color-secondary/90"
                                        >
                                          Edit Segment
                                        </button>
                                      </div>
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                            
                            <div className="mt-4 flex justify-end space-x-3">
                              <button
                                onClick={() => handleRegenerateSection(section.id)}
                                className="px-3 py-1.5 bg-color-secondary text-color-secondary-foreground text-sm rounded-md hover:bg-color-secondary/90"
                              >
                                Regenerate Section
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
                    className="px-4 py-2 bg-color-secondary text-color-secondary-foreground rounded-md text-sm font-medium hover:bg-color-secondary/90"
                    onClick={() => {
                      // This would call the API to regenerate the entire script
                      console.log('Regenerating entire script');
                    }}
                  >
                    Regenerate Entire Script
                  </button>
                  <button
                    className="px-4 py-2 bg-color-primary text-color-primary-foreground rounded-md text-sm font-medium hover:bg-color-primary/90"
                    onClick={() => {
                      // This would proceed to the video creation step
                      console.log('Proceeding to video creation');
                    }}
                  >
                    Proceed to Video Creation
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Segment Editor Modal */}
      {showSegmentEditor && getActiveSegment() && (
        <SegmentEditor
          segment={getActiveSegment()!}
          onSave={handleSaveSegment}
          onCancel={() => setShowSegmentEditor(false)}
        />
      )}
      
      {/* Section Regenerator Modal */}
      {showSectionRegenerator && getActiveSection() && (
        <SectionRegenerator
          section={getActiveSection()!}
          onRegenerate={handleRegenerateSectionSubmit}
          onCancel={() => setShowSectionRegenerator(false)}
        />
      )}
      
      {/* Script Visualizer Modal */}
      {showScriptVisualizer && generatedScript && (
        <ScriptVisualizer
          script={generatedScript}
          onClose={() => setShowScriptVisualizer(false)}
        />
      )}
    </Layout>
  );
}
