import { Script, Visual, ScriptSegment } from '../types/script'; // Add ScriptSegment import

// Use backend URL from env or fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Generate all visuals for a segment based on narration text using the backend endpoint.
 */
export async function generateVisualsForSegment({ projectId, segmentId, narrationText }: { projectId: number; segmentId: string; narrationText: string; }): Promise<{ visuals: any[]; assets: any[] }> {
  const response = await fetch(`${API_BASE_URL}/api/image/generate_visuals_for_segment`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: projectId, segment_id: segmentId, narration_text: narrationText }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to generate visuals for segment';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  return response.json();
}

/**
 * Trigger bulk visuals generation for all segments in the short script (short_content field, 9:16 aspect ratio)
 * @param projectId Project ID
 * @returns {Promise<{ visuals: any[]; assets: any[]; errors: any[] }>}
 */
export async function generateAllShortProjectVisuals(projectId: number): Promise<{ visuals: any[]; assets: any[]; errors: any[] }> {
  const response = await fetch(`${API_BASE_URL}/api/image/generate_all_project_visuals/${projectId}?field=short_content&aspect_ratio=9:16`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    let errorDetail = 'Failed to generate visuals for short script';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  return response.json();
}


/**
 * Preview background removal for an image and optional background.
 * Returns a base64 PNG string.
 */
/**
 * Preview background removal for an image and optional background.
 * Returns a base64 PNG string.
 * Accepts an optional removeBackgroundMethod ('color' or 'rembg').
 */
export async function previewBackgroundRemoval({ imageUrl, backgroundUrl, removeBackgroundMethod, projectId }: { imageUrl: string; backgroundUrl?: string; removeBackgroundMethod?: string; projectId?: number }): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/bg_removal/preview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      image_url: imageUrl,
      background_url: backgroundUrl,
      removeBackgroundMethod: removeBackgroundMethod,
      project_id: projectId
    }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to preview background removal';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  const data = await response.json();
  return data.base64_png;
}


/**
 * Generate an image description for a visual, using script, narration, and selected text as context
 */
/**
 * Start video generation for a project (asynchronous, main script)
 */
export async function generateVideo(projectId: number): Promise<{ status: string; task_id: string }> {
  const response = await fetch(`${API_BASE_URL}/api/video/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: projectId, field: 'content' }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to start video generation';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  return response.json();
}

/**
 * Start video generation for a project (short script)
 */
export async function generateShortVideo(projectId: number): Promise<{ status: string; task_id: string }> {
  const response = await fetch(`${API_BASE_URL}/api/video/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id: projectId, field: 'short_content' }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to start short video generation';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  return response.json();
}

/**
 * Poll video generation status by task ID
 */
export async function getVideoStatus(taskId: string): Promise<{ status: string; video_url?: string; error?: string }> {
  const response = await fetch(`${API_BASE_URL}/api/video/status/${taskId}`);
  if (!response.ok) {
    let errorDetail = 'Failed to get video status';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  return response.json();
}

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
 * Parse a pasted JSON into a script using the backend API
 */
export async function parseScriptJson({ jsonStr, topic, targetAudience, durationMinutes, style, visualStyle, inspiration }: {
  jsonStr: string;
  topic: string;
  targetAudience: string;
  durationMinutes: number;
  style: string;
  visualStyle: string;
  inspiration?: string;
}): Promise<Script> {
  const response = await fetch(`${API_BASE_URL}/api/script/parse_json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      json_str: jsonStr,
      topic,
      target_audience: targetAudience,
      duration_minutes: durationMinutes,
      style,
      visual_style: visualStyle,
      inspiration
    }),
  });
  if (!response.ok) {
    let errorDetail = 'Failed to parse script JSON';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {}
    throw new Error(errorDetail);
  }
  const data = await response.json();
  return data.script;
}

/**
 * Generate a script using the backend API
 */
export async function generateScript(
  topic: string,
  targetAudience: string,
  durationMinutes: number,
  visualStyle: string,
  style: string,
  inspiration: string
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
        inspiration: inspiration,
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
 * Generate a short script (59s) for a project using the backend API
 */
export async function generateShortScript(
  projectId: number,
  topic: string,
  targetAudience: string,
  style: string,
  visualStyle: string,
  inspiration: string
): Promise<Script> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/script/generate_short`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        project_id: projectId,
        topic,
        target_audience: targetAudience,
        style,
        visual_style: visualStyle,
        inspiration,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate short script');
    }

    const data = await response.json();
    return transformScriptFromApi(data.script);
  } catch (error) {
    console.error('Error generating short script:', error);
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
      inspiration: '',
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
    inspiration: apiScript.inspiration || apiScript.content?.inspiration || '',
    totalDuration: apiScript.total_duration || 0,
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
            wordTimings: segment.word_timings || segment.wordTimings || [],
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
              removeBackground: typeof visual.removeBackground !== 'undefined' ? visual.removeBackground : (typeof visual.remove_background !== 'undefined' ? visual.remove_background : false),
              removeBackgroundMethod: visual.removeBackgroundMethod || visual.remove_background_method || 'color',
              referenceText: visual.referenceText || visual.reference_text || '',
              referenceFound: visual.referenceFound,
            }))
          };
        }),
        totalDuration: section.total_duration || 0,
      };
    }),
    createdAt: apiScript.created_at ? new Date(apiScript.created_at) : new Date(),
    updatedAt: apiScript.updated_at ? new Date(apiScript.updated_at) : new Date(),
    status: apiScript.status || 'draft',
  };
}

/**
 * Generate an image based on a description
 */
export async function generateImage(description: string, model?: string, aspectRatio: string = '16:9'): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/image/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: description,
        model,
        aspect_ratio: aspectRatio
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
    remove_background_method: (typeof arguments[0].removeBackgroundMethod !== 'undefined' ? arguments[0].removeBackgroundMethod : 'color'),
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
 * Trigger background audio generation for all segments in a project (main script)
 */
export async function generateAllProjectAudio(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/audio/generate_all_project_audio/${projectId}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
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
 * Trigger background audio generation for all segments in the short script (short_content field)
 * @param projectId Project ID
 * @returns {Promise<{ message: string }>}
 */
export async function generateAllShortProjectAudio(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/audio/generate_all_project_audio/${projectId}?field=short_content`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    // No body needed for this request
  });

  if (!response.ok) {
    let errorDetail = "Failed to trigger bulk audio generation for short script";
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
 * Trigger background visual timing organization for all segments in the short script (short_content)
 */
export async function organizeAllShortProjectVisuals(projectId: number): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/script/organize_all_short_visuals/${projectId}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    // No body needed
  });

  if (!response.ok) {
    let errorDetail = "Failed to trigger bulk visual organization for short script";
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
// Accepts an object with segment, projectId, sectionId
export async function organizeSegmentVisuals({ segment, projectId, sectionId }: { segment: ScriptSegment, projectId: string, sectionId: string }): Promise<{ organized_segment: ScriptSegment }> {
  const payload = { segment, projectId, sectionId };

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
