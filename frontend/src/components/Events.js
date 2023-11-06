import { useState, useEffect } from 'react';
import Container from '@mui/material/Container';    
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { DatePicker } from '@mui/x-date-pickers';

import AppToolbar from './AppToolbar';
import EventsList from './EventsList';
import EventService from '../services/event.service';


const Events = () => {

    const [events, setEvents] = useState([]);
    const [dateFilter, setDateFilter] = useState();
    const [pastFilter, setPastFilter] = useState(false);
    const [futureFilter, setFutureFilter] = useState(false);

    useEffect(() => {
        let params = {};
        if(pastFilter) params.is_past = true;
        if(futureFilter) params.is_future = true;
        if(dateFilter && dateFilter.isValid()) params.date = dateFilter.format('YYYY-MM-DD');
        
        EventService.list(params).then(
            (res) => {setEvents(res.data)}
        )
    }, [pastFilter, futureFilter, dateFilter])

    return (
        <>
        <AppToolbar/>
        
        <Container fixed>
            <Box sx={{marginTop: 8, display: 'flex', alignItems: 'center'}}>
                <Typography component="h1" variant="h3">
                    All Events ({events.length})
                </Typography>
            </Box>
            <Box sx={{maxWidth: 200}}>
                <FormGroup>
                    <FormControlLabel
                        control={<Checkbox />}
                        label="Past events"
                        value={pastFilter}
                        onChange={()=>setPastFilter(!pastFilter)}
                    />
                    <FormControlLabel
                        control={<Checkbox />}
                        label="Future events"
                        value={futureFilter}
                        onChange={()=>setFutureFilter(!futureFilter)}
                    />
                    <DatePicker
                        label="Event start date"
                        value={dateFilter}
                        onChange={(newValue) => setDateFilter(newValue)}
                        componentsProps={{
                            actionBar: {
                                actions: ['clear'],
                            },
                        }}
                    />
                </FormGroup>
            </Box>

            <EventsList events={events}/>

        </Container>
        </>
    );
};
  
export default Events;

