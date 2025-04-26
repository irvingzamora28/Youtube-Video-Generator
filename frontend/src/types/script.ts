// Types for the script generation and editing

export type Visual = {
  /**
   * If true, remove the background from the image and use the project's background image during video generation.
   */
  removeBackground?: boolean;
  /**
   * Method to use for background removal. 'color' or 'rembg'. Defaults to 'color'.
   */
  removeBackgroundMethod?: 'color' | 'rembg';
  id: string;
  description: string; // Description for image generation
  timestamp: number; // Specific timestamp within the segment (in seconds)
  duration: number; // How long this visual should be displayed (in seconds)
  imageUrl?: string; // URL to the generated image once created
  altText?: string; // Accessibility description
  visualType: 'image' | 'animation' | 'diagram' | 'text'; // Type of visual
  visualStyle?: string; // Style guidance for the visual
  position?: 'left' | 'right' | 'center' | 'full'; // Position on screen
  zoomLevel?: number; // For zoom effects
  transition?: 'fade' | 'slide' | 'zoom' | 'none'; // Transition to next visual
  assetId?: number; // Optional: ID linking to the Asset table record
  referenceText?: string; // Optional: Text that references the narrationText
};

export type ScriptSegment = {
  id: string;
  narrationText: string; // Chunk of narration
  startTime: number; // In seconds from the beginning of the section
  duration: number; // In seconds
  visuals: Visual[]; // Multiple visuals can be associated with a segment
  audioUrl?: string; // Optional: URL to the generated audio for narration
  audioAssetId?: number; // Optional: ID linking to the Asset table record for audio
};

export type ScriptSection = {
  id: string;
  title: string; // e.g., "Introduction"
  content: string; // Overview/summary of the section
  segments: ScriptSegment[];
  totalDuration: number; // Sum of all segment durations
};

export type Script = {
  id: string;
  title: string;
  description: string;
  targetAudience: string;
  sections: ScriptSection[];
  createdAt: Date;
  updatedAt: Date;
  totalDuration: number; // Total duration in seconds
  status: 'draft' | 'complete' | 'in_progress';
  visualStyle?: string;
  style?: string;
  background_image?: string; // Optional background image path
  inspiration?: string; // Optional inspiration text
};
