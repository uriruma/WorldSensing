import logo from '../logo.svg';
import '../App.css';

function Home () {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Go to the url: <code>"/api"</code> to show the API control panel.
        </p>
        <p>
          Go to the url: <code>"/about"</code> to learn more about the API.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default Home;