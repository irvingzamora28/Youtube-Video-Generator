import { InfocardHighlightResponse } from '../types/infocardHighlight';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetch saved social posts for a project
 */
export async function getProjectSocialPosts(projectId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/social/${projectId}/social_posts`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch project social posts');
  }
  return response.json();
}


/**
 * Add text to all highlight images for a project
 */
export async function addTextToHighlightImages(projectId: number): Promise<InfocardHighlightResponse> {
  const response = await fetch(`${API_BASE_URL}/api/image/add_text_to_highlight_images/${projectId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to add text to highlight images');
  }
  return response.json();
}


/**
 * Fetch infocard highlights for a project
 */
export async function getInfocardHighlights(projectId: number): Promise<InfocardHighlightResponse> {
  const response = await fetch(`${API_BASE_URL}/api/infocard_highlights/${projectId}`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch infocard highlights');
  }
  return response.json();
}

/**
 * Generate images for all infocard highlights of a project
 */
export async function generateHighlightImages(projectId: number, aspectRatio: string = '16:9', postText?: string): Promise<InfocardHighlightResponse> {
  const response = await fetch(`${API_BASE_URL}/api/image/generate_highlight_images/${projectId}?aspect_ratio=${encodeURIComponent(aspectRatio)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to generate highlight images');
  }
  return response.json();
}
/**
 * Generate infocard highlights for a project (triggers LLM)
 */
export async function generateInfocardHighlights(projectId: number): Promise<InfocardHighlightResponse> {
  const response = await fetch(`${API_BASE_URL}/api/infocard_highlights/${projectId}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({}),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to generate infocard highlights');
  }
  return response.json();
}
