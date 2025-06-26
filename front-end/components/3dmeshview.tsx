import React, { useEffect, useRef, useState } from 'react';

// i need to display this .glb front-end\assets\white_mesh.glb file in the model-viewer web component

// TypeScript declarations for model-viewer web component
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'model-viewer': any;
    }
  }
}

interface Model3DViewerProps {
  modelUrl: string;
  height?: number;
  width?: number;
  showTexture?: boolean;
}

const Model3DViewer: React.FC<Model3DViewerProps> = ({ 
  modelUrl, 
  height = 600, 
  width = 700, 
  showTexture = true 
}) => {
  const modelViewerRef = useRef<any>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    // Import model-viewer web component
    const loadModelViewer = async () => {
      try {
        await import('@google/model-viewer');
      } catch (error) {
        console.error('Failed to load model-viewer:', error);
        setIsError(true);
      }
    };
    
    loadModelViewer();
  }, []);

  useEffect(() => {
    const modelViewer = modelViewerRef.current;
    
    if (modelViewer) {
      const handleLoad = () => {
        setIsLoaded(true);
        setIsError(false);
        
        try {
          // Apply material settings
          const model = modelViewer.model;
          if (model && model.materials && model.materials.length > 0) {
            const material = model.materials[0];
            if (material?.pbrMetallicRoughness) {
              material.pbrMetallicRoughness.setMetallicFactor(0.1);
              material.pbrMetallicRoughness.setRoughnessFactor(showTexture ? 0.5 : 0.7);
              
              if (!showTexture) {
                // Apply gray color for non-textured view
                const color = [43/255, 44/255, 46/255, 1.0];
                material.pbrMetallicRoughness.setBaseColorFactor(color);
              }
            }
          }
        } catch (error) {
          console.warn('Could not apply material settings:', error);
        }
      };

      const handleError = () => {
        setIsError(true);
        setIsLoaded(false);
      };

      modelViewer.addEventListener('load', handleLoad);
      modelViewer.addEventListener('error', handleError);
      
      return () => {
        modelViewer.removeEventListener('load', handleLoad);
        modelViewer.removeEventListener('error', handleError);
      };
    }
  }, [showTexture, modelUrl]);

  if (isError) {
    return (
      <div 
        className="flex items-center justify-center bg-red-50 border border-red-200 rounded-lg"
        style={{ height: `${height}px`, width: `${width}px` }}
      >
        <div className="text-center text-red-600">
          <p>Failed to load 3D model</p>
          <p className="text-sm">Please check the model URL</p>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="flex justify-center items-center rounded-lg border border-gray-200"
      style={{ height: `${height}px`, width: `${width}px` }}
    >
      <model-viewer
        ref={modelViewerRef}
        src={modelUrl}
        style={{ 
          height: `${height}px`, 
          width: `${width}px`,
          backgroundColor: 'transparent'
        }}
        camera-controls="true"
        auto-rotate="true"
        rotation-per-second="10deg"
        camera-target="0m 0m 0m"
        camera-orbit="0deg 90deg 8m"
        environment-image="neutral"
        shadow-intensity="0.9"
        exposure="1.0"
        ar="true"
        disable-tap="true"
        loading="eager"
      >
        {!isLoaded && (
          <div 
            slot="progress-bar" 
            className="absolute inset-0 flex items-center justify-center bg-gray-50"
          >
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
              <p className="text-gray-600">Loading 3D Model...</p>
            </div>
          </div>
        )}
      </model-viewer>
    </div>
  );
};

export default Model3DViewer;