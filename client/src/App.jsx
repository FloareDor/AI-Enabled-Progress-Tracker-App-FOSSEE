import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { Route, Routes } from "react-router-dom";
import Home from "./components/home";
import NavBar from "./components/navbar";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <NavBar></NavBar>
      {/* <MainPageCard></MainPageCard> */}
      <Routes>
        <Route path="/" element={<Home/>}/>
      </Routes>
      {/* <Footer></Footer> */}
    </div>
  );
}

export default App;