import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getPlace } from '../api/client'
import { useLang } from '../i18n/translations'
import './PlaceDetail.css'

export default function PlaceDetail() {
    const { t } = useLang()
    const { id } = useParams()
    const [place, setPlace] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        getPlace(id)
            .then((res) => setPlace(res.data))
            .catch(() => setPlace(null))
            .finally(() => setLoading(false))
    }, [id])

    if (loading) return <div className="loading-container"><div className="spinner"></div></div>
    if (!place) return <div className="detail-empty container"><p>{t.common.error}</p><Link to="/places">{t.common.back}</Link></div>

    const tr = place.translations?.[0]

    return (
        <div className="place-detail container fade-in">
            <Link to="/places" className="back-link">{t.common.back}</Link>
            {place.image && <img src={place.image} alt={tr?.name} className="detail-hero-img" />}
            <div className="detail-body">
                <h1>{tr?.name || `Place #${place.id}`}</h1>
                <div className="detail-meta">
                    <span className="meta-item">📍 {place.address}</span>
                    {place.link && <a href={place.link} target="_blank" rel="noreferrer" className="meta-link">🔗 Website</a>}
                </div>
                {tr?.timetable && (
                    <div className="detail-section">
                        <h3>🕐 Schedule</h3>
                        <p>{tr.timetable}</p>
                    </div>
                )}
                {tr?.description && (
                    <div className="detail-section">
                        <p className="detail-desc">{tr.description}</p>
                    </div>
                )}
            </div>
        </div>
    )
}
