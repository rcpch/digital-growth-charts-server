// React
import React, { useState } from "react";
import "./App.css";

// React Router DOM
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

// RCPCH Components
import "./components/MeasurementForm";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Results from "./pages/Results";
import Spreadsheet from "./pages/Spreadsheet";
import SerialResults from "./pages/SerialResults";
import HeaderBar from "./components/HeaderBar";
import Technical from "./components/Technical";

function App() {
  const [toggle, setToggle] = useState(false);

  function toggleTechnical() {
    setToggle(!toggle);
  }

  return (
    <div className="App">
      <div>
        <Router>
          <HeaderBar toggleTechnical={toggleTechnical} />
          <Switch>
            <Route exact path="/">
              <Home />
            </Route>
            <Route path="/results">
              <Results />
            </Route>
            <Route path="/serial_results">
              <SerialResults />
            </Route>
            <Route path="/spreadsheet">
              <Spreadsheet />
            </Route>
          </Switch>
        </Router>
        <Technical
          technicalSidebarVisible={toggle}
          toggleTechnical={toggleTechnical}
        />
        <Footer />
      </div>
    </div>
  );
}

export default App;
