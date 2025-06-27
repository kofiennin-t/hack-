// Shared model data and utilities

export interface Model {
    id: string
    name: string
    developer: string
    description: string
    category: string
    rating: number
    interactions: number
    tags: string[]
    API_URL: string
    thumbnail: string
    pricing: string
    lastUpdated: string
    supportedInputs: {
      text: boolean
      image: boolean
      document: boolean
      audio: boolean
    }
  }
  
  export const models: Model[] = [
    {
      id: "imagegeneration-1",
      name: "DeepSeek-Image",
      developer: "TechCorp AI", 
      description: "Generate images from text",
      category: "Image Generation",
      thumbnail: "/placeholder.svg?height=200&width=300",
      rating: 4.8,
      interactions: 10,
      tags: ["Image", "Generation", "Creative"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      pricing: "Free tier available",
      lastUpdated: "2024-01-15",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false
      }
    },
    {
      id: "imagegeneration-2", 
      name: "ArtisticVision",
      developer: "Creative Labs",
      description: "Generate stunning artwork and illustrations from text",
      category: "Image Generation",
      rating: 4.9,
      interactions: 8,
      tags: ["Image", "Generation", "Creative"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "$0.05 per image",
      lastUpdated: "2024-01-12",
      supportedInputs: {
        text: true,
        image: true,
        document: false,
        audio: false
      }
    },
    {
      id: "3dgeneration-1",
      name: "DeepDream", 
      developer: "DataMind Solutions",
      description: "Intelligent document and article summarization",
      category: "3D Generation",
      rating: 4.6,
      interactions: 1,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "$0.10 per mesh",
      lastUpdated: "2024-01-10",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false
      }
    },
    {
      id: "3dgeneration-2",
      name: "Hunyuan3D-2",
      developer: "3DGenAI", 
      description: "Generate 3D meshes from images",
      category: "3D Generation",
      rating: 4.8, 
      interactions: 6,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "$0.15 per mesh",
      lastUpdated: "2024-01-08",
      supportedInputs: {
        text: false,
        image: true,
        document: false,
        audio: false
      }
    },
    {
      id: "3dgeneration-3",
      name: "3D Mesh Generator",
      developer: "3DGenAI",
      description: "Generate 3D meshes from text", 
      category: "3D Generation",
      rating: 4.8,
      interactions: 6,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "$0.12 per mesh",
      lastUpdated: "2024-01-05",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false
      }
    },
    {
      id: "musicgeneration-1",
      name: "Music Generator", 
      developer: "MusicGenAI",
      description: "Generate music from text",
      category: "Music Generation",
      rating: 4.9,
      interactions: 2, 
      tags: ["Music", "Generation", "Composition"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "$0.20 per track",
      lastUpdated: "2024-01-14",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: true
      }
    },

    {
      id: "textgeneration-1",
      name: "TextGenAI",
      developer: "TextAI Corp",
      description: "Generate text from prompts",
      category: "Text Generation",
      rating: 4.7,
      interactions: 5,
      tags: ["Text", "Generation", "Creative"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification/resolve/main/thumbnail.png",
      pricing: "Free tier available",
      lastUpdated: "2024-01-11",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false
      }
    }
  ]
  
  export function getModelById(id: string): Model | null {
    return models.find(model => model.id === id) || null
  }
  
  export function getModelsByCategory(category: string): Model[] {
    return models.filter(model => model.category === category)
  }
  
  export function getModelType(id: string): string {
    const prefix = id.split('-')[0]
    return prefix
  }