"use client"

import type React from "react"

import { useState } from "react"
import { Upload, Link, Tag, CheckCircle, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function ModelUploadForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    category: "",
    apiEndpoint: "",
    tokenKey: "",
    tags: "",
    pricing: "",
    thumbnailUrl: "",
    supportedInputs: {
      text: true,
      image: false,
      document: false,
      audio: false,
    },
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<{
    type: "success" | "error" | null
    message: string
  }>({ type: null, message: "" })

  const handleInputChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSupportedInputChange = (inputType: string, checked: boolean) => {
    setFormData((prev) => ({
      ...prev,
      supportedInputs: {
        ...prev.supportedInputs,
        [inputType]: checked,
      },
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus({ type: null, message: "" })

    try {
      // Validate required fields
      if (
        !formData.name ||
        !formData.description ||
        !formData.category ||
        !formData.apiEndpoint ||
        !formData.tokenKey
      ) {
        throw new Error("Please fill in all required fields")
      }

      // Submit to API
      const response = await fetch("/api/models", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.name,
          description: formData.description,
          category: formData.category,
          apiEndpoint: formData.apiEndpoint,
          tokenKey: formData.tokenKey,
          tags: formData.tags,
          pricing: formData.pricing,
          thumbnail: formData.thumbnailUrl,
          supportedInputs: formData.supportedInputs,
          developer: 1001, // Fixed developer ID as requested
          rating: 0,
          interactions: 0

        }),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.error || "Failed to upload model")
      }

      // Success!
      setSubmitStatus({
        type: "success",
        message: `Model "${formData.name}" uploaded successfully! Model ID: ${result.model.id}`,
      })

       // Show pop-up message
      alert("Model details uploaded successfully.");


      // Reset form
      setFormData({
        name: "",
        description: "",
        category: "",
        apiEndpoint: "",
        tokenKey: "",
        tags: "",
        pricing: "",
        thumbnailUrl: "",
        supportedInputs: {
          text: false,
          image: false,
          document: false,
          audio: false,
        },
      })

      console.log("Model uploaded:", result.model)
    } catch (error) {
      console.error("Upload error:", error)
      setSubmitStatus({
        type: "error",
        message: error instanceof Error ? error.message : "Failed to upload model",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Upload New AI Model
        </CardTitle>
      </CardHeader>
      <CardContent>
        {submitStatus.type && (
          <Alert variant={submitStatus.type === "error" ? "destructive" : "default"} className="mb-6">
            {submitStatus.type === "success" ? (
              <CheckCircle className="h-4 w-4" />
            ) : (
              <AlertCircle className="h-4 w-4" />
            )}
            <AlertDescription>{submitStatus.message}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="name">Model Name *</Label>
              <Input
                id="name"
                placeholder="e.g., CodeWizard Pro"
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="category">Category *</Label>
              <Select onValueChange={(value) => handleInputChange("category", value)} value={formData.category}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="3D-model-generation">3D Model Generation</SelectItem>
                  <SelectItem value="text-generation">Text Generation</SelectItem>
                  <SelectItem value="image-generation">Image Generation</SelectItem>
                  <SelectItem value="code-assistant">Code Assistant</SelectItem>
                  <SelectItem value="translation">Translation</SelectItem>
                  <SelectItem value="summarization">Summarization</SelectItem>
                  <SelectItem value="question-answering">Question Answering</SelectItem>
                  <SelectItem value="audio-processing">Audio Processing</SelectItem>
                  <SelectItem value="document-analysis">Document Analysis</SelectItem>
                  <SelectItem value="multi-modal">Multi-Modal</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description *</Label>
            <Textarea
              id="description"
              placeholder="Describe what your AI model does and its capabilities..."
              value={formData.description}
              onChange={(e) => handleInputChange("description", e.target.value)}
              rows={4}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="apiEndpoint" className="flex items-center gap-2">
              <Link className="h-4 w-4" />
              API Endpoint URL *
            </Label>
            <Input
              id="apiEndpoint"
              placeholder="https://api-inference.huggingface.co/models/your-model"
              value={formData.apiEndpoint}
              onChange={(e) => handleInputChange("apiEndpoint", e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="tokenKey">API Token/Key *</Label>
            <Input
              id="tokenKey"
              type="password"
              placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxx"
              value={formData.tokenKey}
              onChange={(e) => handleInputChange("tokenKey", e.target.value)}
              required
            />
            <p className="text-xs text-gray-500">
              Your API token will be stored securely and used to authenticate requests to your model.
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="thumbnailUrl">Thumbnail URL</Label>
            <Input
              id="thumbnailUrl"
              placeholder="https://example.com/your-model-thumbnail.jpg"
              value={formData.thumbnailUrl}
              onChange={(e) => handleInputChange("thumbnailUrl", e.target.value)}
            />
          </div>

          <div className="space-y-4">
            <div>
              <Label className="text-sm font-medium mb-3 block">Supported Input Types *</Label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="text"
                    className="rounded border-gray-300"
                    checked={formData.supportedInputs.text}
                    onChange={(e) => handleSupportedInputChange("text", e.target.checked)}
                  />
                  <Label htmlFor="text" className="text-sm">
                    Text
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="image"
                    className="rounded border-gray-300"
                    checked={formData.supportedInputs.image}
                    onChange={(e) => handleSupportedInputChange("image", e.target.checked)}
                  />
                  <Label htmlFor="image" className="text-sm">
                    Images
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="document"
                    className="rounded border-gray-300"
                    checked={formData.supportedInputs.document}
                    onChange={(e) => handleSupportedInputChange("document", e.target.checked)}
                  />
                  <Label htmlFor="document" className="text-sm">
                    Documents
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="audio"
                    className="rounded border-gray-300"
                    checked={formData.supportedInputs.audio}
                    onChange={(e) => handleSupportedInputChange("audio", e.target.checked)}
                  />
                  <Label htmlFor="audio" className="text-sm">
                    Audio
                  </Label>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="tags" className="flex items-center gap-2">
                  <Tag className="h-4 w-4" />
                  Tags (comma-separated)
                </Label>
                <Input
                  id="tags"
                  placeholder="image,music,3D"
                  value={formData.tags}
                  onChange={(e) => handleInputChange("tags", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="pricing">Pricing Model</Label>
                <Input
                  id="pricing"
                  placeholder="Free tier: 100 requests/day"
                  value={formData.pricing}
                  onChange={(e) => handleInputChange("pricing", e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-medium mb-2">Developer Information</h4>
            <p className="text-sm text-gray-600">
              Developer: <span className="font-mono">Asante Coders</span>
            </p>
          </div>

          <div className="flex gap-4">
            <Button type="submit" className="flex-1" disabled={isSubmitting}>
              {isSubmitting ? "Uploading..." : "Upload Model"}
            </Button>
            <Button
              type="button"
              variant="outline"
              className="bg-white text-gray-700 hover:bg-gray-50"
              disabled={isSubmitting}
            >
              Save as Draft
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
