import { ModelGrid } from "@/components/model-grid"
import { HeroSection } from "@/components/hero-section"
import { CategoryFilter } from "@/components/category-filter"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <HeroSection />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <CategoryFilter />
        <ModelGrid />
      </div>
    </div>
  )
}
