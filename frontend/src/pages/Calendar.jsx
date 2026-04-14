import { useState, useEffect, useCallback, useRef } from 'react'
import { Link } from 'react-router-dom'
import { getCalendarEvents, addCalendarEvent, removeCalendarEvent, getEvents, getEvent } from '../api/client'
import { useLang } from '../i18n/translations'
import './Calendar.css'

function getDaysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate()
}

function getFirstDayOfWeek(year, month) {
    const day = new Date(year, month, 1).getDay()
    return day === 0 ? 6 : day - 1 // Monday=0
}

export default function Calendar() {
    const { t } = useLang()
    const now = new Date()
    const [currentYear, setCurrentYear] = useState(now.getFullYear())
    const [currentMonth, setCurrentMonth] = useState(now.getMonth())
    const [calendarEntries, setCalendarEntries] = useState([])
    const [enrichedEvents, setEnrichedEvents] = useState({})
    const [selectedDay, setSelectedDay] = useState(null)
    const [loading, setLoading] = useState(true)
    const detailPanelRef = useRef(null)

    // Add-event modal state
    const [showAddModal, setShowAddModal] = useState(false)
    const [availableEvents, setAvailableEvents] = useState([])
    const [loadingAvailable, setLoadingAvailable] = useState(false)
    const [searchQuery, setSearchQuery] = useState('')

    const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

    // Fetch user's calendar entries
    const fetchCalendar = useCallback(async () => {
        try {
            const res = await getCalendarEvents()
            const items = res.data.results || res.data || []
            setCalendarEntries(items)

            // Enrich each entry with event details
            const enriched = {}
            await Promise.all(
                items.map(async (ce) => {
                    try {
                        const ev = await getEvent(ce.event)
                        enriched[ce.event] = ev.data
                    } catch {
                        enriched[ce.event] = null
                    }
                })
            )
            setEnrichedEvents(enriched)
        } catch {
            setCalendarEntries([])
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        fetchCalendar()
    }, [fetchCalendar])

    // Scroll to details on mobile when day selected
    useEffect(() => {
        if (selectedDay && window.innerWidth <= 768 && detailPanelRef.current) {
            detailPanelRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [selectedDay])

    // Navigation
    const prevMonth = () => {
        if (currentMonth === 0) {
            setCurrentMonth(11)
            setCurrentYear(currentYear - 1)
        } else {
            setCurrentMonth(currentMonth - 1)
        }
        setSelectedDay(null)
    }

    const nextMonth = () => {
        if (currentMonth === 11) {
            setCurrentMonth(0)
            setCurrentYear(currentYear + 1)
        } else {
            setCurrentMonth(currentMonth + 1)
        }
        setSelectedDay(null)
    }

    const goToday = () => {
        setCurrentYear(now.getFullYear())
        setCurrentMonth(now.getMonth())
        setSelectedDay(now.getDate())
    }

    // Build events-by-date lookup
    const eventsByDate = {}
    calendarEntries.forEach((ce) => {
        const ev = enrichedEvents[ce.event]
        if (!ev || !ev.date) return
        if (!eventsByDate[ev.date]) eventsByDate[ev.date] = []
        eventsByDate[ev.date].push({ ...ce, eventData: ev })
    })

    // Events for selected day
    const selectedDateStr = selectedDay
        ? `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(selectedDay).padStart(2, '0')}`
        : null
    const selectedDayEvents = selectedDateStr ? (eventsByDate[selectedDateStr] || []) : []

    // Delete event from calendar
    const handleDelete = async (calendarEventId) => {
        try {
            await removeCalendarEvent(calendarEventId)
            await fetchCalendar()
        } catch { /* ignore */ }
    }

    // Open add-event modal
    const openAddModal = async () => {
        setShowAddModal(true)
        setLoadingAvailable(true)
        setSearchQuery('')
        try {
            let allEvents = []
            let page = 1
            let hasMore = true
            while (hasMore) {
                const res = await getEvents({ page })
                const results = res.data.results || []
                allEvents = [...allEvents, ...results]
                hasMore = allEvents.length < (res.data.count || 0)
                page++
            }
            // Filter out events already in calendar
            const calEventIds = new Set(calendarEntries.map((ce) => ce.event))
            setAvailableEvents(allEvents.filter((ev) => !calEventIds.has(ev.id)))
        } catch {
            setAvailableEvents([])
        } finally {
            setLoadingAvailable(false)
        }
    }

    // Add event to calendar
    const handleAddEvent = async (eventId) => {
        try {
            await addCalendarEvent({ event: eventId, status: 0 })
            setShowAddModal(false)
            await fetchCalendar()
        } catch { /* ignore */ }
    }

    const getName = (item) => item?.translations?.[0]?.name || `Event #${item?.id}`

    const filteredAvailable = availableEvents.filter((ev) => {
        if (!searchQuery) return true
        const name = getName(ev).toLowerCase()
        return name.includes(searchQuery.toLowerCase())
    })

    const daysInMonth = getDaysInMonth(currentYear, currentMonth)
    const firstDay = getFirstDayOfWeek(currentYear, currentMonth)

    if (loading) {
        return <div className="loading-container"><div className="spinner"></div></div>
    }

    return (
        <div className="calendar-page container fade-in">
            <div className="calendar-header">
                <h1>{t.calendar.title}</h1>
                <div className="calendar-actions">
                    <button className="btn btn-sm btn-secondary" onClick={goToday}>{t.calendar.today}</button>
                    <button className="btn btn-sm btn-primary" onClick={openAddModal}>+ {t.calendar.addEvent || 'Add Event'}</button>
                </div>
            </div>

            <div className="month-nav">
                <button className="btn btn-sm btn-secondary" onClick={prevMonth}>←</button>
                <h2 className="month-title">{t.calendar.monthNames[currentMonth]} {currentYear}</h2>
                <button className="btn btn-sm btn-secondary" onClick={nextMonth}>→</button>
            </div>

            <div className="calendar-layout">
                <div className="calendar-grid-single">
                    <div className="weekday-row">
                        {t.calendar.weekDays.map((d) => (
                            <span key={d} className="weekday-label">{d}</span>
                        ))}
                    </div>

                    <div className="days-grid">
                        {Array.from({ length: firstDay }, (_, i) => (
                            <div key={`empty-${i}`} className="day-cell empty" />
                        ))}

                        {Array.from({ length: daysInMonth }, (_, dayIdx) => {
                            const day = dayIdx + 1
                            const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
                            const dayEvents = eventsByDate[dateStr] || []
                            const isToday = dateStr === todayStr
                            const isSelected = selectedDay === day

                            return (
                                <div
                                    key={day}
                                    className={`day-cell ${isToday ? 'today' : ''} ${dayEvents.length > 0 ? 'has-events' : ''} ${isSelected ? 'selected' : ''}`}
                                    onClick={() => setSelectedDay(day)}
                                >
                                    <span className="day-number">{day}</span>
                                    {dayEvents.length > 0 && (
                                        <span className="event-dots">
                                            {dayEvents.slice(0, 3).map((_, i) => (
                                                <span key={i} className="dot" />
                                            ))}
                                        </span>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>

                <div className="day-detail-panel" ref={detailPanelRef}>
                    {selectedDay ? (
                        <>
                            <h3>
                                {selectedDay} {t.calendar.monthNames[currentMonth]}
                            </h3>
                            {selectedDayEvents.length === 0 ? (
                                <p className="no-results">{t.calendar.noEvents || 'No events this day'}</p>
                            ) : (
                                <div className="day-event-list">
                                    {selectedDayEvents.map((ce) => {
                                        const ev = ce.eventData
                                        return (
                                            <div key={ce.id} className="day-event-card card">
                                                <div className="day-event-info">
                                                    <Link to={`/events/${ce.event}`}>
                                                        <h4>{getName(ev)}</h4>
                                                    </Link>
                                                    {ev?.start_time && (
                                                        <span className="event-time">🕐 {ev.start_time.slice(0, 5)}</span>
                                                    )}
                                                </div>
                                                <button
                                                    className="btn btn-sm btn-danger"
                                                    onClick={() => handleDelete(ce.id)}
                                                >
                                                    ✕
                                                </button>
                                            </div>
                                        )
                                    })}
                                </div>
                            )}
                        </>
                    ) : (
                        <p className="no-results">{t.calendar.selectDay || 'Select a day to view events'}</p>
                    )}
                </div>
            </div>

            {/* Add Event Modal */}
            {showAddModal && (
                <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
                    <div className="modal-card" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>{t.calendar.addEvent || 'Add Event'}</h2>
                            <button className="modal-close" onClick={() => setShowAddModal(false)}>✕</button>
                        </div>
                        <input
                            type="text"
                            className="modal-search"
                            placeholder={t.calendar.searchEvents || 'Search events...'}
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                        <div className="modal-body">
                            {loadingAvailable ? (
                                <div className="loading-container"><div className="spinner"></div></div>
                            ) : filteredAvailable.length === 0 ? (
                                <p className="no-results">{t.calendar.noAvailable || 'No events available'}</p>
                            ) : (
                                filteredAvailable.map((ev) => (
                                    <div key={ev.id} className="add-event-row" onClick={() => handleAddEvent(ev.id)}>
                                        <div>
                                            <strong>{getName(ev)}</strong>
                                            <span className="add-event-date">📅 {ev.date}</span>
                                        </div>
                                        <span className="add-btn-icon">+</span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
