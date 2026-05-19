/**
 * Weather API service — Open-Meteo (no key required)
 * Fetches daily forecast for Almaty, Kazakhstan.
 */

const ALMATY_LAT = 43.2375
const ALMATY_LON = 76.9457
const BASE_URL = 'https://api.open-meteo.com/v1/forecast'

/**
 * WMO weather interpretation codes → label keys used in translations.
 * https://open-meteo.com/en/docs  (Weather variable documentation section)
 */
const WMO_CODE_MAP = {
    0: 'clear',
    1: 'mainlyClear',
    2: 'partlyCloudy',
    3: 'overcast',
    45: 'fog',
    48: 'fog',
    51: 'drizzle',
    53: 'drizzle',
    55: 'drizzle',
    56: 'freezingDrizzle',
    57: 'freezingDrizzle',
    61: 'rain',
    63: 'rain',
    65: 'heavyRain',
    66: 'freezingRain',
    67: 'freezingRain',
    71: 'snow',
    73: 'snow',
    75: 'heavySnow',
    77: 'snowGrains',
    80: 'rainShowers',
    81: 'rainShowers',
    82: 'heavyRainShowers',
    85: 'snowShowers',
    86: 'snowShowers',
    95: 'thunderstorm',
    96: 'thunderstormHail',
    99: 'thunderstormHail',
}

/**
 * Map WMO code to an emoji icon.
 */
const WMO_ICON_MAP = {
    0: '☀️',
    1: '🌤️',
    2: '⛅',
    3: '☁️',
    45: '🌫️',
    48: '🌫️',
    51: '🌦️',
    53: '🌦️',
    55: '🌦️',
    56: '🌧️',
    57: '🌧️',
    61: '🌧️',
    63: '🌧️',
    65: '🌧️',
    66: '🌧️',
    67: '🌧️',
    71: '🌨️',
    73: '🌨️',
    75: '🌨️',
    77: '🌨️',
    80: '🌦️',
    81: '🌦️',
    82: '🌧️',
    85: '🌨️',
    86: '🌨️',
    95: '⛈️',
    96: '⛈️',
    99: '⛈️',
}

/**
 * Fetch weather data from Open-Meteo.
 * Returns { days: [ { date, tempMax, tempMin, weatherCode, weatherKey, icon, precipProbability } ] }
 * Index 0 = yesterday, index 1 = today, 2..7 = next 6 days.
 */
export async function fetchAlmatyWeather() {
    const params = new URLSearchParams({
        latitude: ALMATY_LAT,
        longitude: ALMATY_LON,
        daily: [
            'temperature_2m_max',
            'temperature_2m_min',
            'weather_code',
            'precipitation_probability_max',
        ].join(','),
        past_days: 1,
        forecast_days: 7,
        timezone: 'Asia/Almaty',
    })

    const res = await fetch(`${BASE_URL}?${params}`)
    if (!res.ok) {
        throw new Error(`Weather API error: ${res.status}`)
    }

    const data = await res.json()
    const d = data.daily

    const days = d.time.map((date, i) => ({
        date,
        tempMax: Math.round(d.temperature_2m_max[i]),
        tempMin: Math.round(d.temperature_2m_min[i]),
        weatherCode: d.weather_code[i],
        weatherKey: WMO_CODE_MAP[d.weather_code[i]] || 'clear',
        icon: WMO_ICON_MAP[d.weather_code[i]] || '🌡️',
        precipProbability: d.precipitation_probability_max[i] ?? 0,
    }))

    return { days }
}
