import { Script } from '../types/script';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Generate a script using the backend API
 */
export async function generateScript(
  topic: string,
  targetAudience: string,
  durationMinutes: number,
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
        style,
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
function transformScriptFromApi(apiScript: any): Script {
  // Convert the API script format to the frontend script format
  return {
    id: apiScript.id,
    title: apiScript.title,
    description: apiScript.description,
    targetAudience: apiScript.target_audience,
    sections: apiScript.sections.map((section: any) => ({
      id: section.id,
      title: section.title,
      content: section.content,
      segments: section.segments.map((segment: any) => ({
        id: segment.id,
        narrationText: segment.narration_text,
        startTime: segment.start_time,
        duration: segment.duration,
        visuals: segment.visuals.map((visual: any) => ({
          id: visual.id,
          description: visual.description,
          timestamp: visual.timestamp,
          duration: visual.duration,
          imageUrl: visual.image_url,
          altText: visual.alt_text,
          visualType: visual.visual_type,
          visualStyle: visual.visual_style,
          position: visual.position,
          zoomLevel: visual.zoom_level,
          transition: visual.transition,
        })),
      })),
      totalDuration: section.total_duration,
    })),
    createdAt: new Date(apiScript.created_at),
    updatedAt: new Date(apiScript.updated_at),
    totalDuration: apiScript.total_duration,
    status: apiScript.status,
  };
}
