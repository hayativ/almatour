import { useMemo, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { getPlaces } from '../api/client'
import { useLang } from '../i18n/translations'
import './Places.css'

/* Fix default marker icon paths broken by bundlers */
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
})

const ALMATY_CENTER = [43.238, 76.9286]
const DEFAULT_ZOOM = 13

export default function Places() {
    const { t, lang } = useLang()
    const navigate = useNavigate()
    const [places, setPlaces] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
        getPlaces()
            .then((res) => {
                // Filter out places without coordinates
                const withCoords = res.data.filter(p => p.latitude && p.longitude)
                setPlaces(withCoords)
            })
            .catch(() => setError(true))
            .finally(() => setLoading(false))
    }, [])

    const markers = useMemo(
        () =>
            places.map((p) => {
                const tr = p.translations?.find(t => t.language_id === (lang === 'en' ? 0 : lang === 'ru' ? 1 : 2)) || p.translations?.[0]
                return (
                    <Marker key={p.id} position={[p.latitude, p.longitude]}>
                        <Popup>
                            <div className="map-popup-content">
                                <strong>{tr?.name || `Place #${p.id}`}</strong>
                                <p>{p.address}</p>
                                <button
                                    className="map-popup-btn"
                                    onClick={() => navigate(`/places/${p.id}`)}
                                >
                                    {t.common.viewAll || 'View Details'}
                                </button>
                            </div>
                        </Popup>
                    </Marker>
                )
            }),
        [places, navigate, lang, t],
    )

    if (loading) return <div className="loading-container container"><div className="spinner"></div></div>

    return (
        <div className="places-page container">
            <h1>{t.places.mapTitle}</h1>

            <div className="map-container">
                <MapContainer
                    center={ALMATY_CENTER}
                    zoom={DEFAULT_ZOOM}
                    scrollWheelZoom={true}
                    className="leaflet-map"
                >
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {markers}
                </MapContainer>
            </div>

            <div className="map-info">
                <p className="map-label">📍 Almaty, Kazakhstan</p>
                <p className="map-coords">43.2380° N, 76.9286° E</p>
            </div>
        </div>
    )
}
