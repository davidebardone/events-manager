import Container from '@mui/material/Container';    
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import AppToolbar from './AppToolbar.js';

const Home = () => {
    

    return ( 
        <>
        <AppToolbar/>
        <Container fixed>
            <Box sx={{marginTop: 8, display: 'flex', alignItems: 'center'}}>
                <Typography component="h1" variant="h2">
                    EventManager App
                </Typography>
            </Box>
        </Container>
        </>
    )
};
  
export default Home;