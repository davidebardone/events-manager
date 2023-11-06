//import logo from './logo.svg';
//import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout.js";
import Home from "./components/Home.js";
import Events from "./components/Events.js";
import EditEvent from "./components/EditEvent.js";
import MyEvents from "./components/MyEvents.js";
import Login from "./components/Login.js";
import SignUp from "./components/SignUp.js";

//import { createTheme, ThemeProvider } from '@mui/material/styles';

//const defaultTheme = createTheme();

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="events" element={<Events />} />
          <Route path="myevents" element={<MyEvents />} />
          <Route path="edit_event" element={<EditEvent />} />
          <Route path="*" element={<Home />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
