import { type NextRequest, NextResponse } from "next/server"
import { ModelDatabase } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const query = searchParams.get("q")
    const category = searchParams.get("category")
    const developer = searchParams.get("developer")

    let models = await ModelDatabase.findAll()

    // Apply filters
    if (query) {
      models = await ModelDatabase.search(query)
    }

    if (category && category !== "All Models") {
      models = models.filter((model) => model.category === category)
    }

    if (developer) {
      const developerId = Number.parseInt(developer)
      if (!isNaN(developerId)) {
        models = await ModelDatabase.findByDeveloper(developerId)
      }
    }

    return NextResponse.json({
      success: true,
      models,
      count: models.length,
      filters: {
        query,
        category,
        developer,
      },
    })
  } catch (error) {
    console.error("❌ Error searching models:", error)
    return NextResponse.json({ error: "Failed to search models" }, { status: 500 })
  }
}
