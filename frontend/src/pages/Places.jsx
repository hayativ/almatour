import { useMemo, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { getPlaces } from '../api/client'
import { useLang } from '../i18n/translations'
import { useTheme } from '../theme/ThemeContext'
import './Places.css'

const ALMATY_CENTER = [43.238, 76.9286]
const DEFAULT_ZOOM = 13

/* Map lang code to DB language_id: en=1, ru=2, kz=3 */
const LANG_ID_MAP = { en: 1, ru: 2, kz: 3 }

export default function Places() {
    const { t, lang } = useLang()
    const { isDark } = useTheme()
    const navigate = useNavigate()
    const [places, setPlaces] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
        getPlaces()
            .then((res) => {
                const data = res.data.results || res.data
                const withCoords = data.filter(p => p.lat && p.lng)
                setPlaces(withCoords)
            })
            .catch(() => setError(true))
            .finally(() => setLoading(false))
    }, [])

    const markers = useMemo(
        () =>
            places.map((p) => {
                const langId = LANG_ID_MAP[lang] ?? 1
                const tr =
                    p.translations?.find(t => t.language_id === langId) ||
                    p.translations?.[0]
                return (
                    <CircleMarker
                        key={p.id}
                        center={[p.lat, p.lng]}
                        radius={9}
                        pathOptions={{
                            color: '#3b82f6',
                            fillColor: '#3b82f6',
                            fillOpacity: 0.85,
                            weight: 3,
                            opacity: 1,
                        }}
                        eventHandlers={{
                            click: (e) => {
                                if (window.innerWidth <= 768) {
                                    e.target.openPopup()
                                } else {
                                    navigate(`/places/${p.id}`)
                                }
                            },
                            mouseover: (e) => {
                                if (window.innerWidth > 768) {
                                    e.target.setStyle({ radius: 12, fillOpacity: 1 })
                                    e.target.openPopup()
                                }
                            },
                            mouseout: (e) => {
                                if (window.innerWidth > 768) {
                                    e.target.setStyle({ radius: 9, fillOpacity: 0.85 })
                                }
                            },
                        }}
                    >
                        <Popup>
                            <div className="map-popup-content">
                                <strong>{tr?.name || `Place #${p.id}`}</strong>
                                <p>{p.address}</p>
                                <button
                                    className="map-popup-btn"
                                    onClick={() => navigate(`/places/${p.id}`)}
                                >
                                    {t.places.viewDetails || 'View Details'}
                                </button>
                            </div>
                        </Popup>
                    </CircleMarker>
                )
            }),
        [places, navigate, lang, t],
    )

    if (loading)
        return (
            <div className="loading-container container">
                <div className="spinner"></div>
            </div>
        )

    return (
        <div className="places-page container fade-in">
            <h1>{t.places.mapTitle}</h1>

            <div className="map-wrapper">
                <div className="map-container">
                    <MapContainer
                        center={ALMATY_CENTER}
                        zoom={DEFAULT_ZOOM}
                        scrollWheelZoom={true}
                        className="leaflet-map"
                    >
                        <TileLayer
                            attribution='&copy; <a href="https://carto.com/">CARTO</a>'
                            url={isDark
                                ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                                : "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
                            }
                        />
                        {markers}
                    </MapContainer>
                </div>
            </div>

            <div className="map-info">
                <p className="map-label">Almaty, Kazakhstan</p>
                <p className="map-coords">43.2380° N, 76.9286° E</p>
                <p className="map-count">{places.length} {t.places.title?.toLowerCase?.() || 'places'}</p>
            </div>
        </div>
    )
}
