import { useState } from 'react';
import Layout from '../components/Layout';
import { Script, ScriptSection, ScriptSegment, Visual } from '../types/script';
import SegmentEditor from '../components/SegmentEditor';
import SectionRegenerator from '../components/SectionRegenerator';
import ScriptVisualizer from '../components/ScriptVisualizer';
import SegmentTimeline from '../components/SegmentTimeline';
import { generateScript } from '../services/api';

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

    try {
      // Call the API to generate the script
      const durationMinutes = parseFloat(duration);
      const script = await generateScript(topic, audience, durationMinutes, style);
      setGeneratedScript(script);
    } catch (error) {
      console.error('Error generating script:', error);
      alert('Failed to generate script. Please try again.');
    } finally {
      setIsGenerating(false);
    }
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
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setShowScriptVisualizer(true)}
                      className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
                    >
                      Preview
                    </button>
                    <button
                      onClick={() => setGeneratedScript(null)}
                      className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                    >
                      Create New Script
                    </button>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-2">
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Audience: {generatedScript.targetAudience}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Duration: {formatTime(generatedScript.totalDuration)}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Sections: {generatedScript.sections.length}
                  </div>
                  <div className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
                    Status: {generatedScript.status.replace('_', ' ')}
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
                          activeSectionId === section.id ? 'bg-accent/50' : 'bg-card'
                        }`}
                        onClick={() => handleSectionClick(section.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-medium text-foreground">{section.title}</span>
                          <span className="ml-2 text-sm text-muted-foreground">({formatTime(section.totalDuration)})</span>
                        </div>
                        <svg
                          className={`h-5 w-5 text-muted-foreground transition-transform ${
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
                        <div className="px-4 py-3 border-t border-border">
                          <div className="prose prose-sm max-w-none text-foreground">
                            <h4 className="text-sm font-medium text-muted-foreground mb-2">Overview</h4>
                            <div className="p-3 bg-muted/30 rounded-md mb-4">
                              <p>{section.content}</p>
                            </div>

                            {/* Section timeline */}
                            <SegmentTimeline
                              section={section}
                              onSegmentSelect={handleSegmentClick}
                              selectedSegmentId={activeSegmentId}
                            />

                            {/* Segments */}
                            <h4 className="text-sm font-medium text-muted-foreground mt-4 mb-2">Segments</h4>
                            <div className="space-y-3">
                              {section.segments.map((segment) => (
                                <div
                                  key={segment.id}
                                  className={`p-3 border rounded-md ${
                                    activeSegmentId === segment.id ? 'border-primary bg-primary/5' : 'border-border'
                                  }`}
                                  onClick={() => handleSegmentClick(segment.id)}
                                >
                                  <div className="flex justify-between items-start mb-2">
                                    <div className="flex items-center">
                                      <span className="text-sm font-medium text-foreground">
                                        {formatTime(segment.startTime)} - {formatTime(segment.startTime + segment.duration)}
                                      </span>
                                      <span className="ml-2 text-xs text-muted-foreground">
                                        ({segment.duration}s)
                                      </span>
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                      {segment.visuals.length} visual{segment.visuals.length !== 1 ? 's' : ''}
                                    </div>
                                  </div>

                                  <p className="text-sm text-foreground mb-2">{segment.narrationText}</p>

                                  {activeSegmentId === segment.id && (
                                    <div className="mt-3">
                                      <h5 className="text-xs font-medium text-muted-foreground mb-2">Visuals</h5>
                                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                                        {segment.visuals.map((visual) => (
                                          <div key={visual.id} className="p-2 border border-border rounded-md bg-muted/10">
                                            <div className="text-xs text-muted-foreground mb-1">
                                              {formatTime(segment.startTime + visual.timestamp)} ({visual.duration}s)
                                            </div>
                                            <p className="text-xs text-foreground">{visual.description}</p>
                                          </div>
                                        ))}
                                      </div>

                                      <div className="flex justify-end mt-3 space-x-2">
                                        <button
                                          onClick={() => handleEditSegment(segment.id)}
                                          className="px-3 py-1 bg-secondary text-secondary-foreground text-xs rounded-md hover:bg-secondary/90"
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
                                className="px-3 py-1.5 bg-secondary text-secondary-foreground text-sm rounded-md hover:bg-secondary/90"
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
                    className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/90"
                    onClick={() => {
                      // This would call the API to regenerate the entire script
                      console.log('Regenerating entire script');
                    }}
                  >
                    Regenerate Entire Script
                  </button>
                  <button
                    className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
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
