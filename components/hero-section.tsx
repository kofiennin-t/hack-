import { Search, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function HeroSection() {
  return (
    <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="h-8 w-8 mr-2" />
            <h1 className="text-4xl font-bold">AIHub</h1>
          </div>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Discover and interact with cutting-edge AI models from developers worldwide. Chat, create, and explore the
            future of artificial intelligence.
          </p>
          <div className="max-w-md mx-auto flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input placeholder="Search AI models..." className="pl-10 bg-white text-black" />
            </div>
            <Button variant="secondary">Search</Button>
          </div>
        </div>
      </div>
    </div>
  )
}
