import { InfocardHighlightResponse } from '../types/infocardHighlight';

const API_BASE_URL = 'http://localhost:8000';

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
