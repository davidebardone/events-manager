import { useEffect, useState } from 'react';
import dayjs from 'dayjs';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate } from "react-router-dom";

import EventService from '../services/event.service';


const EventEditor = ({event}) => {
 
    const navigate = useNavigate();
    
    const [creationError, setCreationError] = useState("");
    
    const [name, setName] = useState('');
    const [desc, setDesc] = useState('');
    const [startDate, setStartDate] = useState(dayjs());
    const [endDate, setEndDate] = useState(dayjs());
    const [capacity, setCapacity] = useState(10);

    const handleCapacityChange = (event) => {
        setCapacity(event.target.value);
    }

    const buttonText = () => {
        return event !== undefined ? 'Update Event' : 'Create Event';
    }

    useEffect(() => {
        if(event !== undefined){
            setName(event.name);
            setDesc(event.desc);
            setCapacity(event.max_capacity);
            setStartDate(dayjs(event.start_date));
            setEndDate(dayjs(event.end_date));
        }
    }, [event])

    const handleSubmit = (ev) => {
        setCreationError("");
        ev.preventDefault();
        if(!startDate){
            setCreationError("Please input start date");
        } else if (!endDate){
            setCreationError("Please input end date");
        } else if (startDate > endDate){
            setCreationError("Start date must be before end date");
        } else {
            const data = new FormData(ev.currentTarget);
            const eventData = {
                'name': data.get('name'),
                'desc': data.get('description'),
                'max_capacity': capacity,
                'start_date': startDate.format('YYYY-MM-DD'),
                'end_date': endDate.format('YYYY-MM-DD')
            }
            if(event !== undefined){
                // update event
                EventService.update(event.id, eventData)
                    .then((res) => navigate('/myevents'))
                    .catch((err) => setCreationError(JSON.stringify(err.response.data)));
            } else {
                // create new event
                EventService.create(eventData)
                    .then((res) => navigate('/myevents'))
                    .catch((err) => setCreationError(JSON.stringify(err.response.data)));
            }
        }
    }

    return ( 

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                <Grid container spacing={2}>
                
                    <Grid item xs={12} sm={6}>
                        <TextField
                            name="name"
                            required
                            fullWidth
                            id="name"
                            label="Event Name"
                            autoFocus
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                    </Grid>
                    
                    <Grid item xs={12}>
                        <TextField
                            required
                            fullWidth
                            id="description"
                            label="Event Description"
                            name="description"
                            multiline
                            rows="2"
                            value={desc}
                            onChange={e => setDesc(e.target.value)}
                        />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                        <DatePicker
                            label="Event start date"
                            value={startDate}
                            onChange={(newValue) => setStartDate(newValue)}
                        />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                        <DatePicker
                            label="Event end date"
                            value={endDate}
                            onChange={(newValue) => setEndDate(newValue)}
                        />
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                        Maximum Capacity: <Select
                            id="capacity"
                            value={capacity}
                            onChange={handleCapacityChange}
                        >
                            <MenuItem value={10}>10</MenuItem>
                            <MenuItem value={50}>50</MenuItem>
                            <MenuItem value={100}>100</MenuItem>
                            <MenuItem value={200}>200</MenuItem>
                        </Select>
                    </Grid>


                </Grid>
                
                <Typography color="red">
                    {creationError}
                </Typography>
                
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                >
                    {buttonText()}
                </Button>

            </Box>

    )
};
  
export default EventEditor;