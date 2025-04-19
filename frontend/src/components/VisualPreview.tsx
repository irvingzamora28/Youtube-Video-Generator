import React from 'react';
import { Visual } from '../types/script'; // Assuming types are correctly placed

interface VisualPreviewProps {
  currentVisual: Visual | undefined | null;
  normalizeUrl: (path?: string) => string | undefined;
}

const VisualPreview: React.FC<VisualPreviewProps> = ({ currentVisual, normalizeUrl }) => {
  const imageUrl = currentVisual?.imageUrl ? normalizeUrl(currentVisual.imageUrl) : undefined;

  return (
    <div className="aspect-video bg-muted rounded-lg flex items-center justify-center text-muted-foreground overflow-hidden relative border border-border">
      {imageUrl ? (
        <img
          // Use a key based on the URL to force re-render if the image source changes but the component instance doesn't
          key={imageUrl}
          src={imageUrl}
          alt={currentVisual?.description || 'Visual'}
          className="max-w-full max-h-full object-contain"
          // Add error handling for images
          onError={(e) => {
            console.error(`Error loading image: ${imageUrl}`);
            // Optionally replace with a placeholder or hide the image
            (e.target as HTMLImageElement).style.display = 'none';
            // You could also set a state here to show a placeholder text/icon
          }}
        />
      ) : (
        // Display description if no image URL, or fallback text
        <span>{currentVisual?.description || 'Select a point on the timeline'}</span>
      )}
      {/* Overlay for text visuals */}
      {currentVisual?.visualType === 'text' && (
         <div className="absolute inset-0 flex items-center justify-center p-8 bg-black/50">
             <p className="text-white text-2xl text-center">{currentVisual.description}</p>
         </div>
      )}
    </div>
  );
};

export default VisualPreview;
