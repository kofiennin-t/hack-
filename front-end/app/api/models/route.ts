import { type NextRequest, NextResponse } from "next/server"

// In a real application, you would use a proper database
// For now, we'll simulate a database with a JSON file or in-memory storage
const modelsDatabase: any[] = []

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const { name, description, category, apiEndpoint, tokenKey, tags, thumbnailUrl, pricing, supportedInputs } = body

    // Validate required fields
    if (!name || !description || !category || !apiEndpoint || !tokenKey) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 })
    }

    // Generate a unique ID for the model
    const modelId = `model_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    // Create the model object
    const newModel = {
      id: modelId,
      name,
      description,
      category,
      apiEndpoint,
      tokenKey, // Store the token key securely
      tags: tags
        .split(",")
        .map((tag: string) => tag.trim())
        .filter(Boolean),
      thumbnailUrl: thumbnailUrl || "/placeholder.svg?height=400&width=600",
      pricing: pricing || "Free tier",
      developerId: 1001, // Fixed developer ID as requested
      rating: 4.5, // Default rating
      interactions: 0, // Start with 0 interactions
      lastUpdated: new Date().toISOString().split("T")[0],
      supportedInputs: supportedInputs || {
        text: true,
        image: false,
        document: false,
        audio: false,
      },
      createdAt: new Date().toISOString(),
      status: "active",
    }

    // Add to our "database"
    modelsDatabase.push(newModel)

    // In a real app, you would save to a database here
    // await db.models.create(newModel)

    console.log("New model created:", newModel)

    return NextResponse.json({
      success: true,
      model: newModel,
      message: "Model uploaded successfully!",
    })
  } catch (error) {
    console.error("Error creating model:", error)
    return NextResponse.json({ error: "Failed to create model" }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    // Return all models from our "database"
    return NextResponse.json({
      success: true,
      models: modelsDatabase,
    })
  } catch (error) {
    console.error("Error fetching models:", error)
    return NextResponse.json({ error: "Failed to fetch models" }, { status: 500 })
  }
}
