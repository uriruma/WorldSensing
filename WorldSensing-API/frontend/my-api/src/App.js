import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import About from './components/about';
import ApiControlPanel from './components/api-control-panel';
import { Link } from 'react-router-dom'
import './App.css'

function App() {
  // const location = useLocation();

  return (
    <Router>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/api">API Control Panel</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/api" element={<ApiControlPanel />} />
      </Routes>
    </Router>
  );
}
 
export default App;
