import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { getEvents } from '../api/client'
import { useLang } from '../i18n/translations'
import './Calendar.css'

const YEAR = 2026

function getDaysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate()
}

function getFirstDayOfWeek(year, month) {
    const day = new Date(year, month, 1).getDay()
    return day === 0 ? 6 : day - 1 // Monday=0
}

export default function Calendar() {
    const { t } = useLang()
    const [events, setEvents] = useState([])
    const [loading, setLoading] = useState(true)
    const [hiddenEvents, setHiddenEvents] = useState(new Set())
    const todayRef = useRef(null)

    useEffect(() => {
        async function fetchAll() {
            let allEvents = []
            let page = 1
            let hasMore = true
            while (hasMore) {
                try {
                    const res = await getEvents({ page })
                    const results = res.data.results || []
                    allEvents = [...allEvents, ...results]
                    const count = res.data.count || 0
                    hasMore = allEvents.length < count
                    page++
                } catch {
                    hasMore = false
                }
            }
            setEvents(allEvents)
            setLoading(false)
        }
        fetchAll()
    }, [])

    // Build events lookup by date
    const eventsByDate = {}
    events.forEach((ev) => {
        if (hiddenEvents.has(ev.id)) return
        if (!ev.date) return
        if (!eventsByDate[ev.date]) eventsByDate[ev.date] = []
        eventsByDate[ev.date].push(ev)
    })

    const today = new Date()
    const todayStr =
        today.getFullYear() === YEAR
            ? `${YEAR}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
            : null

    const scrollToToday = () => {
        todayRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }

    const handleRemoveEvent = (e, eventId) => {
        e.preventDefault()
        e.stopPropagation()
        setHiddenEvents((prev) => new Set([...prev, eventId]))
    }

    const getName = (item) => item.translations?.[0]?.name || `Event #${item.id}`

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
            </div>
        )
    }

    return (
        <div className="calendar-page container fade-in">
            <div className="calendar-header">
                <h1>{t.calendar.title}</h1>
                {todayStr && (
                    <button className="btn btn-primary btn-sm" onClick={scrollToToday}>
                        📍 {t.calendar.today}
                    </button>
                )}
            </div>

            <div className="calendar-grid">
                {Array.from({ length: 12 }, (_, monthIdx) => {
                    const daysInMonth = getDaysInMonth(YEAR, monthIdx)
                    const firstDay = getFirstDayOfWeek(YEAR, monthIdx)
                    const isCurrentMonth =
                        today.getFullYear() === YEAR && today.getMonth() === monthIdx

                    return (
                        <div
                            key={monthIdx}
                            className={`month-card ${isCurrentMonth ? 'current-month' : ''}`}
                        >
                            <h3 className="month-title">{t.calendar.monthNames[monthIdx]}</h3>

                            <div className="weekday-row">
                                {t.calendar.weekDays.map((d) => (
                                    <span key={d} className="weekday-label">
                                        {d}
                                    </span>
                                ))}
                            </div>

                            <div className="days-grid">
                                {/* Empty cells for offset */}
                                {Array.from({ length: firstDay }, (_, i) => (
                                    <div key={`empty-${i}`} className="day-cell empty" />
                                ))}

                                {/* Day cells */}
                                {Array.from({ length: daysInMonth }, (_, dayIdx) => {
                                    const day = dayIdx + 1
                                    const dateStr = `${YEAR}-${String(monthIdx + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
                                    const dayEvents = eventsByDate[dateStr] || []
                                    const isToday = dateStr === todayStr

                                    return (
                                        <div
                                            key={day}
                                            className={`day-cell ${isToday ? 'today' : ''} ${dayEvents.length > 0 ? 'has-events' : ''}`}
                                            ref={isToday ? todayRef : null}
                                        >
                                            <span className="day-number">{day}</span>
                                            {dayEvents.length > 0 && (
                                                <div className="day-events">
                                                    {dayEvents.slice(0, 3).map((ev) => (
                                                        <Link
                                                            to={`/events/${ev.id}`}
                                                            key={ev.id}
                                                            className="event-chip"
                                                            title={getName(ev)}
                                                        >
                                                            <span className="chip-text">
                                                                {ev.start_time && (
                                                                    <span className="chip-time">
                                                                        {ev.start_time.slice(0, 5)}
                                                                    </span>
                                                                )}
                                                                <span className="chip-name">{getName(ev)}</span>
                                                            </span>
                                                            <button
                                                                className="chip-delete"
                                                                onClick={(e) => handleRemoveEvent(e, ev.id)}
                                                                title={t.calendar.deleteEvent}
                                                            >
                                                                ✕
                                                            </button>
                                                        </Link>
                                                    ))}
                                                    {dayEvents.length > 3 && (
                                                        <span className="more-events">
                                                            +{dayEvents.length - 3}
                                                        </span>
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
