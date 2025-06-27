// Database utility functions
// This file provides a centralized way to manage the database

export interface AIModel {
  id: string
  name: string
  description: string
  category: string
  apiEndpoint: string
  tokenKey: string
  tags: string[]
  thumbnailUrl: string
  pricing: string
  developerId: number
  rating: number
  interactions: number
  lastUpdated: string
  supportedInputs: {
    text: boolean
    image: boolean
    document: boolean
    audio: boolean
  }
  createdAt: string
  status: "active" | "inactive" | "pending"
}

// In-memory database (replace with real database in production)
const database: AIModel[] = []

export class ModelDatabase {
  static async create(modelData: Partial<AIModel>): Promise<AIModel> {
    const id = `model_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    const model: AIModel = {
      id,
      name: modelData.name || "",
      description: modelData.description || "",
      category: modelData.category || "",
      apiEndpoint: modelData.apiEndpoint || "",
      tokenKey: modelData.tokenKey || "",
      tags: modelData.tags || [],
      thumbnailUrl: modelData.thumbnailUrl || "/placeholder.svg?height=400&width=600",
      pricing: modelData.pricing || "Free tier",
      developerId: 1001,
      rating: 4.5,
      interactions: 0,
      lastUpdated: new Date().toISOString().split("T")[0],
      supportedInputs: modelData.supportedInputs || {
        text: true,
        image: false,
        document: false,
        audio: false,
      },
      createdAt: new Date().toISOString(),
      status: "active",
    }

    database.push(model)
    return model
  }

  static async findAll(): Promise<AIModel[]> {
    return database
  }

  static async findById(id: string): Promise<AIModel | null> {
    return database.find((model) => model.id === id) || null
  }

  static async update(id: string, updates: Partial<AIModel>): Promise<AIModel | null> {
    const index = database.findIndex((model) => model.id === id)
    if (index === -1) return null

    database[index] = {
      ...database[index],
      ...updates,
      lastUpdated: new Date().toISOString().split("T")[0],
    }

    return database[index]
  }

  static async delete(id: string): Promise<boolean> {
    const index = database.findIndex((model) => model.id === id)
    if (index === -1) return false

    database.splice(index, 1)
    return true
  }

  static async incrementInteractions(id: string): Promise<void> {
    const model = await this.findById(id)
    if (model) {
      model.interactions += 1
    }
  }

  // Utility methods
  static async findByCategory(category: string): Promise<AIModel[]> {
    return database.filter((model) => model.category === category)
  }

  static async findByDeveloper(developerId: number): Promise<AIModel[]> {
    return database.filter((model) => model.developerId === developerId)
  }

  static async search(query: string): Promise<AIModel[]> {
    const lowercaseQuery = query.toLowerCase()
    return database.filter(
      (model) =>
        model.name.toLowerCase().includes(lowercaseQuery) ||
        model.description.toLowerCase().includes(lowercaseQuery) ||
        model.tags.some((tag) => tag.toLowerCase().includes(lowercaseQuery)),
    )
  }
}
