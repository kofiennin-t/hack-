"use client"

import type React from "react"

import { useState } from "react"
import { Upload, Link, Tag } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export function ModelUploadForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    category: "",
    apiEndpoint: "",
    tags: "",
    pricing: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Model upload:", formData)
    // Handle form submission
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
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="name">Model Name</Label>
              <Input
                id="name"
                placeholder="e.g., CodeWizard Pro"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="category">Category</Label>
              <Select onValueChange={(value) => setFormData({ ...formData, category: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="text-generation">Text Generation</SelectItem>
                  <SelectItem value="image-generation">Image Generation</SelectItem>
                  <SelectItem value="code-assistant">Code Assistant</SelectItem>
                  <SelectItem value="translation">Translation</SelectItem>
                  <SelectItem value="summarization">Summarization</SelectItem>
                  <SelectItem value="question-answering">Question Answering</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              placeholder="Describe what your AI model does and its capabilities..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={4}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="apiEndpoint" className="flex items-center gap-2">
              <Link className="h-4 w-4" />
              API Endpoint URL
            </Label>
            <Input
              id="apiEndpoint"
              placeholder="https://api.yourservice.com/v1/chat"
              value={formData.apiEndpoint}
              onChange={(e) => setFormData({ ...formData, apiEndpoint: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="tags" className="flex items-center gap-2">
                <Tag className="h-4 w-4" />
                Tags (comma-separated)
              </Label>
              <Input
                id="tags"
                placeholder="Python, JavaScript, Debugging"
                value={formData.tags}
                onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="pricing">Pricing Model</Label>
              <Input
                id="pricing"
                placeholder="Free tier: 100 requests/day"
                value={formData.pricing}
                onChange={(e) => setFormData({ ...formData, pricing: e.target.value })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="thumbnail">Model Thumbnail</Label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="h-8 w-8 mx-auto text-gray-400 mb-2" />
              <p className="text-sm text-gray-600">Click to upload or drag and drop</p>
              <p className="text-xs text-gray-500">PNG, JPG up to 2MB</p>
            </div>
          </div>

          <div className="flex gap-4">
            <Button type="submit" className="flex-1">
              Upload Model
            </Button>
            <Button type="button" variant="outline" className="bg-white text-gray-700 hover:bg-gray-50">
              Save as Draft
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
