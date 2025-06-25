import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

export const maxDuration = 30

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openai("gpt-4o-mini"),
    messages,
    system: "You are a helpful AI assistant. Provide clear, concise, and helpful responses.",
  })

  return result.toDataStreamResponse()
}
