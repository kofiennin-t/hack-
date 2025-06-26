import { ModelCard } from "@/components/model-card"

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
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {sampleModels.map((model) => (
        <ModelCard key={model.id} model={model} />
      ))}
    </div>
  )
}
