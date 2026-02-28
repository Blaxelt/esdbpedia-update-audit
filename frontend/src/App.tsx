import './App.css'
import { useState } from 'react'

function App() {
  const [articleId, setArticleId] = useState('171311417')
  const [inputValue, setInputValue] = useState('')
  const [error, setError] = useState('')

  const handleSearch = () => {
    if (!inputValue.trim()) {
      setError('Enter an article ID')
      return
    }
    if (isNaN(Number(inputValue))) {
      setError('ID must be a number')
      return
    }
    setError('')
    setArticleId(inputValue)
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
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
      </div>
      <div className="panels">
        <div className="clean-panel">
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
