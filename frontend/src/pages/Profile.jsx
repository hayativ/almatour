import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import { getCalendarEvents, removeCalendarEvent, getEvent } from '../api/client'
import './Profile.css'

export default function Profile() {
    const { t } = useLang()
    const { user, loading: authLoading, logout } = useAuth()
    const navigate = useNavigate()
    const [calEvents, setCalEvents] = useState([])
    const [loadingCal, setLoadingCal] = useState(true)

    useEffect(() => {
        if (!authLoading && !user) {
            navigate('/login')
            return
        }
        if (user) {
            getCalendarEvents()
                .then(async (res) => {
                    const items = res.data.results || res.data || []
                    const enriched = await Promise.all(
                        items.map(async (ce) => {
                            try {
                                const ev = await getEvent(ce.event)
                                return { ...ce, eventData: ev.data }
                            } catch {
                                return { ...ce, eventData: null }
                            }
                        })
                    )
                    setCalEvents(enriched)
                })
                .catch(() => setCalEvents([]))
                .finally(() => setLoadingCal(false))
        }
    }, [user, authLoading, navigate])

    const handleLogout = () => {
        logout()
        navigate('/')
    }

    const handleRemove = async (id) => {
        await removeCalendarEvent(id)
        setCalEvents((prev) => prev.filter((c) => c.id !== id))
    }

    if (authLoading) return <div className="loading-container"><div className="spinner"></div></div>
    if (!user) return null

    return (
        <div className="profile-page container fade-in">
            <div className="profile-header">
                <div className="profile-avatar">{user.username?.[0]?.toUpperCase() || '?'}</div>
                <div>
                    <h1>{t.profile.title}</h1>
                    <p className="profile-email">{user.email}</p>
                </div>
            </div>

            <div className="profile-info-grid">
                <div className="info-card">
                    <span className="info-label">{t.profile.username}</span>
                    <span className="info-value">{user.username}</span>
                </div>
                <div className="info-card">
                    <span className="info-label">{t.profile.email}</span>
                    <span className="info-value">{user.email}</span>
                </div>
                <div className="info-card">
                    <span className="info-label">{t.profile.phone}</span>
                    <span className="info-value">{user.phone}</span>
                </div>
            </div>

            <button className="btn btn-danger" onClick={handleLogout}>{t.profile.signOut}</button>

            <section className="calendar-section">
                <h2>{t.profile.myCalendar}</h2>
                {loadingCal ? (
                    <div className="loading-container"><div className="spinner"></div></div>
                ) : calEvents.length === 0 ? (
                    <p className="no-results">{t.profile.noCalendar}</p>
                ) : (
                    <div className="cal-list">
                        {calEvents.map((ce) => {
                            const name = ce.eventData?.translations?.[0]?.name || `Event #${ce.event}`
                            return (
                                <div key={ce.id} className="cal-item card">
                                    <div className="cal-info">
                                        <Link to={`/events/${ce.event}`}><h4>{name}</h4></Link>
                                        {ce.eventData?.date && <span className="cal-date">📅 {ce.eventData.date}</span>}
                                    </div>
                                    <button className="btn btn-sm btn-danger" onClick={() => handleRemove(ce.id)}>✕</button>
                                </div>
                            )
                        })}
                    </div>
                )}
            </section>
        </div>
    )
}
