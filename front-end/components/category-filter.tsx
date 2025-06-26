"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"

const categories = [
  "All Models",
  "Text Generation",
  "Image Generation",
  "Code Assistant",
  "Translation",
  "Summarization",
  "Question Answering",
  "Audio Processing",
  "Document Analysis",
  "Multi-Modal",
]

export function CategoryFilter() {
  const [activeCategory, setActiveCategory] = useState("All Models")

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold mb-4">Browse AI Models</h2>
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => (
          <Button
            key={category}
            variant={activeCategory === category ? "default" : "outline"}
            onClick={() => setActiveCategory(category)}
            className={activeCategory !== category ? "bg-white text-gray-700 hover:bg-gray-50" : ""}
          >
            {category}
          </Button>
        ))}
      </div>
    </div>
  )
}
