import { Script } from '../types/script';
import { transformScriptFromApi } from './api';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Types for project API
 */
export type ProjectListItem = {
  id: number;
  title: string;
  description: string;
  targetAudience: string;
  status: string;
  createdAt: Date;
  updatedAt: Date;
  totalDuration: number;
};

export type ProjectCreateParams = {
  title: string;
  description?: string;
  targetAudience?: string;
  visualStyle?: string;
  style?: string;
  inspiration?: string;
};

export type ProjectUpdateParams = {
  title?: string;
  description?: string;
  targetAudience?: string;
  status?: string;
  visualStyle?: string;
  style?: string;
  inspiration?: string;
};

export type AssetType = 'image' | 'audio' | 'video';

export type Asset = {
  id: number;
  projectId: number;
  assetType: AssetType;
  path: string;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  dataUrl?: string; // Base64 data URL for images
};

/**
 * Get images for a specific segment in a project
 */
export async function getSegmentImages(projectId: number, segmentId: string): Promise<Asset[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/segment/${segmentId}/images`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch segment images');
    }
    const data = await response.json();
    return data.assets.map(transformAssetFromApi);
  } catch (error) {
    console.error(`Error fetching images for project ${projectId}, segment ${segmentId}:`, error);
    throw error;
  }
}

/**
 * Transform project data from API format to frontend format
 */
function transformProjectFromApi(apiProject: any): ProjectListItem {
  return {
    id: apiProject.id,
    title: apiProject.title,
    description: apiProject.description || '',
    targetAudience: apiProject.target_audience || '',
    status: apiProject.status || 'draft',
    createdAt: new Date(apiProject.created_at),
    updatedAt: new Date(apiProject.updated_at),
    totalDuration: apiProject.total_duration || 0,
  };
}

/**
 * Transform asset data from API format to frontend format
 */
function transformAssetFromApi(apiAsset: any): Asset {
  return {
    id: apiAsset.id,
    projectId: apiAsset.project_id,
    assetType: apiAsset.asset_type,
    path: apiAsset.path,
    metadata: apiAsset.metadata || {},
    createdAt: new Date(apiAsset.created_at),
    updatedAt: new Date(apiAsset.updated_at),
    dataUrl: apiAsset.data, // Base64 data if included
  };
}

/**
 * Get all projects
 */
export async function getProjects(): Promise<ProjectListItem[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch projects');
    }

    const data = await response.json();
    return data.projects.map(transformProjectFromApi);
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
}

/**
 * Get a project by ID
 */
export async function uploadBackgroundImage(projectId: number, file: File): Promise<string> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/background-image`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to upload background image');
  }
  const data = await response.json();
  return data.background_image;
}

export async function getProject(projectId: number): Promise<Script> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch project');
    }

    const data = await response.json();
    console.log('Raw project data from API:', data);

    // If the project doesn't have a script yet, create an empty one
    if (!data.project.content) {
      console.log('No content found, creating empty object');
      data.project.content = {};
    } else {
      console.log('Project content:', data.project.content);
    }

    // If content is a string (JSON), parse it
    if (typeof data.project.content === 'string') {
      try {
        data.project.content = JSON.parse(data.project.content);
      } catch (e) {
        console.error('Error parsing project content:', e);
        data.project.content = {};
      }
    }

    // Add sections if they don't exist
    if (!data.project.sections) {
      data.project.sections = [];
    }

    const transformedScript = transformScriptFromApi(data.project);
    console.log('Transformed script:', transformedScript);
    return transformedScript;
  } catch (error) {
    console.error(`Error fetching project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Get a project's script content
 */
export async function getProjectScript(projectId: number): Promise<Script> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/script`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch project script');
    }

    const data = await response.json();
    return transformScriptFromApi(data.script);
  } catch (error) {
    console.error(`Error fetching script for project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Create a new project
 */
export async function createProject(params: ProjectCreateParams): Promise<ProjectListItem> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: params.title,
        description: params.description || '',
        target_audience: params.targetAudience || '',
        visual_style: params.visualStyle || '',
        inspiration: params.inspiration || '',
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create project');
    }

    const data = await response.json();
    return transformProjectFromApi(data.project);
  } catch (error) {
    console.error('Error creating project:', error);
    throw error;
  }
}

/**
 * Update a project
 */
export async function updateProject(
  projectId: number,
  params: ProjectUpdateParams
): Promise<ProjectListItem> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...(params.title !== undefined && { title: params.title }),
        ...(params.description !== undefined && { description: params.description }),
        ...(params.targetAudience !== undefined && { target_audience: params.targetAudience }),
        ...(params.status !== undefined && { status: params.status }),
        ...(params.visualStyle !== undefined && { visual_style: params.visualStyle }),
        ...(params.inspiration !== undefined && { inspiration: params.inspiration }),
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to update project');
    }

    const data = await response.json();
    return transformProjectFromApi(data.project);
  } catch (error) {
    console.error(`Error updating project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Get only the full script text (plain text, not structured)
 */
export async function getProjectFullScript(projectId: number): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/full_script`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch full script');
  }
  const data = await response.json();
  return data.script;
}

/**
 * Update a project's script content
 */
export async function updateProjectScript(projectId: number, script: Script): Promise<Script> {
  try {
    // Transform the script to API format
    // The backend expects the entire script object to be in the content field
    const apiScript = {
      content: script
    };

    console.log('Saving script to project:', projectId);
    console.log('Script data:', JSON.stringify(apiScript, null, 2));

    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/script`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(apiScript),
    });

    console.log('Script update response status:', response.status);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error updating script:', errorData);
      throw new Error(errorData.detail || 'Failed to update project script');
    }

    const responseData = await response.json();
    console.log('Script update response:', responseData);

    // Return the updated script
    return script;
  } catch (error) {
    console.error(`Error updating script for project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Delete a project
 */
export async function deleteProject(projectId: number): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to delete project');
    }

    const data = await response.json();
    return data.success;
  } catch (error) {
    console.error(`Error deleting project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Get assets for a project
 */
export async function getProjectAssets(
  projectId: number,
  assetType?: AssetType
): Promise<Asset[]> {
  try {
    const url = new URL(`${API_BASE_URL}/api/project/${projectId}/assets`);
    if (assetType) {
      url.searchParams.append('asset_type', assetType);
    }

    const response = await fetch(url.toString());

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch project assets');
    }

    const data = await response.json();
    return data.assets.map(transformAssetFromApi);
  } catch (error) {
    console.error(`Error fetching assets for project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Get a single asset by ID
 */
export async function getAsset(assetId: number, includeData: boolean = false): Promise<Asset> {
  try {
    const url = new URL(`${API_BASE_URL}/api/project/assets/${assetId}`);
    if (includeData) {
      url.searchParams.append('include_data', 'true');
    }

    const response = await fetch(url.toString());

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch asset');
    }

    const data = await response.json();
    return transformAssetFromApi(data.asset);
  } catch (error) {
    console.error(`Error fetching asset ${assetId}:`, error);
    throw error;
  }
}

/**
 * Upload an asset for a project
 */
export async function uploadAsset(
  projectId: number,
  assetType: AssetType,
  file: File,
  metadata: Record<string, any> = {}
): Promise<Asset> {
  try {
    const formData = new FormData();
    formData.append('asset_type', assetType);
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/assets`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to upload asset');
    }

    const data = await response.json();
    return transformAssetFromApi(data.asset);
  } catch (error) {
    console.error(`Error uploading asset for project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Upload a base64 image as an asset
 */
export async function uploadBase64Image(
  projectId: number,
  base64Data: string,
  metadata: Record<string, any> = {}
): Promise<Asset> {
  try {
    const formData = new FormData();
    formData.append('asset_type', 'image');
    formData.append('base64_data', base64Data);
    formData.append('metadata', JSON.stringify(metadata));

    const response = await fetch(`${API_BASE_URL}/api/project/${projectId}/assets`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to upload image');
    }

    const data = await response.json();
    return transformAssetFromApi(data.asset);
  } catch (error) {
    console.error(`Error uploading image for project ${projectId}:`, error);
    throw error;
  }
}

/**
 * Update an asset's metadata
 */
export async function updateAsset(
  assetId: number,
  metadata: Record<string, any>
): Promise<Asset> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/assets/${assetId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        metadata,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to update asset');
    }

    const data = await response.json();
    return transformAssetFromApi(data.asset);
  } catch (error) {
    console.error(`Error updating asset ${assetId}:`, error);
    throw error;
  }
}

/**
 * Delete an asset
 */
export async function deleteAsset(assetId: number): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/project/assets/${assetId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to delete asset');
    }

    const data = await response.json();
    return data.success;
  } catch (error) {
    console.error(`Error deleting asset ${assetId}:`, error);
    throw error;
  }
}
