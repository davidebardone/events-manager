import { useEffect, useState } from 'react';

import Container from '@mui/material/Container';    
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useParams } from 'react-router-dom';

import AppToolbar from './AppToolbar';
import EventEditor from './EventEditor'
import EventService from '../services/event.service';

const EditEvent = () => {

    const { eventId } = useParams();

    const [event, setEvent] = useState();

    useEffect(() => {
        if(eventId){
            EventService.get(eventId).then(
                (res) => {
                    let event = res.data;
                    setEvent(event)
                }
            )
        }
    }, [eventId]);

    return ( 
        <>
        <AppToolbar/>
        
        <Container fixed>
            <Box sx={{marginTop: 8, display: 'flex', alignItems: 'center'}}>
                <Typography component="h1" variant="h3">
                    Edit event
                </Typography>
            </Box>

            {event && <EventEditor event={event}/>}

        </Container>
        </>
    )
};
  
export default EditEvent;
