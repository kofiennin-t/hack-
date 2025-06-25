import { User, ExternalLink, Shield } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface DeveloperInfoProps {
  developer: string
}

export function DeveloperInfo({ developer }: DeveloperInfoProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="h-5 w-5" />
          Developer
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-lg">{developer.charAt(0)}</span>
          </div>
          <div>
            <h3 className="font-semibold">{developer}</h3>
            <p className="text-sm text-gray-600">Verified Developer</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center text-sm text-gray-600">
            <Shield className="h-4 w-4 mr-2 text-green-500" />
            <span>Verified & Trusted</span>
          </div>
          <p className="text-sm text-gray-700">
            Professional AI developer with expertise in machine learning and natural language processing.
          </p>
        </div>

        <div className="space-y-2">
          <Button variant="outline" className="w-full bg-white text-gray-700 hover:bg-gray-50">
            <ExternalLink className="h-4 w-4 mr-2" />
            View Profile
          </Button>
          <Button variant="outline" className="w-full bg-white text-gray-700 hover:bg-gray-50">
            More Models
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
