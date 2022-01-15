import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import MealDetails from './MealDetails';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Router>
          <Routes>
            <Route exact path="/" element={<Home/>}/>
            <Route path="/meals/:id/*" element={<MealDetails />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
