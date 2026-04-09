import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getEvent, addCalendarEvent, removeCalendarEvent, getCalendarEvents } from '../api/client'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import './EventDetail.css'

export default function EventDetail() {
    const { t } = useLang()
    const { user } = useAuth()
    const { id } = useParams()
    const [event, setEvent] = useState(null)
    const [loading, setLoading] = useState(true)
    const [calendarId, setCalendarId] = useState(null)

    useEffect(() => {
        getEvent(id)
            .then((res) => setEvent(res.data))
            .catch(() => setEvent(null))
            .finally(() => setLoading(false))

        if (user) {
            getCalendarEvents()
                .then((res) => {
                    const entry = (res.data.results || res.data || []).find((c) => String(c.event) === String(id))
                    if (entry) setCalendarId(entry.id)
                })
                .catch(() => { })
        }
    }, [id, user])

    const handleAddCalendar = async () => {
        try {
            const res = await addCalendarEvent({ event: parseInt(id), status: 0 })
            setCalendarId(res.data.id)
        } catch { }
    }

    const handleRemoveCalendar = async () => {
        if (!calendarId) return
        try {
            await removeCalendarEvent(calendarId)
            setCalendarId(null)
        } catch { }
    }

    if (loading) return <div className="loading-container"><div className="spinner"></div></div>
    if (!event) return <div className="detail-empty container"><p>{t.common.error}</p><Link to="/events">{t.common.back}</Link></div>

    const tr = event.translations?.[0]

    return (
        <div className="event-detail container fade-in">
            <Link to="/events" className="back-link">{t.common.back}</Link>
            {event.image && <img src={event.image} alt={tr?.name} className="detail-hero-img" />}
            <div className="detail-body">
                <h1>{tr?.name || `Event #${event.id}`}</h1>

                <div className="event-detail-meta">
                    <div className="meta-card">
                        <span className="meta-icon">📅</span>
                        <div><strong>{t.events.date}</strong><p>{event.date}</p></div>
                    </div>
                    <div className="meta-card">
                        <span className="meta-icon">🕐</span>
                        <div><strong>{t.events.time}</strong><p>{event.start_time?.slice(0, 5)}</p></div>
                    </div>
                    <div className="meta-card">
                        <span className="meta-icon">⏱️</span>
                        <div><strong>{t.events.duration}</strong><p>{event.duration} {t.events.mins}</p></div>
                    </div>
                    <div className="meta-card">
                        <span className="meta-icon">💰</span>
                        <div><strong>{t.events.cost}</strong><p>{event.cost > 0 ? `${event.cost} ${event.currency}` : t.events.free}</p></div>
                    </div>
                </div>

                {event.artist && (
                    <div className="detail-section">
                        <h3>🎤 {t.events.artist}</h3>
                        <p>{event.artist}</p>
                    </div>
                )}

                <div className="detail-section">
                    <p className="detail-addr">📍 {event.address}</p>
                    {event.link && <a href={event.link} target="_blank" rel="noreferrer" className="meta-link">🔗 Website</a>}
                </div>

                {tr?.description && (
                    <div className="detail-section">
                        <p className="detail-desc">{tr.description}</p>
                    </div>
                )}

                {user && (
                    <div className="calendar-action">
                        {calendarId ? (
                            <button className="btn btn-danger" onClick={handleRemoveCalendar}>{t.events.removeFromCalendar}</button>
                        ) : (
                            <button className="btn btn-primary" onClick={handleAddCalendar}>{t.events.addToCalendar}</button>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}
