"use client"

import { useState } from "react"

// API URL for the FLUX text-to-image model
const API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"

// Hardcoded Hugging Face token
const headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

interface ImageGenerationUIProps {
  model: any
}

export default function ImageGenerationUI({ model }: ImageGenerationUIProps) {
  const [prompt, setPrompt] = useState("")
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const generateImage = async () => {
    if (!prompt.trim()) return
    
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ inputs: prompt })
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        setImageUrl(url)
      } else {
        setError(`Failed to generate image: ${response.status}`)
      }
    } catch (err) {
      setError("Error generating image")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-4 text-purple-800">Image Generation Studio</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Text Prompt</label>
            <textarea 
              className="w-full p-3 border rounded-lg resize-none" 
              rows={4}
              placeholder="Describe the image you want to generate..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button 
              className="mt-3 w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50"
              onClick={generateImage}
              disabled={isLoading || !prompt.trim()}
            >
              {isLoading ? "Generating..." : "Generate Image"}
            </button>
            {error && (
              <p className="mt-2 text-red-600 text-sm">{error}</p>
            )}
          </div>
          <div className="bg-gray-100 rounded-lg aspect-square flex items-center justify-center">
            {imageUrl ? (
              <img 
                src={imageUrl} 
                alt="Generated image"
                className="max-w-full max-h-full rounded-lg"
              />
            ) : (
              <span className="text-gray-500">Generated image will appear here</span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
