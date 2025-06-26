import { ModelCard } from "@/components/model-card"
import { models } from "@/components/models-availble"

export function ModelGrid() {
  // Group models by category
  const modelsByCategory = models.reduce((acc, model) => {
    if (!acc[model.category]) {
      acc[model.category] = []
    }
    acc[model.category].push(model)
    return acc
  }, {} as Record<string, typeof models>)

  // Get sorted category names
  const categories = Object.keys(modelsByCategory).sort()

  return (
    <div className="space-y-12">
      {categories.map((category) => (
        <div key={category} className="space-y-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {category}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              {modelsByCategory[category].length} model{modelsByCategory[category].length !== 1 ? 's' : ''} available
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {modelsByCategory[category].map((model) => (
              <ModelCard key={model.id} model={model} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}