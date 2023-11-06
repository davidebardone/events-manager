import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';    
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import AppToolbar from './AppToolbar';
import EventsList from './EventsList';
import EventService from '../services/event.service';


const MyEvents = () => {

    const [events, setEvents] = useState([]);

    useEffect(() => {
        EventService.listMine().then(
            (res) => {setEvents(res.data)}
        )
    }, [])

    return (
        <>
        <AppToolbar/>
        
        <Container fixed>
            <Box sx={{margin: 8, display: 'flex', alignItems: 'center'}}>
                <Typography component="h1" variant="h3">
                    My Events
                </Typography>
            </Box>

            <EventsList events={events}/>

        </Container>
        </>
    );
};
  
export default MyEvents;
