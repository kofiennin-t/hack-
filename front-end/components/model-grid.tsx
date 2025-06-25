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
    name: "LinguaTranslate",
    developer: "GlobalAI Inc",
    description: "Real-time translation across 100+ languages",
    category: "Translation",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.7,
    interactions: 45200,
    tags: ["Translation", "Multilingual", "Communication"],
  },
  {
    id: "4",
    name: "SummaryMaster",
    developer: "DataMind Solutions",
    description: "Intelligent document and article summarization",
    category: "Summarization",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.6,
    interactions: 12800,
    tags: ["Summarization", "Documents", "Analysis"],
  },
  {
    id: "5",
    name: "ChatGenius",
    developer: "ConversationAI",
    description: "Advanced conversational AI for customer support",
    category: "Text Generation",
    thumbnail: "/placeholder.svg?height=200&width=300",
    rating: 4.8,
    interactions: 67500,
    tags: ["Chat", "Support", "Conversation"],
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
