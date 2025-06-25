# AIHub - AI Model Platform

A YouTube-inspired platform where AI developers can showcase their models and users can interact with them through intuitive chat interfaces. Think of it as "YouTube for AI models" - developers get their own channels, users can discover and chat with various AI models, and everything is designed for seamless interaction.

## 🌟 Features

### For Users
- **Discover AI Models**: Browse through a curated collection of AI models with YouTube-style thumbnails and descriptions
- **Interactive Chat**: Real-time chat interfaces with streaming responses for smooth conversations
- **Model Categories**: Filter models by type (Text Generation, Image Generation, Code Assistant, etc.)
- **Ratings & Reviews**: See community ratings and interaction counts to find the best models
- **Search & Filter**: Find exactly what you're looking for with powerful search and filtering

### For Developers
- **Developer Dashboard**: Comprehensive portal to manage your AI models and track performance
- **Easy Model Upload**: Simple form-based interface to register your AI model endpoints
- **Analytics**: Track interactions, ratings, and performance metrics
- **Channel-Style Profiles**: Get your own developer profile showcasing all your models
- **API Integration**: Connect any AI model with a REST API endpoint

## 🚀 Tech Stack

- **Framework**: Next.js 14 with App Router
- **UI Components**: shadcn/ui with Tailwind CSS
- **AI Integration**: Vercel AI SDK for chat functionality
- **Icons**: Lucide React
- **Styling**: Tailwind CSS with responsive design
- **TypeScript**: Full type safety throughout the application

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aihub-platform.git
   cd aihub-platform
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the root directory:
   ```env
   # OpenAI API Key (for chat functionality)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Add other AI provider keys as needed
   ANTHROPIC_API_KEY=your_anthropic_key
   GROQ_API_KEY=your_groq_key
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000) to see the application.

## 🏗️ Project Structure

```
├── app/
│   ├── api/chat/          # AI chat API endpoints
│   ├── developer/         # Developer dashboard pages
│   ├── model/[id]/        # Individual model pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx          # Homepage
│   └── globals.css       # Global styles
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── hero-section.tsx  # Homepage hero
│   ├── model-grid.tsx    # Model discovery grid
│   ├── model-chat.tsx    # Chat interface
│   ├── developer-dashboard.tsx
│   └── ...
├── lib/
│   └── utils.ts          # Utility functions
└── types/
    └── ...               # TypeScript type definitions
```

## 🔧 Configuration

### Adding New AI Providers

The platform uses the Vercel AI SDK, making it easy to add new AI providers:

```typescript
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'
import { anthropic } from '@ai-sdk/anthropic'

// Switch between providers easily
const { text } = await generateText({
  model: openai('gpt-4o'), // or anthropic('claude-3-sonnet')
  prompt: 'Your prompt here'
})
```

### Customizing Model Categories

Edit the categories in `components/category-filter.tsx`:

```typescript
const categories = [
  "All Models",
  "Text Generation",
  "Image Generation",
  "Code Assistant",
  "Translation",
  "Summarization",
  "Question Answering",
  // Add your custom categories here
]
```

## 🎨 Customization

### Styling
- The project uses Tailwind CSS for styling
- shadcn/ui components can be customized in `components/ui/`
- Global styles are in `app/globals.css`

### Adding New Model Types
1. Update the category filter options
2. Add new model card layouts if needed
3. Extend the model data structure in types

### Branding
- Update the logo and app name in `components/navigation.tsx`
- Modify colors in `tailwind.config.ts`
- Replace placeholder images with your own assets

## 🚀 Deployment

### Vercel (Recommended)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy automatically

### Other Platforms
The app can be deployed to any platform that supports Next.js:
- Netlify
- Railway
- DigitalOcean App Platform
- AWS Amplify

## 🔌 API Integration

### For Developers Adding Models

To integrate your AI model:

1. **Ensure your API follows this format**:
   ```
   POST /your-api-endpoint
   Content-Type: application/json
   
   {
     "messages": [
       {"role": "user", "content": "Hello"}
     ]
   }
   ```

2. **Response should be streaming or standard JSON**:
   ```json
   {
     "choices": [
       {
         "message": {
           "content": "Hello! How can I help you?"
         }
       }
     ]
   }
   ```

3. **Register your model** through the developer dashboard

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Use the existing component patterns
- Add proper error handling
- Write meaningful commit messages
- Test your changes thoroughly

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check out the [Vercel AI SDK docs](https://sdk.vercel.ai)
- **Issues**: Report bugs or request features via GitHub Issues
- **Community**: Join our discussions for help and feedback

## 🙏 Acknowledgments

- [Vercel AI SDK](https://sdk.vercel.ai) for the excellent AI integration tools
- [shadcn/ui](https://ui.shadcn.com) for the beautiful UI components
- [Tailwind CSS](https://tailwindcss.com) for the utility-first CSS framework
- [Lucide](https://lucide.dev) for the clean, consistent icons

## 🗺️ Roadmap

- [ ] User authentication and profiles
- [ ] Model rating and review system
- [ ] Payment integration for premium models
- [ ] Advanced search and filtering
- [ ] Model performance analytics
- [ ] Mobile app development
- [ ] API marketplace features
- [ ] Multi-language support

---

**Built with ❤️ using Next.js and the Vercel AI SDK**
```

I've created a comprehensive README for your AI model platform! The README includes:

## Key Sections:
- **Project overview** explaining the YouTube + Hugging Face concept
- **Feature breakdown** for both users and developers
- **Complete installation guide** with environment setup
- **Project structure** showing how the code is organized
- **Configuration instructions** for adding new AI providers
- **Deployment guides** for various platforms
- **API integration docs** for developers wanting to add their models
- **Contributing guidelines** for open source collaboration

## Highlights:
- Clear installation steps with all necessary commands
- Environment variable setup for AI providers
- Code examples showing how to extend the platform
- Deployment instructions for Vercel and other platforms
- API documentation for model integration
- Roadmap showing future development plans

The README follows best practices with proper markdown formatting, code blocks, and emoji icons to make it visually appealing and easy to navigate. It provides everything someone would need to understand, install, customize, and contribute to your AI model platform!
