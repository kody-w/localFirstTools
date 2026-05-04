import { useState, useRef, useEffect, useCallback } from 'react'
import './App.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
  codeChange?: {
    file: string
    code: string
    description: string
  }
}

interface AppState {
  version: number
  customStyles: string
  features: string[]
  theme: 'light' | 'dark'
  layout: 'default' | 'split' | 'minimal'
}

// The app's "DNA" - this gets modified by Claude's suggestions
const INITIAL_STATE: AppState = {
  version: 1,
  customStyles: '',
  features: ['chat', 'code-preview'],
  theme: 'dark',
  layout: 'default'
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [apiKey, setApiKey] = useState(localStorage.getItem('anthropic_api_key') || '')
  const [showApiKeyInput, setShowApiKeyInput] = useState(!localStorage.getItem('anthropic_api_key'))
  const [appState, setAppState] = useState<AppState>(INITIAL_STATE)
  const [showCode, setShowCode] = useState(false)
  const [currentCode, setCurrentCode] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Apply custom styles dynamically
  useEffect(() => {
    const styleEl = document.getElementById('dynamic-styles') || document.createElement('style')
    styleEl.id = 'dynamic-styles'
    styleEl.textContent = appState.customStyles
    if (!document.getElementById('dynamic-styles')) {
      document.head.appendChild(styleEl)
    }
  }, [appState.customStyles])

  const saveApiKey = () => {
    localStorage.setItem('anthropic_api_key', apiKey)
    setShowApiKeyInput(false)
  }

  const generateSystemPrompt = useCallback(() => {
    return `You are Claude, embedded in a self-improving React chat application. This is meta - you're running inside the app you can modify!

CURRENT APP STATE:
${JSON.stringify(appState, null, 2)}

YOUR CAPABILITIES:
1. Chat normally with the user
2. Suggest and apply modifications to this very app
3. Add new features, change styles, modify behavior

When the user asks you to modify the app, respond with a JSON code block containing the changes:

\`\`\`json
{
  "action": "modify_app",
  "changes": {
    "customStyles": "/* CSS changes */",
    "theme": "light" | "dark",
    "layout": "default" | "split" | "minimal",
    "features": ["array", "of", "features"],
    "description": "What this change does"
  }
}
\`\`\`

Or for more complex React component changes:

\`\`\`json
{
  "action": "suggest_code",
  "file": "App.tsx",
  "description": "Description of the change",
  "code": "// The new code to show the user"
}
\`\`\`

CURRENT FEATURES: ${appState.features.join(', ')}
CURRENT THEME: ${appState.theme}
CURRENT LAYOUT: ${appState.layout}
VERSION: ${appState.version}

Be creative! You can:
- Change colors, fonts, layouts
- Add new UI elements
- Modify behavior
- Add animations
- Change the overall look and feel

Always explain what you're changing and why. The user can see the changes in real-time!`
  }, [appState])

  const parseAndApplyChanges = (content: string) => {
    const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/)
    if (jsonMatch) {
      try {
        const changes = JSON.parse(jsonMatch[1])

        if (changes.action === 'modify_app') {
          setAppState(prev => ({
            ...prev,
            ...changes.changes,
            version: prev.version + 1
          }))
        } else if (changes.action === 'suggest_code') {
          setCurrentCode(changes.code)
          setShowCode(true)
        }
      } catch (e) {
        console.error('Failed to parse changes:', e)
      }
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 4096,
          system: generateSystemPrompt(),
          messages: [...messages, userMessage].map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      })

      const data = await response.json()

      if (data.content && data.content[0]) {
        const assistantContent = data.content[0].text
        const assistantMessage: Message = {
          role: 'assistant',
          content: assistantContent
        }
        setMessages(prev => [...prev, assistantMessage])
        parseAndApplyChanges(assistantContent)
      } else if (data.error) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `Error: ${data.error.message}`
        }])
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getLayoutClass = () => {
    switch (appState.layout) {
      case 'split': return 'layout-split'
      case 'minimal': return 'layout-minimal'
      default: return 'layout-default'
    }
  }

  if (showApiKeyInput) {
    return (
      <div className={`app-container ${appState.theme}`}>
        <div className="api-key-setup">
          <h1>🔄 Self-Improving Chat</h1>
          <p>Enter your Anthropic API key to get started</p>
          <p className="subtitle">This app can modify itself based on your feedback!</p>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-ant-..."
            className="api-key-input"
          />
          <button onClick={saveApiKey} className="save-key-btn">
            Start Chatting
          </button>
          <p className="security-note">
            Your API key is stored locally in your browser
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className={`app-container ${appState.theme} ${getLayoutClass()}`}>
      <header className="app-header">
        <div className="header-left">
          <h1>🔄 Self-Improving Chat v{appState.version}</h1>
          <span className="feature-badges">
            {appState.features.map(f => (
              <span key={f} className="badge">{f}</span>
            ))}
          </span>
        </div>
        <div className="header-right">
          <button
            className="toggle-btn"
            onClick={() => setShowCode(!showCode)}
          >
            {showCode ? '💬 Chat' : '👁️ Code'}
          </button>
          <button
            className="settings-btn"
            onClick={() => setShowApiKeyInput(true)}
          >
            ⚙️
          </button>
        </div>
      </header>

      <div className="main-content">
        <div className={`chat-panel ${showCode ? 'with-code' : ''}`}>
          <div className="messages-container">
            {messages.length === 0 && (
              <div className="welcome-message">
                <h2>Welcome to the Meta Chat! 🚀</h2>
                <p>I'm Claude, running inside this React app. The twist? You can ask me to modify this very interface!</p>
                <div className="suggestions">
                  <p><strong>Try asking me to:</strong></p>
                  <ul>
                    <li>"Make the background gradient purple and pink"</li>
                    <li>"Add a dark mode toggle"</li>
                    <li>"Make the messages appear with animations"</li>
                    <li>"Change the layout to be more minimal"</li>
                    <li>"Add typing indicators"</li>
                  </ul>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <pre>{msg.content}</pre>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message assistant loading">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything, or tell me to modify this app..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              className="send-btn"
            >
              {isLoading ? '...' : '→'}
            </button>
          </div>
        </div>

        {showCode && (
          <div className="code-panel">
            <div className="code-header">
              <h3>📝 Current App State</h3>
            </div>
            <pre className="code-content">
              {currentCode || JSON.stringify(appState, null, 2)}
            </pre>
          </div>
        )}
      </div>

      <footer className="app-footer">
        <span>Theme: {appState.theme}</span>
        <span>Layout: {appState.layout}</span>
        <span>Modifications: {appState.version - 1}</span>
      </footer>
    </div>
  )
}

export default App
