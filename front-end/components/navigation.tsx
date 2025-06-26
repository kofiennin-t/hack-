import Link from "next/link"
import { Sparkles, User, Upload } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Navigation() {
  return (
    <nav className="border-b bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-purple-600" />
            <span className="text-xl font-bold">Bridge.ai</span>
          </Link>

          <div className="flex items-center gap-4">
            <Link href="/developer">
              <Button variant="outline" className="bg-white text-gray-700 hover:bg-gray-50">
                <Upload className="h-4 w-4 mr-2" />
                Developer Portal
              </Button>
            </Link>
            <Button variant="outline" className="bg-white text-gray-700 hover:bg-gray-50">
              <User className="h-4 w-4 mr-2" />
              Sign In
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
