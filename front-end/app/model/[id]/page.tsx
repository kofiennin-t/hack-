import { MultiInputChat } from "@/components/multi-input-chat"
import { ModelInfo } from "@/components/model-info"
import { DeveloperInfo } from "@/components/developer-info"

// Sample model data - YOU CAN MANUALLY ADD API URLs AND TOKENS HERE
const getModelData = async (id: string) => {
  // First try to fetch from API
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"}/api/models/${id}`, {
      cache: "no-store", // Always fetch fresh data
    })

    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        return {
          id: data.model.id,
          name: data.model.name,
          developer: `Developer ${data.model.developerId}`,
          description: data.model.description,
          category: data.model.category,
          thumbnail: data.model.thumbnailUrl,
          rating: data.model.rating,
          interactions: data.model.interactions,
          tags: data.model.tags,
          apiEndpoint: data.model.apiEndpoint,
          huggingFaceToken: data.model.tokenKey,
          pricing: data.model.pricing,
          lastUpdated: data.model.lastUpdated,
          supportedInputs: data.model.supportedInputs,
        }
      }
    }
  } catch (error) {
    console.error("Failed to fetch model from API:", error)
  }

  // Fallback to hardcoded models
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
      // 👇 REPLACE THESE WITH YOUR ACTUAL VALUES
      apiEndpoint: "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
      huggingFaceToken: "hf_YOUR_ACTUAL_TOKEN_HERE", // Replace with your real token
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
      // 👇 MANUALLY ADD YOUR API URL AND TOKEN HERE
      apiEndpoint: "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
      huggingFaceToken: "hf_YOUR_TOKEN_HERE", // Replace with your actual token
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
      // 👇 MANUALLY ADD YOUR API URL AND TOKEN HERE
      apiEndpoint: "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
      huggingFaceToken: "hf_YOUR_TOKEN_HERE", // Replace with your actual token
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
      // 👇 MANUALLY ADD YOUR API URL AND TOKEN HERE
      apiEndpoint: "https://api-inference.huggingface.co/models/openai/whisper-large-v3",
      huggingFaceToken: "hf_YOUR_TOKEN_HERE", // Replace with your actual token
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
      // 👇 MANUALLY ADD YOUR API URL AND TOKEN HERE
      apiEndpoint: "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
      huggingFaceToken: "hf_YOUR_TOKEN_HERE", // Replace with your actual token
      pricing: "Free tier: 25 requests/day, Pro: $49/month",
      lastUpdated: "2024-01-25",
      supportedInputs: {
        text: true,
        image: true,
        document: true,
        audio: true,
      },
    },
    // 👇 ADD MORE MODELS HERE
    "6": {
      id: "6",
      name: "Your Custom Model",
      developer: "Your Company",
      description: "Description of your custom AI model",
      category: "Custom Category",
      thumbnail: "/placeholder.svg?height=400&width=600",
      rating: 4.5,
      interactions: 1000,
      tags: ["Custom", "AI", "Model"],
      // 👇 ADD YOUR CUSTOM API URL AND TOKEN HERE
      apiEndpoint: "https://your-custom-api.com/v1/chat",
      huggingFaceToken: "your_custom_token_here",
      pricing: "Custom pricing",
      lastUpdated: "2024-01-26",
      supportedInputs: {
        text: true,
        image: false,
        document: false,
        audio: false,
      },
    },
  }
  return models[id as keyof typeof models] || models["1"]
}

// Make the component async and await params
export default async function ModelPage({ params }: { params: { id: string } }) {
  // Await the params before using them
  const model = await getModelData(params.id)

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
