import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getEvents } from '../api/client'
import { useLang } from '../i18n/translations'
import './Events.css'

const CATEGORIES = [null, 0, 1, 2, 3]

export default function Events() {
    const { t } = useLang()
    const [events, setEvents] = useState([])
    const [loading, setLoading] = useState(true)
    const [category, setCategory] = useState(null)
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)

    useEffect(() => {
        setLoading(true)
        const params = { page }
        if (category !== null) params.category = category
        getEvents(params)
            .then((res) => {
                setEvents(res.data.results || [])
                const count = res.data.count || 0
                setTotalPages(Math.max(1, Math.ceil(count / 25)))
            })
            .catch(() => setEvents([]))
            .finally(() => setLoading(false))
    }, [category, page])

    const catLabels = [
        t.events.allCategories,
        t.events.category0,
        t.events.category1,
        t.events.category2,
        t.events.category3,
    ]

    const getName = (item) => item.translations?.[0]?.name || `Event #${item.id}`

    return (
        <div className="events-page container">
            <h1>{t.events.title}</h1>

            <div className="category-filters">
                {CATEGORIES.map((cat, i) => (
                    <button
                        key={i}
                        className={`filter-btn ${category === cat ? 'active' : ''}`}
                        onClick={() => { setCategory(cat); setPage(1) }}
                    >
                        {catLabels[i]}
                    </button>
                ))}
            </div>

            {loading ? (
                <div className="loading-container"><div className="spinner"></div></div>
            ) : events.length === 0 ? (
                <p className="no-results">{t.events.noResults}</p>
            ) : (
                <>
                    <div className="events-list-grid">
                        {events.map((ev) => (
                            <Link to={`/events/${ev.id}`} key={ev.id} className="ev-list-card card fade-in">
                                {ev.image && <img src={ev.image} alt={getName(ev)} className="ev-img" />}
                                <div className="ev-body">
                                    <h3>{getName(ev)}</h3>
                                    <div className="ev-meta">
                                        <span>📅 {ev.date}</span>
                                        <span>🕐 {ev.start_time?.slice(0, 5)}</span>
                                    </div>
                                    <div className="ev-cost">
                                        {ev.cost > 0 ? `${ev.cost} ${ev.currency}` : t.events.free}
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>

                    {totalPages > 1 && (
                        <div className="pagination">
                            <button className="btn btn-sm btn-secondary" disabled={page <= 1} onClick={() => setPage(page - 1)}>←</button>
                            <span className="page-info">{page} / {totalPages}</span>
                            <button className="btn btn-sm btn-secondary" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>→</button>
                        </div>
                    )}
                </>
            )}
        </div>
    )
}
