import axios from 'axios'

const API_BASE = '/api/v1'

const client = axios.create({
    baseURL: API_BASE,
    headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

client.interceptors.response.use(
    (res) => res,
    async (error) => {
        const original = error.config
        if (error.response?.status === 401 && !original._retry) {
            original._retry = true
            const refresh = localStorage.getItem('refresh_token')
            if (refresh) {
                try {
                    const { data } = await axios.post(`${API_BASE}/users/token/refresh/`, { refresh })
                    localStorage.setItem('access_token', data.access)
                    original.headers.Authorization = `Bearer ${data.access}`
                    return client(original)
                } catch {
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    window.location.href = '/login'
                }
            }
        }
        return Promise.reject(error)
    }
)

// Places
export const getPlaces = (params) => client.get('/places/', { params })
export const getPlace = (id) => client.get(`/places/${id}/`)

// Events
export const getEvents = (params) => client.get('/events/events/', { params })
export const getEvent = (id) => client.get(`/events/events/${id}/`)

// Calendar
export const getCalendarEvents = () => client.get('/events/calendar/')
export const addCalendarEvent = (data) => client.post('/events/calendar/', data)
export const removeCalendarEvent = (id) => client.delete(`/events/calendar/${id}/`)

// Info
export const getSouvenirs = () => client.get('/info/souvenirs/')
export const getApps = () => client.get('/info/apps/')
export const getAdvertisements = () => client.get('/info/advertisements/')

// Auth
export const login = (data) => axios.post(`${API_BASE}/users/token/`, data)
export const register = (data) => axios.post(`${API_BASE}/users/register/`, data)
export const getProfile = () => client.get('/users/profile/')
export const updateProfile = (data) => client.patch('/users/profile/', data)

export default client
