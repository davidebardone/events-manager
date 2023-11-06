import Container from '@mui/material/Container';    
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import AppToolbar from './AppToolbar';
import EventEditor from './EventEditor'


const Home = () => {
 
    return ( 
        <>
        <AppToolbar/>
        
        <Container fixed>
            <Box sx={{marginTop: 8, display: 'flex', alignItems: 'center'}}>
                <Typography component="h1" variant="h3">
                    EventManager
                </Typography>
            </Box>

            <EventEditor />

        </Container>
        </>
    )
};
  
export default Home;