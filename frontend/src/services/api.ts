import { Script, Visual, ScriptSegment } from '../types/script'; // Add ScriptSegment import

// Use backend URL from env or fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate an image description for a visual, using script, narration, and selected text as context
 */
export async function generateImageDescription({
  script,
  narration,
  selectedText,
}: {
  script: string;
  narration: string;
  selectedText: string;
}): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/image/generate-description`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ script, narration, selected_text: selectedText }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to generate image description';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  const data = await response.json();
  return data.description;
}

/**
 * Generate a script using the backend API
 */
export async function generateScript(
  topic: string,
  targetAudience: string,
  durationMinutes: number,
  visualStyle: string,
  style: string
): Promise<Script> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/script/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        topic,
        target_audience: targetAudience,
        duration_minutes: durationMinutes,
        style: style,
        visual_style: visualStyle,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate script');
    }

    const data = await response.json();
    return transformScriptFromApi(data.script);
  } catch (error) {
    console.error('Error generating script:', error);
    throw error;
  }
}

/**
 * Transform the script from the API format to the frontend format
 */
export function transformScriptFromApi(apiScript: any): Script {
  console.log('Transforming API script:', apiScript);

  // Handle the case where apiScript might be null or undefined
  if (!apiScript) {
    console.log('API script is null or undefined, returning default script');
    return {
      id: '0',
      title: '',
      description: '',
      targetAudience: '',
      sections: [],
      totalDuration: 0,
      status: 'draft',
      visualStyle: '',
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }

  // Check if the content field contains the actual script
  if (apiScript.content && typeof apiScript.content === 'object' && apiScript.content.sections) {
    console.log('Found script in content field, using that instead');
    apiScript = apiScript.content;
  }

  console.log('Sections in API script:', apiScript.sections);

  // Convert the API script format to the frontend script format
  return {
    id: apiScript.id || 0,
    title: apiScript.title || '',
    description: apiScript.description || '',
    targetAudience: apiScript.target_audience || '',
    visualStyle: apiScript.visual_style || apiScript.content?.visual_style || '',
    sections: (apiScript.sections || []).map((section: any) => {
      return {
        id: section.id || `section-${Math.random().toString(36).substring(2, 11)}`,
        title: section.title || '',
        content: section.content || '',
        segments: (section.segments || []).map((segment: any) => {
          console.log('Processing segment in transform:', segment);
          console.log('Segment narration_text:', segment.narration_text);
          return {
            id: segment.id || `segment-${Math.random().toString(36).substring(2, 11)}`,
            narrationText: segment.narration_text || segment.narrationText || '',
            startTime: segment.start_time || segment.startTime || 0, // Check both cases
            duration: segment.duration || 0,
            audioUrl: segment.audioUrl || '', // Add audioUrl mapping
            audioAssetId: segment.audioAssetId, // Add audioAssetId mapping
            visuals: (segment.visuals || []).map((visual: any) => ({
              id: visual.id || `visual-${Math.random().toString(36).substring(2, 11)}`,
              description: visual.description || '',
              timestamp: visual.timestamp || 0,
              duration: visual.duration || 0,
              imageUrl: visual.imageUrl || visual.image_url || '', // Use camelCase first, fallback to snake_case
              assetId: visual.assetId, // Add assetId mapping
              altText: visual.altText || visual.alt_text || '',
              visualType: visual.visualType || visual.visual_type || 'image',
              visualStyle: visual.visualStyle || visual.visual_style || '',
              position: visual.position || '',
              zoomLevel: visual.zoomLevel || visual.zoom_level || 1,
              transition: visual.transition || '',
            }))
          };
        }),
        totalDuration: section.total_duration || 0,
      };
    }),
    createdAt: apiScript.created_at ? new Date(apiScript.created_at) : new Date(),
    updatedAt: apiScript.updated_at ? new Date(apiScript.updated_at) : new Date(),
    totalDuration: apiScript.total_duration || 0,
    status: apiScript.status || 'draft',
  };
}

/**
 * Generate an image based on a description
 */
export async function generateImage(description: string, model?: string): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/image/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: description,
        model,
        aspect_ratio: '16:9'
      }),
    });

    if (!response.ok) {
      try {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate image');
      } catch (parseError) {
        // If we can't parse the error as JSON, use the status text
        throw new Error(`Failed to generate image: ${response.status} ${response.statusText}`);
      }
    }

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || 'Failed to generate image');
    }

    // Return the base64 image data
    return `data:${data.mime_type};base64,${data.image_data}`;
  } catch (error) {
    console.error('Error generating image:', error);
    throw error;
  }
}

/**
 * Generate an image for a visual
 */
export async function generateImageForVisual(visual: Visual): Promise<string> {
  // Create a prompt that includes all the relevant information from the visual
  const prompt = `Generate a ${visual.visualType} of: ${visual.description}.
  Style: ${visual.visualStyle || 'simple, clear, educational'}.`;

  return generateImage(prompt);
}

// Use backend URL from env or fallback

export async function saveImageAsset({
  projectId,
  segmentId,
  visualId,
  timestamp,
  duration,
  imageData,
  description = "",
}: {
  projectId: number;
  segmentId: string;
  visualId: string;
  timestamp: number;
  duration: number;
  imageData: string;
  description?: string;
}) {
  // Send data as JSON instead of FormData
  // Ensure keys match the Pydantic model fields in the backend
  const payload = {
    project_id: projectId, // Matches backend model field name
    segment_id: segmentId, // Matches backend model field name
    visual_id: visualId,   // Matches backend model field name
    timestamp: timestamp,
    duration: duration,
    image_data: imageData, // Matches backend model field name
    description: description,
  };

  const response = await fetch(`${API_BASE_URL}/api/image/save`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json', // Set content type to JSON
    },
    body: JSON.stringify(payload), // Send JSON stringified payload
  });

  if (!response.ok) {
    // Try to parse error details from the response
    let errorDetail = "Failed to save image asset";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {
      // Ignore JSON parsing error if response is not JSON
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

/**
 * Generate audio for a specific segment
 */
export async function generateSegmentAudio({
  projectId,
  segmentId,
}: {
  projectId: number;
  segmentId: string;
}) {
  const payload = {
    project_id: projectId,
    segment_id: segmentId,
  };

  const response = await fetch(`${API_BASE_URL}/api/audio/generate_segment_audio`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = "Failed to generate segment audio";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  return response.json(); // Returns GenerateAudioResponse structure
}

/**
 * Trigger background audio generation for all segments in a project
 */
export async function generateAllProjectAudio(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/audio/generate_all_project_audio/${projectId}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json', // Content-Type might not be strictly needed for POST without body, but good practice
    },
    // No body needed for this request
  });

  if (!response.ok) {
    let errorDetail = "Failed to trigger bulk audio generation";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  return response.json(); // Returns { message: "..." }
}

/**
 * Trigger background visual timing organization for all segments in a project
 */
export async function organizeAllProjectVisuals(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/script/organize_all_visuals/${projectId}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    // No body needed
  });

  if (!response.ok) {
    let errorDetail = "Failed to trigger bulk visual organization";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  return response.json(); // Returns { message: "..." }
}

/**
 * Organize visuals within a segment using the backend LLM
 */
export async function organizeSegmentVisuals(segment: ScriptSegment): Promise<{ organized_segment: ScriptSegment }> {
  const payload = { segment }; // Send the whole segment object

  const response = await fetch(`${API_BASE_URL}/api/script/organize_visuals`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = "Failed to organize visuals";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  return response.json(); // Returns { organized_segment: ScriptSegment }
}

/**
 * Trigger background image generation for all visuals in a project
 */
export async function generateAllProjectImages(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/image/generate_all_project_images/${projectId}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    // No body needed
  });

  if (!response.ok) {
    let errorDetail = "Failed to trigger bulk image generation";
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) { /* Ignore JSON parsing error */ }
    throw new Error(errorDetail);
  }
  return response.json(); // Returns { message: "..." }
}
