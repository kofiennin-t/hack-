"use client"

import { ModelChat } from "@/components/model-chat"
import { ModelInfo } from "@/components/model-info"
import { DeveloperInfo } from "@/components/developer-info"
import { getModelById, getModelType, type Model } from "@/components/models-availble"
import { notFound } from 'next/navigation'
import Model3DViewer from "@/components/3dmeshview"
import { useState, useEffect } from "react"
import ImageGenerationUI from "./model-img-gen"
import DiseaseDetectionUI from "./diseeasedet"
// Helper function to validate and determine UI layout
const getUIConfig = (modelType: string) => {
  const configs = {
    imagegeneration: {
      layout: 'image',
      primaryComponent: 'ImageGenerator',
      bgColor: 'bg-purple-50',
      accentColor: 'purple'
    },
    '3dgeneration': {
      layout: '3d',
      primaryComponent: '3DViewer', 
      bgColor: 'bg-blue-50',
      accentColor: 'blue'
    },
    musicgeneration: {
      layout: 'audio',
      primaryComponent: 'AudioPlayer',
      bgColor: 'bg-green-50', 
      accentColor: 'green'
    },
    default: {
      layout: 'chat',
      primaryComponent: 'ModelChat',
      bgColor: 'bg-gray-50',
      accentColor: 'gray'
    }
  }
  
  return configs[modelType as keyof typeof configs] || configs.default
}



const ThreeDGenerationUI = ({ model, API_URL }: { model: any, API_URL: string }) => {
  const [generatedModelUrl, setGeneratedModelUrl] = useState<string | null>(null)
  
  // Use your local white_mesh.glb file
  const exampleModelUrl = "/white_mesh.glb"
  
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-4 text-blue-800">3D Mesh Generator</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Input Description</label>
            <textarea 
              className="w-full p-3 border rounded-lg resize-none" 
              rows={3}
              placeholder="Describe the 3D object..."
            />
            <div className="mt-3 space-y-2">
              <label className="block text-sm font-medium">Quality</label>
              <select className="w-full p-2 border rounded-lg">
                <option>Low (Fast)</option>
                <option>Medium</option>
                <option>High (Slow)</option>
              </select>
            </div>
            <button 
              className="mt-3 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
              onClick={() => setGeneratedModelUrl(exampleModelUrl)}
            >
              Generate 3D Mesh
            </button>
            <button 
              className="mt-2 w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700"
              onClick={() => setGeneratedModelUrl("/white_mesh.glb")}
            >
              Load White Mesh
            </button>
          </div>
          <div className="bg-gray-100 rounded-lg flex items-center justify-center min-h-[400px]">
            {generatedModelUrl ? (
              <Model3DViewer 
                modelUrl={generatedModelUrl}
                height={400}
                width={500}
                showTexture={true}
              />
            ) : (
              <span className="text-gray-500">3D viewer will appear here</span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const MusicGenerationUI = ({ model, API_URL }: { model: any, API_URL: string }) => (
  <div className="space-y-6">
    <div className="bg-white rounded-lg p-6 shadow-sm">
      <h2 className="text-xl font-semibold mb-4 text-green-800">Music Composition Studio</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Music Description</label>
          <textarea 
            className="w-full p-3 border rounded-lg resize-none" 
            rows={3}
            placeholder="Describe the music style, mood, instruments..."
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Genre</label>
            <select className="w-full p-2 border rounded-lg">
              <option>Classical</option>
              <option>Jazz</option>
              <option>Electronic</option>
              <option>Pop</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Duration</label>
            <select className="w-full p-2 border rounded-lg">
              <option>30 seconds</option>
              <option>1 minute</option>
              <option>2 minutes</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Tempo</label>
            <select className="w-full p-2 border rounded-lg">
              <option>Slow</option>
              <option>Medium</option>
              <option>Fast</option>
            </select>
          </div>
        </div>
        <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700">
          Generate Music
        </button>
        <div className="bg-gray-100 rounded-lg p-4">
          <span className="text-gray-500">Audio player will appear here</span>
        </div>
      </div>
    </div>
  </div>
)

export default function ModelPage({ params }: { params: Promise<{ id: string }> }) {
  const [model, setModel] = useState<Model | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadModel() {
      try {
        const resolvedParams = await params
        const foundModel = getModelById(resolvedParams.id)
        
        if (!foundModel) {
          notFound()
          return
        }
        
        setModel(foundModel)
      } catch (error) {
        console.error('Error loading model:', error)
        notFound()
      } finally {
        setIsLoading(false)
      }
    }

    loadModel()
  }, [params])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading model...</p>
        </div>
      </div>
    )
  }

  if (!model) {
    notFound()
  }
  
  const modelType = getModelType(model.id)
  const uiConfig = getUIConfig(modelType)

  // Render different UI based on model type
  const renderPrimaryInterface = () => {
    switch (modelType) {
      case 'imagegeneration':
        return <ImageGenerationUI model={model} API_URL={model.API_URL} />
      case '3dgeneration':
        return <ThreeDGenerationUI model={model} API_URL={model.API_URL} />
      case 'musicgeneration':
        return <MusicGenerationUI model={model} API_URL={model.API_URL} />
      case 'diseasedectection':
        return <DiseaseDetectionUI model={model} API_URL={model.API_URL} />
      default:
        return <ModelChat model={model} API_URL={model.API_URL} />
    }
  }

  return (
    <div className={`min-h-screen ${uiConfig.bgColor}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            {renderPrimaryInterface()}
          </div>
          <div className="space-y-6">
            <ModelInfo model={model} />
            <DeveloperInfo developer={model.developer} />
          </div>
        </div>
      </div>
    </div>
  )
}
