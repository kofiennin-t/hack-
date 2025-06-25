import { ModelChat } from "@/components/model-chat"
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
            <ModelChat model={model} />
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
