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

  const loadArticle = (id: string) => {
    setError('')
    setArticleId(id)
    setInputValue(id)
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
    if (!date) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/articles/load?date=${date.replace(/-/g, '')}`, {
        method: "POST",
      });

      const data = await response.json();
      console.log("Respuesta:", data);
      setShowPicker(false);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="top-bar">
        <p>Revision ID: {articleId}</p>
        <div className="input-container">
          <input
            type="text"
            placeholder='Revision ID...'
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button onClick={handleSearch}>🔎</button>
          <button onClick={() => handleAdjacent('prev')}>⬅️</button>
          <button onClick={() => handleAdjacent('next')}>➡️</button>
          <button onClick={() => setShowPicker(true)}>Load bz2</button>
          {error && <p style={{ color: 'red', margin: 0, whiteSpace: 'nowrap', alignSelf: 'center' }}>{error}</p>}
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
          </div>
        </div>
      )}
      <div className="panels">
        <div className="clean-panel">
          <p style={{ whiteSpace: 'pre-wrap' }}>{articleText}</p>
        </div>
        <div className="original-panel">
          <iframe
            src={`https://es.wikipedia.org/w/index.php?oldid=${articleId}`}
            className="original-iframe"
            title="Wikipedia Article"
          />
        </div>
      </div>
    </div>
  )
}

export default App
