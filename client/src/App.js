import { useEffect, useState } from "react";

const socket = new WebSocket("ws://localhost:8000/coin_list/");

function App() {
  const [coins, setCoins] = useState([]);
  const [currency, setCurrency] = useState("usd");

  useEffect(() => {
    socket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      setCoins(data["coin_list"]);
    };
  }, []);

  const handleCurrency = () => {
    const currency = document.getElementById("currency").value;
    setCurrency(currency);
    socket.send(
      JSON.stringify({
        currency: currency,
      })
    );
  };

  return (
    <div className="App">
      <label for="currency">Switch currency:</label>
      <select name="currency" id="currency" onChange={handleCurrency}>
        <option value="usd">US Dollars</option>
        <option value="eur">Euro</option>
        <option value="myr">Malaysian Ringgit</option>
        <option value="btc">Bitcoin</option>
      </select>
      <ol>
        {coins
          ? coins.map((coin) => (
              <li>
                {coin.name} | {coin.current_price} {currency.toUpperCase()}
              </li>
            ))
          : null}
      </ol>
    </div>
  );
}

export default App;
