import { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';

import EventService from '../services/event.service';
import dayjs from 'dayjs';


const EventsList = ({ events }) => {

    const [eventsList, setEventsList] = useState([]);
    
    useEffect(() => {
        setEventsList(events);
    }, [events])

    const handleRegister = (event) => {
        EventService.register(event.id).then(
            (res) => {
                EventService.get(event.id).then((res) => {
                    setEventsList(
                        eventsList.map((item) => item.id===res.data.id ? res.data : item)
                    );
                });
            }
        );
    }
    
    const handleUnregister = (event) => {
        EventService.unregister(event.id).then(
            (res) => {
                EventService.get(event.id).then((res) => {
                    setEventsList(
                        eventsList.map((item) => item.id===res.data.id ? res.data : item)
                    );
                });
            }
        );
    }

    const canUnregister = (event) => {
        return dayjs(event.start_date) > dayjs() && event.is_attendee;
    }
    
    const canRegister = (event) => {
        return dayjs(event.start_date) > dayjs() && !event.is_attendee && event.max_capacity > event.attendees.length;
    }

    return (
        <>

        <Grid container spacing={3}>
        
        {eventsList.map(event => (

            <Grid item xs={12} sm={4} key={event.id}>
                <Card sx={{ minWidth: 275, margin: 2}}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            {event.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            {event.desc}
                        </Typography>
                        <Typography variant="body2">
                            Start: {event.start_date}
                        </Typography>
                        <Typography variant="body2">
                            End: {event.end_date}
                        </Typography>
                        <Typography variant="body2">
                            Capacity: {event.attendees.length}/{event.max_capacity}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        { 
                            dayjs(event.start_date) > dayjs() && event.is_author &&
                            <Button size="small" href={'/editevent/'+event.id}>Edit</Button>
                        }
                        {
                            canUnregister(event) &&
                            <Button size="small" color="error" onClick={() => handleUnregister(event)}>Unregister</Button>
                        }
                        {
                            canRegister(event) &&
                            <Button size="small" onClick={() => handleRegister(event)}>Register</Button>
                        }
                    </CardActions>
                </Card>
            </Grid>
        ))}

        </Grid>
        </>
    )
}

export default EventsList;
