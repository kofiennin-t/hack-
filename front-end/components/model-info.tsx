import { Calendar, DollarSign, Star, MessageCircle, Tag } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface ModelInfoProps {
  model: {
    name: string
    description: string
    category: string
    thumbnail: string
    rating: number
    interactions: number
    tags: string[]
    pricing: string
    lastUpdated: string
    supportedInputs: {
      text: boolean
      image: boolean
      document: boolean
      audio: boolean
    }
  }
}

export function ModelInfo({ model }: ModelInfoProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Information</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden">
          <img src={model.thumbnail || "/placeholder.svg"} alt={model.name} className="w-full h-full object-cover" />
        </div>

        <div>
          <h3 className="font-semibold text-lg mb-2">{model.name}</h3>
          <p className="text-gray-700 text-sm mb-3">{model.description}</p>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center text-sm">
              <Star className="h-4 w-4 text-yellow-400 mr-2" />
              <span>{model.rating} rating</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <MessageCircle className="h-4 w-4 mr-1" />
              <span>{model.interactions.toLocaleString()} interactions</span>
            </div>
          </div>

          <div className="flex items-center text-sm text-gray-600">
            <DollarSign className="h-4 w-4 mr-2" />
            <span>{model.pricing}</span>
          </div>

          <div className="flex items-center text-sm text-gray-600">
            <Calendar className="h-4 w-4 mr-2" />
            <span>Updated {model.lastUpdated}</span>
          </div>
        </div>

        <div>
          <div className="flex items-center mb-2">
            <Tag className="h-4 w-4 mr-2" />
            <span className="text-sm font-medium">Tags</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {model.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center mb-2">
            <Tag className="h-4 w-4 mr-2" />
            <span className="text-sm font-medium">Supported Inputs</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {model.supportedInputs.text && (
              <Badge variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200">
                ✅ Text
              </Badge>
            )}
            {model.supportedInputs.image && (
              <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
                ✅ Images
              </Badge>
            )}
            {model.supportedInputs.document && (
              <Badge variant="outline" className="text-xs bg-purple-50 text-purple-700 border-purple-200">
                ✅ Documents
              </Badge>
            )}
            {model.supportedInputs.audio && (
              <Badge variant="outline" className="text-xs bg-orange-50 text-orange-700 border-orange-200">
                ✅ Audio
              </Badge>
            )}
            {!model.supportedInputs.text && (
              <Badge variant="outline" className="text-xs bg-gray-50 text-gray-500 border-gray-200">
                ❌ Text
              </Badge>
            )}
            {!model.supportedInputs.image && (
              <Badge variant="outline" className="text-xs bg-gray-50 text-gray-500 border-gray-200">
                ❌ Images
              </Badge>
            )}
            {!model.supportedInputs.document && (
              <Badge variant="outline" className="text-xs bg-gray-50 text-gray-500 border-gray-200">
                ❌ Documents
              </Badge>
            )}
            {!model.supportedInputs.audio && (
              <Badge variant="outline" className="text-xs bg-gray-50 text-gray-500 border-gray-200">
                ❌ Audio
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
