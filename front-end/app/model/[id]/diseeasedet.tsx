"use client"

import { useState } from "react"

// API URL for the FLUX text-to-image model
// const API_URL = "https://router.huggingface.co/hf-inference/models/Anwarkh1/Skin_Cancer-Image_Classification"

// Hardcoded Hugging Face token
const headers = {
    "Authorization": "Bearer hf_....",
}

interface DiseaseDetectionUIProps {
  model: any
  API_URL: string
}

interface ClassificationResult {
  label: string
  score: number
}

export default function DiseaseDetectionUI({ model, API_URL }: DiseaseDetectionUIProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<ClassificationResult[] | null>(null)

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedImage(file)
      setError(null)
      setResults(null)
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const classifyImage = async () => {
    if (!selectedImage) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          "Content-Type": "image/jpeg",
          ...headers
        },
        body: selectedImage
      })

      if (response.ok) {
        const result = await response.json()
        setResults(result)
      } else {
        setError(`Failed to classify image: ${response.status}`)
      }
    } catch (err) {
      setError("Error classifying image")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-4 text-purple-800">{model.name}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Upload Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="w-full p-3 border rounded-lg file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
            />
            <button 
              className="mt-3 w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50"
              onClick={classifyImage}
              disabled={isLoading || !selectedImage}
            >
              {isLoading ? "Analyzing..." : "Analyze Image"}
            </button>
            {error && (
              <p className="mt-2 text-red-600 text-sm">{error}</p>
            )}
            
            {/* Classification Results */}
            {results && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold mb-2">Classification Results:</h3>
                <div className="space-y-2">
                  {results.map((result, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm">{result.label}</span>
                      <span className="text-sm font-mono bg-purple-100 px-2 py-1 rounded">
                        {(result.score * 100).toFixed(2)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          
          <div className="bg-gray-100 rounded-lg aspect-square flex items-center justify-center">
            {imagePreview ? (
              <img 
                src={imagePreview} 
                alt="Selected image for analysis"
                className="max-w-full max-h-full rounded-lg object-contain"
              />
            ) : (
              <span className="text-gray-500">Selected image will appear here</span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
