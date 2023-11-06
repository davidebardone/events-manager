import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

import TokenService from '../services/token.service';


const Layout = () => {
  
  const navigate = useNavigate();
  const location = useLocation();
  
  function checkToken() {
    // if not logged in redirect to /login
    if(location.pathname === '/signup' || location.pathname === '/login')
      return;
    const token = TokenService.getUser();
    if (!token) navigate('/login');
  }
  
  useEffect(() => {checkToken()});  
  
  return <Outlet />;
};

export default Layout;