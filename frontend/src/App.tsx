import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import TotalsCardComponent from './components/totals/TotalsCardComponent';
import SpreadsCardComponent from './components/spreads/SpreadsCardComponent.tsx';
import H2HCardComponent from './components/h2h/H2HCardComponent';
import { Box } from '@mui/material';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>

      <div className="card-component">
        <H2HCardComponent />
        <Box sx={{ height: '10px', margin: '4px 0' }} />
        <SpreadsCardComponent />
        <Box sx={{ height: '10px', margin: '4px 0' }} />
        <TotalsCardComponent />
      </div>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
