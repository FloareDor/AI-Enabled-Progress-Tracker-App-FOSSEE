import { Link } from "react-router-dom";
// import Login from "./login";
import { Route, Routes } from "react-router-dom";
import { useState } from "react";
// import logoMain from "/home/maneesh/Desktop/rateprofs/client/src/assets/logoMain.svg"

const NavBar = () =>{
    return (
    <div className="navhead">
        <div className="companyName">
            <h1>AI Progress Tracker</h1>
            <button className="loginBut">Login</button>
        </div>
        
    </div>
    
    );
  }
  export default NavBar;