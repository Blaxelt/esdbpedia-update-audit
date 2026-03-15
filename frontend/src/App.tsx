import './App.css'
import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [articleId, setArticleId] = useState('')
  const [inputValue, setInputValue] = useState('')
  const [articleText, setArticleText] = useState('')
  const [showPicker, setShowPicker] = useState(false)
  const [date, setDate] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [modalError, setModalError] = useState('')
  const [iframeSrc, setIframeSrc] = useState('')

  const buildIframeSrc = (id: string, fragment?: string) => {
    const base = `https://es.wikipedia.org/w/index.php?oldid=${id}`
    if (fragment) {
      return `${base}#:~:text=${encodeURIComponent(fragment)}`
    }
    return base
  }

  const loadArticle = (id: string) => {
    setError('')
    setArticleId(id)
    setInputValue(id)
    setIframeSrc(buildIframeSrc(id))
    fetch(`${API_URL}/articles/${id}`)
      .then(response => {
        if (!response.ok) throw new Error('Article not found')
        return response.json()
      })
      .then(data => setArticleText(data.text))
      .catch(error => setError(error.message))
  }

  const handleSearch = () => {
    if (!inputValue.trim()) {
      setError('Enter a revision ID')
      return
    }
    if (isNaN(Number(inputValue))) {
      setError('ID must be a number')
      return
    }
    loadArticle(inputValue)
  }

  const handleAdjacent = (direction: 'next' | 'prev') => {
    fetch(`${API_URL}/articles/${articleId}/${direction}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(direction === 'next' ? 'No next article' : 'No prev article')
        }
        return response.json()
      })
      .then(data => loadArticle(data.id))
      .catch(error => setError(error.message))
  }

  const handleSubmit = async () => {
    if (!date) return
    setLoading(true)
    setModalError('')
    try {
      const response = await fetch(`${API_URL}/articles/load?date=${date.replace(/-/g, '')}`, {
        method: 'POST',
      })
      if (!response.ok) {
        const data = await response.json()
        setModalError(data.detail || 'Unknown error')
        return
      }
      const data = await response.json()
      console.log('Respuesta:', data)
      setShowPicker(false)
    } catch (err) {
      setModalError('Could not reach the server.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  // Capture mouse-up on the clean text panel and scroll the iframe
  const handleTextSelection = () => {
    if (!articleId) return

    const selection = window.getSelection()
    if (!selection || selection.isCollapsed) return

    const selectedText = selection.toString().trim()
    if (!selectedText || selectedText.length < 3) return

    // Use up to the first 15 words to keep the fragment URL reliable
    const fragment = selectedText.split(/\s+/).slice(0, 15).join(' ')

    // Changing src forces the iframe to reload and jump to the fragment
    setIframeSrc(buildIframeSrc(articleId, fragment))
  }

  return (
    <div>
      <div className="top-bar">
        <p>Revision ID: {articleId}</p>
        <div className="input-container">
          <input
            type="text"
            placeholder="Revision ID..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch}>🔎</button>
          <button onClick={() => handleAdjacent('prev')}>⬅️</button>
          <button onClick={() => handleAdjacent('next')}>➡️</button>
          <button onClick={() => setShowPicker(true)}>Load bz2</button>
          {error && (
            <p style={{ color: 'red', margin: 0, whiteSpace: 'nowrap', alignSelf: 'center' }}>
              {error}
            </p>
          )}
        </div>
      </div>

      {showPicker && (
        <div className="modal-overlay" onClick={() => setShowPicker(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Select dump date</h3>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <div className="modal-actions">
              <button onClick={handleSubmit} disabled={!date || loading}>
                {loading ? 'Loading...' : 'Load'}
              </button>
              <button onClick={() => setShowPicker(false)}>Cancel</button>
            </div>
            {modalError && (
              <p style={{ color: 'red', marginTop: '0.5rem', fontSize: '0.9rem' }}>
                ⚠️ {modalError}
              </p>
            )}
          </div>
        </div>
      )}

      <div className="panels">
        <div
          className="clean-panel"
          onMouseUp={handleTextSelection}>
          <p style={{ whiteSpace: 'pre-wrap' }}>{articleText}</p>
        </div>

        <div className="original-panel">
          <iframe
            src={iframeSrc}
            className="original-iframe"
            title="Wikipedia Article"
          />
        </div>
      </div>
    </div>
  )
}

export default App