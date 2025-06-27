import { type NextRequest, NextResponse } from "next/server"

// Simulated database - in production, use a real database
const modelsDatabase: any[] = []

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params

    // Find the model by ID
    const model = modelsDatabase.find((m) => m.id === id)

    if (!model) {
      return NextResponse.json({ error: "Model not found" }, { status: 404 })
    }

    return NextResponse.json({
      success: true,
      model,
    })
  } catch (error) {
    console.error("Error fetching model:", error)
    return NextResponse.json({ error: "Failed to fetch model" }, { status: 500 })
  }
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params
    const body = await request.json()

    // Find and update the model
    const modelIndex = modelsDatabase.findIndex((m) => m.id === id)

    if (modelIndex === -1) {
      return NextResponse.json({ error: "Model not found" }, { status: 404 })
    }

    // Update the model
    modelsDatabase[modelIndex] = {
      ...modelsDatabase[modelIndex],
      ...body,
      lastUpdated: new Date().toISOString().split("T")[0],
    }

    return NextResponse.json({
      success: true,
      model: modelsDatabase[modelIndex],
      message: "Model updated successfully!",
    })
  } catch (error) {
    console.error("Error updating model:", error)
    return NextResponse.json({ error: "Failed to update model" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params

    // Find and remove the model
    const modelIndex = modelsDatabase.findIndex((m) => m.id === id)

    if (modelIndex === -1) {
      return NextResponse.json({ error: "Model not found" }, { status: 404 })
    }

    // Remove the model
    modelsDatabase.splice(modelIndex, 1)

    return NextResponse.json({
      success: true,
      message: "Model deleted successfully!",
    })
  } catch (error) {
    console.error("Error deleting model:", error)
    return NextResponse.json({ error: "Failed to delete model" }, { status: 500 })
  }
}
