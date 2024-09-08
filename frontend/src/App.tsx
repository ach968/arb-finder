import { useState, useEffect } from 'react';
import './App.css';
import TotalsCardComponent from './components/totals/TotalsCardComponent';
import SpreadsCardComponent from './components/spreads/SpreadsCardComponent';
import H2HCardComponent from './components/h2h/H2HCardComponent';

function App() {
  const [data, setData] = useState<any[]>([]);  // State to hold the fetched data
  const [loading, setLoading] = useState(true);  // State to track loading status
  const [error, setError] = useState<Error | null>(null);  // State to track errors

  useEffect(() => {
    // Fetch data from the backend
    fetch('http://localhost:5001/api/fetch_arb_data/')  // Replace with your backend URL
      .then(response => response.json())
      .then(data => {
        setData(data);  // Save the fetched data in the state
        setLoading(false);  // Set loading to false
      })
      .catch(err => {
        setError(err);  // Handle errors if any
        setLoading(false);
      });
  }, []);  // Empty dependency array means this effect runs once when the component mounts

  if (loading) return <p>Loading...</p>;  // Show a loading message while data is being fetched
  if (error) return <p>Error: {error.message}</p>;  // Show an error message if the fetch fails

  // Filter data by market type
  const h2hData = data.filter(item => item.market === 'h2h');
  const spreadsData = data.filter(item => item.market === 'spreads');
  const totalsData = data.filter(item => item.market === 'totals');

  return (
    <>
      <h2 style={{ textAlign: 'center', margin: '20px 0' }}>arbitrage opportunities</h2>
      <hr style={{ margin: '10px 40px' }} />
      <div className="card-component">
        {/* Render H2H Cards */}
        {h2hData.length > 0 && (
          <>
            {h2hData.map((item) => (
              <div key={item.id}>
                <H2HCardComponent data={item} />
              </div>
            ))}
          </>
        )}

        {/* Render Spreads Cards */}
        {spreadsData.length > 0 && (
          <>
            {spreadsData.map((item) => (
              <div key={item.id}>
                <SpreadsCardComponent data={item} />
              </div>
            ))}
          </>
        )}

        {/* Render Totals Cards */}
        {totalsData.length > 0 && (
          <>
            {totalsData.map((item) => (
              <div key={item.id}>
                <TotalsCardComponent data={item} />
              </div>
            ))}
          </>
        )}
      </div>
    </>
  );
}

export default App;
