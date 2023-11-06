import api from './api';


const create = (eventData) => {
    return api.post('/events/', eventData)
}

const get = (eventId) => {
    return api.get(`/events/${eventId}`)
}

const update = (eventId, eventData) => {
    return api.put(`/events/${eventId}/`, eventData)
}

const list = (filters) => {
    return api.get('/events', {params: filters});
}

const register = (eventId) => {
    return api.post(`/events/${eventId}/registrations`)
}

const unregister = (eventId) => {
    return api.delete(`/events/${eventId}/registrations`)
}


const EventService = {
    create,
    get,
    update,
    list,
    register,
    unregister
}

export default EventService;