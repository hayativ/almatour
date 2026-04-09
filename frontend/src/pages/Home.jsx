import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPlaces, getEvents, getAdvertisements } from '../api/client'
import { useLang } from '../i18n/translations'
import './Home.css'

export default function Home() {
    const { t } = useLang()
    const [places, setPlaces] = useState([])
    const [events, setEvents] = useState([])
    const [ads, setAds] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        Promise.all([
            getPlaces({ page_size: 6 }).catch(() => ({ data: { results: [] } })),
            getEvents({ page_size: 4 }).catch(() => ({ data: { results: [] } })),
            getAdvertisements().catch(() => ({ data: { results: [] } })),
        ]).then(([p, e, a]) => {
            setPlaces(p.data.results || [])
            setEvents(e.data.results || [])
            setAds(a.data.results || [])
            setLoading(false)
        })
    }, [])

    const getName = (item) => {
        const tr = item.translations?.[0]
        return tr?.name || `#${item.id}`
    }

    const getDesc = (item) => {
        const tr = item.translations?.[0]
        return tr?.description || ''
    }

    return (
        <div className="home">
            {/* Hero */}
            <section className="hero">
                <div className="hero-bg"></div>
                <div className="hero-content container">
                    <h1 className="hero-title">{t.home.hero}</h1>
                    <p className="hero-sub">{t.home.heroSub}</p>
                    <div className="hero-actions">
                        <Link to="/places" className="btn btn-primary">{t.home.explorePlaces}</Link>
                        <Link to="/events" className="btn btn-secondary">{t.home.upcomingEvents}</Link>
                    </div>
                </div>
            </section>

            {/* Ads Carousel */}
            {ads.length > 0 && (
                <section className="section container">
                    <h2 className="section-title">{t.home.ads}</h2>
                    <div className="ads-row">
                        {ads.map((ad) => (
                            <div key={ad.id} className="ad-card card">
                                {ad.image && <img src={ad.image} alt={getName(ad)} className="ad-img" />}
                                <div className="ad-info">
                                    <h4>{getName(ad)}</h4>
                                    <p>{getDesc(ad)}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            {/* Featured Places */}
            <section className="section container">
                <div className="section-header">
                    <h2 className="section-title">{t.home.featuredPlaces}</h2>
                    <Link to="/places" className="view-all">{t.home.viewAll} →</Link>
                </div>
                {loading ? (
                    <div className="loading-container"><div className="spinner"></div></div>
                ) : places.length === 0 ? (
                    <p className="empty-msg">{t.places.noResults}</p>
                ) : (
                    <div className="places-grid">
                        {places.map((place) => (
                            <Link to={`/places/${place.id}`} key={place.id} className="place-card card fade-in">
                                {place.image && <img src={place.image} alt={getName(place)} className="place-img" />}
                                <div className="place-info">
                                    <h3>{getName(place)}</h3>
                                    <p className="place-address">📍 {place.address}</p>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </section>

            {/* Upcoming Events */}
            <section className="section container">
                <div className="section-header">
                    <h2 className="section-title">{t.home.upcomingEvents}</h2>
                    <Link to="/events" className="view-all">{t.home.viewAll} →</Link>
                </div>
                {loading ? (
                    <div className="loading-container"><div className="spinner"></div></div>
                ) : events.length === 0 ? (
                    <p className="empty-msg">{t.events.noResults}</p>
                ) : (
                    <div className="events-grid">
                        {events.map((ev) => (
                            <Link to={`/events/${ev.id}`} key={ev.id} className="event-card card fade-in">
                                {ev.image && <img src={ev.image} alt={getName(ev)} className="event-img" />}
                                <div className="event-info">
                                    <h3>{getName(ev)}</h3>
                                    <div className="event-meta">
                                        <span>📅 {ev.date}</span>
                                        <span>🕐 {ev.start_time?.slice(0, 5)}</span>
                                        <span>{ev.cost > 0 ? `💰 ${ev.cost} ${ev.currency}` : `✨ ${t.events.free}`}</span>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </section>
        </div>
    )
}
