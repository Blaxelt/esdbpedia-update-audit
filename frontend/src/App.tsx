import './App.css'
import { useState } from 'react'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [articleId, setArticleId] = useState('')
  const [inputValue, setInputValue] = useState('')
  const [articleText, setArticleText] = useState('')
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
      setError('Enter an article ID')
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

  return (
    <div>
      <div className="top-bar">
        <p>Article ID: {articleId}</p>
        <div className="input-container">
          <input
            type="text"
            placeholder='Article ID...'
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button onClick={handleSearch}>🔎</button>
          <button onClick={() => handleAdjacent('prev')}>⬅️</button>
          <button onClick={() => handleAdjacent('next')}>➡️</button>
          {error && <p style={{ color: 'red', margin: 0, whiteSpace: 'nowrap', alignSelf: 'center' }}>{error}</p>}
        </div>
      </div>
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
