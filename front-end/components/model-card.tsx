import Link from "next/link"
import { Star, MessageCircle, User } from "lucide-react"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface ModelCardProps {
  model: {
    id: string
    name: string
    developer: string
    description: string
    category: string
    thumbnail: string
    rating: number
    interactions: number
    tags: string[]
  }
}

export function ModelCard({ model }: ModelCardProps) {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="aspect-video bg-gray-200 relative">
        <img src={model.thumbnail || "/placeholder.svg"} alt={model.name} className="w-full h-full object-cover" />
        <Badge className="absolute top-2 right-2 bg-black/70 text-white">{model.category}</Badge>
      </div>

      <CardContent className="p-4">
        <h3 className="font-semibold text-lg mb-1 line-clamp-1">{model.name}</h3>
        <div className="flex items-center text-sm text-gray-600 mb-2">
          <User className="h-3 w-3 mr-1" />
          <span>{model.developer}</span>
        </div>
        <p className="text-sm text-gray-700 mb-3 line-clamp-2">{model.description}</p>

        <div className="flex items-center justify-between text-sm mb-3">
          <div className="flex items-center">
            <Star className="h-4 w-4 text-yellow-400 mr-1" />
            <span>{model.rating}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <MessageCircle className="h-4 w-4 mr-1" />
            <span>{model.interactions.toLocaleString()}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-1 mb-3">
          {model.tags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0">
        <Link href={`/model/${model.id}`} className="w-full">
          <Button className="w-full">Try Model</Button>
        </Link>
      </CardFooter>
    </Card>
  )
}
