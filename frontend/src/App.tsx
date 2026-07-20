import { useEffect, useState } from 'react'
import viumsaLogo from './assets/brand/viumsa_logo.png'
import './App.css'

type Message = {
  role: 'user' | 'assistant'
  content: string
}
type Conversation = {
  id: number
  title: string
}

function App() {
  const [started, setStarted] = useState(false)
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  const [conversationId, setConversationId] =
    useState<number | null>(null)

  const [conversations, setConversations] =
    useState<Conversation[]>([])

  const [sidebarOpen, setSidebarOpen] = useState(true)
  async function loadConversations() {
  try {
    const response = await fetch(
      'http://127.0.0.1:8000/conversations'
    )

    if (!response.ok) {
      throw new Error('Failed to load conversations')
    }

    const data = await response.json()

    setConversations(data)
  } catch (error) {
    console.error('Could not load conversations:', error)
  }
}

useEffect(() => {
  loadConversations()
}, [])
async function openConversation(id: number) {
  if (loading) return

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/conversations/${id}/messages`
    )

    if (!response.ok) {
      throw new Error('Failed to load conversation')
    }

    const data = await response.json()

    setConversationId(id)
    setMessages(data)
    setStarted(true)
  } catch (error) {
    console.error('Could not open conversation:', error)
  }
}
function startNewChat() {
  setConversationId(null)
  setMessages([])
  setInput('')
  setStarted(true)
}
  
  async function sendMessage() {
    const message = input.trim()

    if (!message || loading) return

    setMessages((current) => [
      ...current,
      { role: 'user', content: message },
    ])

    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
        },

        body: JSON.stringify({
        message: message,
        conversation_id: conversationId,
      }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data = await response.json()
      setConversationId(data.conversation_id)
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: data.response },
      ])
    } catch (error) {
      console.error(error)

      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: 'Something went wrong while contacting Viumsa.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  if (started) {
    return (
      <main className={`chat-app ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
        <div className="sidebar-brand">
          <img src={viumsaLogo} alt="Viumsa" />
          {sidebarOpen && <span>VIUMSA</span>}
        </div>

    <button
      className="sidebar-toggle"
      onClick={() => setSidebarOpen(!sidebarOpen)}
      aria-label="Toggle sidebar"
      >
      {sidebarOpen ? '‹' : '›'}
    </button>
  </div>
      {sidebarOpen && (
      <button
        className="sidebar-new-chat"
        onClick={startNewChat}
        >
          + New chat
        </button>
      )}
      
  {sidebarOpen && (
  <div className="sidebar-conversations">
    <p className="sidebar-section-title">Recent</p>

    {conversations.map((conversation) => (
      <button
        key={conversation.id}
        className={`conversation-item ${
  conversationId === conversation.id ? 'active' : ''
}`}
        onClick={() => openConversation(conversation.id)}
      >
        {conversation.title}
      </button>
    ))}
  </div>
)}
</aside>
        <header className="chat-header">
          <div className="chat-brand">
            <img src={viumsaLogo} alt="Viumsa" />
            <span>VIUMSA</span>
          </div>

          <button
            className="new-chat-button"
            onClick={startNewChat}
          >
            New chat
          </button>
        </header>

        <section className="conversation">
          {messages.length === 0 ? (
            <div className="empty-chat">
              <img src={viumsaLogo} alt="" />

              <h2>How can I help you?</h2>

              <p>Ask, learn, create, or explore something new.</p>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.role}`}
                >
                  <p>{message.content}</p>
                </div>
              ))}

              {loading && (
                <div className="message assistant">
                  <p>Thinking...</p>
                </div>
              )}
            </div>
          )}
        </section>

        <div className="composer-area">
          <div className="composer">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault()
                  sendMessage()
                }
              }}
              placeholder="Ask Viumsa anything..."
              rows={1}
            />

            <button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              aria-label="Send message"
            >
              ↑
            </button>
          </div>

          <p className="disclaimer">
            Viumsa can make mistakes. Check important information.
          </p>
        </div>
      </main>
    )
  }

  return (
    <main className="viumsa-app">
      <section className="welcome">
        <div className="viumsa-mark">
          <img
            src={viumsaLogo}
            alt="Viumsa logo"
            className="viumsa-logo"
          />
        </div>

        <h1>VIUMSA</h1>

        <p className="tagline">
          Learn. Teach. Explore. Together.
        </p>

        <button
          className="start-button"
          onClick={startNewChat}
        >
          Start
        </button>
      </section>
    </main>
  )
}

export default App