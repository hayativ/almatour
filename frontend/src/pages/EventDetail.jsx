import { useState, useEffect, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getEvent, addCalendarEvent, removeCalendarEvent, getCalendarEvents } from '../api/client'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import { formatDateCIS } from '../utils/dateFormat'
import './EventDetail.css'

export default function EventDetail() {
    const { t, lang } = useLang()
    const { user } = useAuth()
    const { id } = useParams()
    const [event, setEvent] = useState(null)
    const [loading, setLoading] = useState(true)
    const [calendarId, setCalendarId] = useState(null)
    const [copied, setCopied] = useState(false)

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

    const copyAddress = useCallback(() => {
        if (!event?.address) return
        navigator.clipboard.writeText(event.address).then(() => {
            setCopied(true)
            setTimeout(() => setCopied(false), 2000)
        })
    }, [event])

    if (loading) return <div className="loading-container"><div className="spinner"></div></div>
    if (!event) return <div className="detail-empty container"><p>{t.common.error}</p><Link to="/events">{t.common.back}</Link></div>

    const LANG_ID_MAP = { en: 0, ru: 1, kz: 2, tr: 3, zh: 4, hi: 5, ko: 6 }
    const langId = LANG_ID_MAP[lang] ?? 0
    const tr = event.translations?.find(x => x.language_id === langId) || event.translations?.[0]

    return (
        <div className="event-detail container fade-in">
            <Link to="/events" className="back-link">{t.common.back}</Link>

            {event.image && (
                <div className="detail-hero">
                    <img src={event.image} alt={tr?.name} className="detail-hero-img" />
                </div>
            )}

            <div className="detail-body">
                <h1>{tr?.name || `Event #${event.id}`}</h1>

                {/* Date */}
                <div className="detail-card">
                    <div className="detail-card-content">
                        <span className="detail-card-label">{t.events.date}</span>
                        <span className="detail-card-value">{formatDateCIS(event.date)}</span>
                    </div>
                </div>

                {/* Time */}
                <div className="detail-card">
                    <div className="detail-card-content">
                        <span className="detail-card-label">{t.events.time}</span>
                        <span className="detail-card-value">{event.start_time?.slice(0, 5)}</span>
                    </div>
                </div>

                {/* Duration */}
                <div className="detail-card">
                    <div className="detail-card-content">
                        <span className="detail-card-label">{t.events.duration}</span>
                        <span className="detail-card-value">{event.duration} {t.events.mins}</span>
                    </div>
                </div>

                {/* Cost */}
                <div className="detail-card">
                    <div className="detail-card-content">
                        <span className="detail-card-label">{t.events.cost}</span>
                        <span className="detail-card-value">{event.cost > 0 ? `${event.cost} ${event.currency}` : t.events.free}</span>
                    </div>
                </div>

                {/* Artist */}
                {event.artist && (
                    <div className="detail-card">
                        <div className="detail-card-content">
                            <span className="detail-card-label">{t.events.artist}</span>
                            <span className="detail-card-value">{event.artist}</span>
                        </div>
                    </div>
                )}

                {/* Address with copy button */}
                {event.address && (
                    <div className="detail-card">
                        <div className="detail-card-content">
                            <span className="detail-card-label">{t.places.addressLabel || 'Address'}</span>
                            <span className="detail-card-value">{event.address}</span>
                        </div>
                        <button
                            className={`copy-btn ${copied ? 'copied' : ''}`}
                            onClick={copyAddress}
                            title={t.places.copyAddress || 'Copy address'}
                        >
                            {copied ? '✓' : '🔗'}
                        </button>
                    </div>
                )}

                {/* Website link */}
                {event.link && (
                    <div className="detail-card">
                        <div className="detail-card-content">
                            <span className="detail-card-label">{t.places.website || 'Website'}</span>
                            <a
                                href={event.link}
                                target="_blank"
                                rel="noreferrer"
                                className="detail-card-link"
                            >
                                {event.link.replace(/^https?:\/\//, '').replace(/\/$/, '')}
                            </a>
                        </div>
                    </div>
                )}

                {/* Description */}
                {tr?.description && (
                    <div className="detail-description">
                        <p>{tr.description}</p>
                    </div>
                )}

                {/* Calendar action */}
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

            {/* Copied toast */}
            {copied && (
                <div className="copy-toast fade-in">
                    ✓ {t.places.addressCopied || 'Address copied!'}
                </div>
            )}
        </div>
    )
}
