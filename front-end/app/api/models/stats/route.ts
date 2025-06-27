import { type NextRequest, NextResponse } from "next/server"
import { ModelDatabase } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    const models = await ModelDatabase.findAll()

    // Calculate statistics
    const stats = {
      totalModels: models.length,
      totalInteractions: models.reduce((sum, model) => sum + model.interactions, 0),
      averageRating: models.length > 0 ? models.reduce((sum, model) => sum + model.rating, 0) / models.length : 0,
      categoryCounts: models.reduce(
        (acc, model) => {
          acc[model.category] = (acc[model.category] || 0) + 1
          return acc
        },
        {} as Record<string, number>,
      ),
      recentModels: models
        .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
        .slice(0, 5),
      topRatedModels: models.sort((a, b) => b.rating - a.rating).slice(0, 5),
      mostPopularModels: models.sort((a, b) => b.interactions - a.interactions).slice(0, 5),
    }

    return NextResponse.json({
      success: true,
      stats,
    })
  } catch (error) {
    console.error("❌ Error fetching stats:", error)
    return NextResponse.json({ error: "Failed to fetch statistics" }, { status: 500 })
  }
}
