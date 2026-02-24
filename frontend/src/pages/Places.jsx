import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPlaces } from '../api/client'
import { useLang } from '../i18n/translations'
import './Places.css'

const CATEGORIES = [null, 0, 1, 2, 3]

export default function Places() {
    const { t } = useLang()
    const [places, setPlaces] = useState([])
    const [loading, setLoading] = useState(true)
    const [category, setCategory] = useState(null)
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)

    useEffect(() => {
        setLoading(true)
        const params = { page }
        if (category !== null) params.category = category
        getPlaces(params)
            .then((res) => {
                setPlaces(res.data.results || [])
                const count = res.data.count || 0
                setTotalPages(Math.max(1, Math.ceil(count / 25)))
            })
            .catch(() => setPlaces([]))
            .finally(() => setLoading(false))
    }, [category, page])

    const catLabels = [
        t.places.allCategories,
        t.places.category0,
        t.places.category1,
        t.places.category2,
        t.places.category3,
    ]

    const getName = (item) => item.translations?.[0]?.name || `Place #${item.id}`

    return (
        <div className="places-page container">
            <h1>{t.places.title}</h1>

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
            ) : places.length === 0 ? (
                <p className="no-results">{t.places.noResults}</p>
            ) : (
                <>
                    <div className="places-list-grid">
                        {places.map((place) => (
                            <Link to={`/places/${place.id}`} key={place.id} className="place-list-card card fade-in">
                                {place.image && <img src={place.image} alt={getName(place)} className="plc-img" />}
                                <div className="plc-body">
                                    <h3>{getName(place)}</h3>
                                    <p className="plc-addr">📍 {place.address}</p>
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
