import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar';
import Home from './Home';
import MealDetails from './MealDetails';
import ShoppingListDetails from './ShoppingListDetails';
import ShoppingListList from './ShoppingListList';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Router>
          <Routes>
            <Route exact path="/" element={<Home/>}/>
            <Route exact path="/shoppingLists" element={<ShoppingListList/>}/>
            <Route path="/shoppingLists/:id/*" element={<ShoppingListDetails/>}/>
            <Route path="/meals/:id/*" element={<MealDetails />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
