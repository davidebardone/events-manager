import './App.css';

import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout.js";
import Home from "./components/Home.js";
import Events from "./components/Events.js";
import EditEvent from "./components/EditEvent.js";
import MyEvents from "./components/MyEvents.js";
import Login from "./components/Login.js";
import SignUp from "./components/SignUp.js";


function App() {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="allevents" element={<Events />} />
          <Route path="myevents" element={<MyEvents />} />
          <Route path="editevent/:eventId" element={<EditEvent />} />
          <Route path="*" element={<Home />} />
        </Route>
      </Routes>
    </BrowserRouter>

    </LocalizationProvider>

  );
}

export default App;
