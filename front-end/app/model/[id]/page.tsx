import { MultiInputChat } from "@/components/multi-input-chat"
import { ModelInfo } from "@/components/model-info"
import { DeveloperInfo } from "@/components/developer-info"

// Sample model data - in a real app, this would come from a database
const getModelData = (id: string) => {
  const models = {
    "1": {
      id: "1",
      name: "CodeWizard Pro",
      developer: "TechCorp AI",
      description:
        "Advanced code generation and debugging assistant powered by state-of-the-art language models. Supports multiple programming languages and can help with code review, optimization, and debugging.",
      category: "Code Assistant",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.8,
      interactions: 15420,
      tags: ["Python", "JavaScript", "Debugging", "Code Review"],
      apiEndpoint: "https://api.techcorp.ai/codewizard",
      pricing: "Free tier: 100 requests/day, Pro: $29/month",
      lastUpdated: "2024-01-15",
      supportedInputs: {
        text: true,
        image: false,
        document: true,
        audio: false,
      },
    },
    "2": {
      id: "2",
      name: "ArtisticVision",
      developer: "Creative Labs",
      description: "Generate stunning artwork and illustrations from text and image inputs",
      category: "Image Generation",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.9,
      interactions: 28350,
      tags: ["Art", "Digital", "Creative"],
      apiEndpoint: "https://api.creativelabs.ai/artistic",
      pricing: "Free tier: 50 requests/day, Pro: $19/month",
      lastUpdated: "2024-01-20",
      supportedInputs: {
        text: true,
        image: true,
        document: false,
        audio: false,
      },
    },
    "3": {
      id: "3",
      name: "DocumentAnalyzer",
      developer: "DataMind Solutions",
      description: "Analyze and extract insights from documents, images, and text",
      category: "Document Analysis",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.7,
      interactions: 12800,
      tags: ["Analysis", "Documents", "OCR"],
      apiEndpoint: "https://api.datamind.ai/analyzer",
      pricing: "Free tier: 25 requests/day, Pro: $39/month",
      lastUpdated: "2024-01-18",
      supportedInputs: {
        text: true,
        image: true,
        document: true,
        audio: false,
      },
    },
    "4": {
      id: "4",
      name: "VoiceTranscriber",
      developer: "AudioTech AI",
      description: "Advanced speech-to-text and audio analysis with support for multiple languages",
      category: "Audio Processing",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.6,
      interactions: 18900,
      tags: ["Speech", "Transcription", "Audio", "Languages"],
      apiEndpoint: "https://api.audiotech.ai/transcribe",
      pricing: "Free tier: 60 minutes/month, Pro: $24/month",
      lastUpdated: "2024-01-22",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: true,
      },
    },
    "5": {
      id: "5",
      name: "MultiModal Assistant",
      developer: "OmniAI Corp",
      description: "Universal AI assistant that can process text, images, documents, and audio files",
      category: "Multi-Modal",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.9,
      interactions: 52100,
      tags: ["Multi-Modal", "Universal", "Assistant", "All-in-One"],
      apiEndpoint: "https://api.omniai.ai/process",
      pricing: "Free tier: 25 requests/day, Pro: $49/month",
      lastUpdated: "2024-01-25",
      supportedInputs: {
        text: true,
        image: true,
        document: true,
        audio: true,
      },
    },
  }
  return models[id as keyof typeof models] || models["1"]
}

export default function ModelPage({ params }: { params: { id: string } }) {
  const model = getModelData(params.id)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <MultiInputChat model={model} />
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
