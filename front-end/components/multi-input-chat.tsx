"use client"

import type React from "react"

import { useChat } from "ai/react"
import { useState, useRef } from "react"
import { Send, Bot, User, Upload, FileText, ImageIcon, X, Paperclip, Volume2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"

interface MultiInputChatProps {
  model: {
    id: string
    name: string
    description: string
    supportedInputs: {
      text: boolean
      image: boolean
      document: boolean
      audio: boolean
    }
  }
}

interface AttachedFile {
  file: File
  type: "image" | "document" | "audio"
  preview?: string
}

export function MultiInputChat({ model }: MultiInputChatProps) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
    initialMessages: [
      {
        id: "welcome",
        role: "assistant",
        content: `Hello! I'm ${model.name}. ${model.description} 

I can work with:
${model.supportedInputs.text ? "✅ Text input" : "❌ Text input"}
${model.supportedInputs.image ? "✅ Images (PNG, JPEG, JPG)" : "❌ Images"}
${model.supportedInputs.document ? "✅ Documents (PDF, DOCX)" : "❌ Documents"}
${model.supportedInputs.audio ? "✅ Audio (MP3, WAV)" : "❌ Audio"}

How can I help you today?`,
      },
    ],
  })

  const [activeTab, setActiveTab] = useState("text")
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([])
  const [textInput, setTextInput] = useState("")
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files) return

    Array.from(files).forEach((file) => {
      let fileType: "image" | "document" | "audio"

      if (file.type.startsWith("image/")) {
        fileType = "image"
      } else if (file.type.startsWith("audio/")) {
        fileType = "audio"
      } else {
        fileType = "document"
      }

      // Check if file type is supported
      if (fileType === "image" && !model.supportedInputs.image) {
        alert(`${model.name} doesn't support image inputs`)
        return
      }
      if (fileType === "document" && !model.supportedInputs.document) {
        alert(`${model.name} doesn't support document inputs`)
        return
      }
      if (fileType === "audio" && !model.supportedInputs.audio) {
        alert(`${model.name} doesn't support audio inputs`)
        return
      }

      const newFile: AttachedFile = {
        file,
        type: fileType,
      }

      // Create preview for images
      if (fileType === "image") {
        const reader = new FileReader()
        reader.onload = (e) => {
          newFile.preview = e.target?.result as string
          setAttachedFiles((prev) => [...prev, newFile])
        }
        reader.readAsDataURL(file)
      } else {
        setAttachedFiles((prev) => [...prev, newFile])
      }
    })

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const removeFile = (index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    let messageContent = ""

    if (activeTab === "text") {
      messageContent = input
    } else {
      messageContent = textInput
    }

    if (!messageContent.trim() && attachedFiles.length === 0) {
      return
    }

    // In a real implementation, you would handle file uploads here
    // For now, we'll just mention the attached files in the message
    if (attachedFiles.length > 0) {
      const fileDescriptions = attachedFiles.map((f) => `[${f.type.toUpperCase()}: ${f.file.name}]`).join(" ")
      messageContent = `${messageContent}\n\nAttached files: ${fileDescriptions}`
    }

    // Create a synthetic event for handleSubmit
    const syntheticEvent = {
      preventDefault: () => {},
      target: {
        elements: {
          message: { value: messageContent },
        },
      },
    } as any

    handleSubmit(syntheticEvent)

    // Clear inputs
    setTextInput("")
    setAttachedFiles([])
  }

  const getAcceptedFileTypes = () => {
    const types = []
    if (model.supportedInputs.image) {
      types.push(".png", ".jpg", ".jpeg")
    }
    if (model.supportedInputs.document) {
      types.push(".pdf", ".docx")
    }
    if (model.supportedInputs.audio) {
      types.push(".mp3", ".wav")
    }
    return types.join(",")
  }

  return (
    <Card className="h-[600px] flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-5 w-5" />
          Chat with {model.name}
        </CardTitle>
        <div className="flex gap-2">
          {model.supportedInputs.text && <Badge variant="secondary">Text</Badge>}
          {model.supportedInputs.image && <Badge variant="secondary">Images</Badge>}
          {model.supportedInputs.document && <Badge variant="secondary">Documents</Badge>}
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col p-0">
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className={`flex gap-2 max-w-[80%] ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                  <div className="flex-shrink-0">
                    {message.role === "user" ? (
                      <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                        <User className="h-4 w-4 text-white" />
                      </div>
                    ) : (
                      <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                        <Bot className="h-4 w-4 text-white" />
                      </div>
                    )}
                  </div>
                  <div
                    className={`rounded-lg px-4 py-2 ${
                      message.role === "user" ? "bg-blue-500 text-white" : "bg-gray-100 text-gray-900"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex gap-3 justify-start">
                <div className="flex gap-2">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <Bot className="h-4 w-4 text-white" />
                  </div>
                  <div className="bg-gray-100 rounded-lg px-4 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="border-t p-4">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger
                value="text"
                disabled={!model.supportedInputs.text}
                className="data-[state=active]:bg-blue-500 data-[state=active]:text-white"
              >
                Text
              </TabsTrigger>
              <TabsTrigger
                value="upload"
                disabled={
                  !model.supportedInputs.image && !model.supportedInputs.document && !model.supportedInputs.audio
                }
                className="data-[state=active]:bg-blue-500 data-[state=active]:text-white"
              >
                Upload
              </TabsTrigger>
              <TabsTrigger
                value="mixed"
                disabled={
                  !model.supportedInputs.text ||
                  (!model.supportedInputs.image && !model.supportedInputs.document && !model.supportedInputs.audio)
                }
                className="data-[state=active]:bg-blue-500 data-[state=active]:text-white"
              >
                Text + Files
              </TabsTrigger>
            </TabsList>

            <TabsContent value="text" className="mt-4">
              <form onSubmit={handleSubmit} className="flex gap-2">
                <Input
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Type your message..."
                  disabled={isLoading || !model.supportedInputs.text}
                  className="flex-1"
                />
                <Button type="submit" disabled={isLoading || !input.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="upload" className="mt-4">
              <div className="space-y-4">
                {/* File Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    accept={getAcceptedFileTypes()}
                    multiple
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={
                      !model.supportedInputs.image && !model.supportedInputs.document && !model.supportedInputs.audio
                    }
                    className="bg-white text-gray-700 hover:bg-gray-50"
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Choose Files
                  </Button>
                  <p className="text-sm text-gray-600 mt-2">
                    {model.supportedInputs.image &&
                      model.supportedInputs.document &&
                      model.supportedInputs.audio &&
                      "Images (PNG, JPG, JPEG), Documents (PDF, DOCX), or Audio (MP3, WAV)"}
                    {model.supportedInputs.image &&
                      model.supportedInputs.document &&
                      !model.supportedInputs.audio &&
                      "Images (PNG, JPG, JPEG) or Documents (PDF, DOCX)"}
                    {model.supportedInputs.image &&
                      !model.supportedInputs.document &&
                      model.supportedInputs.audio &&
                      "Images (PNG, JPG, JPEG) or Audio (MP3, WAV)"}
                    {!model.supportedInputs.image &&
                      model.supportedInputs.document &&
                      model.supportedInputs.audio &&
                      "Documents (PDF, DOCX) or Audio (MP3, WAV)"}
                    {model.supportedInputs.image &&
                      !model.supportedInputs.document &&
                      !model.supportedInputs.audio &&
                      "Images (PNG, JPG, JPEG)"}
                    {!model.supportedInputs.image &&
                      model.supportedInputs.document &&
                      !model.supportedInputs.audio &&
                      "Documents (PDF, DOCX)"}
                    {!model.supportedInputs.image &&
                      !model.supportedInputs.document &&
                      model.supportedInputs.audio &&
                      "Audio (MP3, WAV)"}
                  </p>
                </div>

                {/* Attached Files */}
                {attachedFiles.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Attached Files:</h4>
                    <div className="space-y-2">
                      {attachedFiles.map((attachedFile, index) => (
                        <div key={index} className="flex items-center gap-2 p-2 border rounded-lg">
                          {attachedFile.type === "image" ? (
                            <ImageIcon className="h-4 w-4 text-blue-500" />
                          ) : attachedFile.type === "audio" ? (
                            <Volume2 className="h-4 w-4 text-orange-500" />
                          ) : (
                            <FileText className="h-4 w-4 text-green-500" />
                          )}
                          <span className="text-sm flex-1">{attachedFile.file.name}</span>
                          <Button type="button" variant="ghost" size="sm" onClick={() => removeFile(index)}>
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <Button
                  onClick={handleFormSubmit}
                  disabled={isLoading || attachedFiles.length === 0}
                  className="w-full"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Send Files
                </Button>
              </div>
            </TabsContent>

            <TabsContent value="mixed" className="mt-4">
              <div className="space-y-4">
                <Textarea
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={isLoading}
                  rows={3}
                />

                {/* File Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    accept={getAcceptedFileTypes()}
                    multiple
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => fileInputRef.current?.click()}
                    className="bg-white text-gray-700 hover:bg-gray-50"
                  >
                    <Paperclip className="h-4 w-4 mr-2" />
                    Attach Files
                  </Button>
                </div>

                {/* Attached Files */}
                {attachedFiles.length > 0 && (
                  <div className="space-y-2">
                    <div className="flex flex-wrap gap-2">
                      {attachedFiles.map((attachedFile, index) => (
                        <div key={index} className="flex items-center gap-1 px-2 py-1 bg-gray-100 rounded-md text-xs">
                          {attachedFile.type === "image" ? (
                            <ImageIcon className="h-3 w-3 text-blue-500" />
                          ) : attachedFile.type === "audio" ? (
                            <Volume2 className="h-3 w-3 text-orange-500" />
                          ) : (
                            <FileText className="h-3 w-3 text-green-500" />
                          )}
                          <span className="max-w-20 truncate">{attachedFile.file.name}</span>
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => removeFile(index)}
                            className="h-4 w-4 p-0"
                          >
                            <X className="h-2 w-2" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <Button
                  onClick={handleFormSubmit}
                  disabled={isLoading || (!textInput.trim() && attachedFiles.length === 0)}
                  className="w-full"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Send Message
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </CardContent>
    </Card>
  )
}
