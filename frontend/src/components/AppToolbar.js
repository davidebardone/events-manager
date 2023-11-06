import Container from '@mui/material/Container';    
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import HomeIcon from '@mui/icons-material/Home';
import { useNavigate } from "react-router-dom";

import TokenService from '../services/token.service';

const AppToolbar = () => {

  const navigate = useNavigate();

  const logoutHandler = (event) => {
    TokenService.removeUser();
    navigate('/login');
  }

  return (
    <AppBar position="static">
       <Container maxWidth="xl">
        <Toolbar disableGutters>

            <Button
                size="large"
                href="/"
                color="inherit"
            >
                <HomeIcon /> Home
            </Button>
          
            <Button
                size="large"
                href="/events"
                color="inherit"
            >
                Events
            </Button>
          
            <Button
                size="large"
                href="/myevents"
                color="inherit"
            >
              My Events
            </Button>
          
            <Box sx={{ ml: 'auto' }}>
              <Button
                  size="large"
                  onClick={logoutHandler}
                  color="inherit"
              >
                Logout
              </Button>
            </Box>

        </Toolbar>

      </Container>
    </AppBar>

  )
};

export default AppToolbar;