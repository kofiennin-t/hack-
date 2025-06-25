import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const modelData = [
  { name: "CodeWizard Pro", interactions: 15420, rating: 4.8, status: "Active" },
  { name: "DataAnalyzer", interactions: 8350, rating: 4.6, status: "Active" },
  { name: "TextSummarizer", interactions: 12100, rating: 4.7, status: "Active" },
  { name: "ImageClassifier", interactions: 5200, rating: 4.5, status: "Maintenance" },
]

export function ModelStats() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Models Performance</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {modelData.map((model, index) => (
            <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
              <div>
                <h3 className="font-medium">{model.name}</h3>
                <p className="text-sm text-gray-600">{model.interactions.toLocaleString()} interactions</p>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">★ {model.rating}</div>
                <div
                  className={`text-xs px-2 py-1 rounded-full ${
                    model.status === "Active" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {model.status}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
