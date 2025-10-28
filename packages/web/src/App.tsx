import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  // Example of using environment variables
  const apiUrl = import.meta.env.VITE_API_URL;
  const appTitle = import.meta.env.VITE_APP_TITLE;

  return (
    <div className="App">
      <header className="App-header">
        <h1>{appTitle}</h1>
        <p>AI-powered conference deadline tracker</p>
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
        </div>
        <p className="info">
          API URL: {apiUrl}
        </p>
        <p className="info">
          Environment: {import.meta.env.MODE}
        </p>
      </header>
    </div>
  );
}

export default App;
