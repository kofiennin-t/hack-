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
      developer: "Dzifa Yabetse", 
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
      developer: "Kofi Hassan",
      description: "Generate stunning artwork and illustrations from text",
      category: "Image Generation",
      rating: 4.9,
      interactions: 8,
      tags: ["Image", "Generation", "Creative"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "/artisticvision.jpg",
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
      developer: "Joey Karachi",
      description: "Intelligent document and article summarization",
      category: "3D Generation",
      rating: 4.6,
      interactions: 1,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "/deepdream.jpg",
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
      developer: "Frederica Josiane", 
      description: "Generate 3D meshes from images",
      category: "3D Generation",
      rating: 4.8, 
      interactions: 6,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "/hunyuan.png",
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
      developer: "Kwame Coder",
      description: "Generate 3D meshes from text", 
      category: "3D Generation",
      rating: 4.8,
      interactions: 6,
      tags: ["3D", "Mesh", "Generation"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "/3dmesh.png",
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
      developer: "Dadou Uwumukiza",
      description: "Generate music from text",
      category: "Music Generation",
      rating: 4.9,
      interactions: 2, 
      tags: ["Music", "Generation", "Composition"],
      API_URL:"https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev",
      thumbnail: "/musicgenerator.jpg",
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
      developer: "Asante Coders",
      description: "Generate text from prompts",
      category: "Text Generation",
      rating: 4.7,
      interactions: 5,
      tags: ["Text", "Generation", "Creative"],
      API_URL:"https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions",
      thumbnail: "/textgen.png",
      pricing: "Free tier available",
      lastUpdated: "2024-01-11",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false
      }
    },

    {
      id: "diseasedectection-1",
      name: "Skin Cancer Detection",
      developer: "DeMarcus",
      description: "Detect skin cancer from images",
      category: "Disease Detection",
      rating: 4.7,
      interactions: 1,
      tags: ["skin", "cancer", "detection"],
      API_URL:"https://router.huggingface.co/hf-inference/models/Anwarkh1/Skin_Cancer-Image_Classification",
      thumbnail: "/cancer.png",
      pricing: "Free tier available",
      lastUpdated: "2024-01-11",
      supportedInputs: {
        text: false,
        image: true,
        document: false,
        audio: false
      }
    },
    {
      id: "diseasedectection-2",
      name: "Plant Disease Detection",
      developer: "Freeman",
      description: "Detect plant diseases from images",
      category: "Disease Detection",
      rating: 4.7,
      interactions: 5,
      tags: ["plant", "disease", "detection"],
      API_URL:"https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
      thumbnail: "/plantdisease.png",
      pricing: "Free tier available",
      lastUpdated: "2024-01-11",
      supportedInputs: {
        text: false,
        image: true,
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