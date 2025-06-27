"use client"

import { useEffect, useState } from "react"
import { ModelCard } from "@/components/model-card"

interface Model {
  id: string
  name: string
  developer: string
  description: string
  category: string
  thumbnail: string
  rating: number
  interactions: number
  tags: string[]
}

// Sample models as fallback
const sampleModels = [
  {
    id: "1",
    name: "CodeWizard Pro",
    developer: "TechCorp AI",
    description: "Advanced code generation and debugging assistant",
    category: "Code Assistant",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.8,
    interactions: 15420,
    tags: ["Python", "JavaScript", "Debugging"],
  },
  {
    id: "2",
    name: "ArtisticVision",
    developer: "Creative Labs",
    description: "Generate stunning artwork and illustrations from text",
    category: "Image Generation",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.9,
    interactions: 28350,
    tags: ["Art", "Digital", "Creative"],
  },
  {
    id: "3",
    name: "DocumentAnalyzer",
    developer: "DataMind Solutions",
    description: "Analyze and extract insights from documents and images",
    category: "Document Analysis",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.7,
    interactions: 12800,
    tags: ["Analysis", "Documents", "OCR"],
  },
  {
    id: "4",
    name: "VoiceTranscriber",
    developer: "AudioTech AI",
    description: "Advanced speech-to-text and audio analysis",
    category: "Audio Processing",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.6,
    interactions: 18900,
    tags: ["Speech", "Transcription", "Audio"],
  },
  {
    id: "5",
    name: "MultiModal Assistant",
    developer: "OmniAI Corp",
    description: "Universal AI assistant for all file types",
    category: "Multi-Modal",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.9,
    interactions: 52100,
    tags: ["Multi-Modal", "Universal", "Assistant"],
  },
  {
    id: "6",
    name: "MathSolver Pro",
    developer: "EduTech AI",
    description: "Solve complex mathematical problems step by step",
    category: "Question Answering",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.9,
    interactions: 23400,
    tags: ["Math", "Education", "Problem Solving"],
  },
]

export function ModelGrid() {
  const [models, setModels] = useState<Model[]>(sampleModels)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch models from API
    const fetchModels = async () => {
      try {
        const response = await fetch("/api/models")
        const data = await response.json()

        if (data.success && data.models.length > 0) {
          // Transform API models to match our interface
          const apiModels = data.models.map((model: any) => ({
            id: model.id,
            name: model.name,
            developer: `Developer ${model.developerId}`, // You can enhance this with actual developer names
            description: model.description,
            category: model.category,
            thumbnail: model.thumbnailUrl,
            rating: model.rating,
            interactions: model.interactions,
            tags: model.tags,
          }))

          // Combine API models with sample models
          setModels([...apiModels, ...sampleModels])
        }
      } catch (error) {
        console.error("Failed to fetch models:", error)
        // Keep sample models as fallback
      } finally {
        setLoading(false)
      }
    }

    fetchModels()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-gray-200 aspect-video rounded-t-lg"></div>
            <div className="p-4 space-y-2">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              <div className="h-3 bg-gray-200 rounded w-full"></div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {models.map((model) => (
        <ModelCard key={model.id} model={model} />
      ))}
    </div>
  )
}
