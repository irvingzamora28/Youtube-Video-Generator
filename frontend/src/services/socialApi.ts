const API_BASE_URL = 'http://localhost:8000';


export async function generateSocialPosts(projectId: number, context?: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/social/${projectId}/generate_social_posts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: context ? JSON.stringify({ context }) : '{}',
  });
  if (!response.ok) {
    let errorMessage = 'Failed to generate social posts.';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        // Show a user-friendly message for JSON parsing errors
        if (errorData.detail.includes('Failed to parse LLM response')) {
          errorMessage = 'Sorry, the AI response could not be processed. Please try again or rephrase your request.';
        } else {
          errorMessage = errorData.detail;
        }
      }
    } catch (e) {
      // Ignore JSON parsing errors, use default message
    }
    throw new Error(errorMessage);
  }
  return response.json();
}
