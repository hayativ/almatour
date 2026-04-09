import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getSouvenirs } from '../api/client'
import { useLang } from '../i18n/translations'
import './Souvenirs.css'

export default function Souvenirs() {
    const { t } = useLang()
    const [souvenirs, setSouvenirs] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        getSouvenirs()
            .then((res) => setSouvenirs(res.data.results || res.data || []))
            .catch(() => setSouvenirs([]))
            .finally(() => setLoading(false))
    }, [])

    return (
        <div className="souvenirs-page container">
            <Link to="/" className="back-link">{t.common.back}</Link>
            <h1>{t.info.souvenirsTitle}</h1>

            {loading ? (
                <div className="loading-container"><div className="spinner"></div></div>
            ) : souvenirs.length === 0 ? (
                <p className="no-results">{t.info.noSouvenirs}</p>
            ) : (
                <div className="souvenirs-grid">
                    {souvenirs.map((item) => (
                        <div key={item.id} className="souvenir-card card fade-in">
                            {item.image && <img src={item.image} alt={item.name} className="souvenir-img" />}
                            <div className="souvenir-body">
                                <h3>{item.name}</h3>
                                {item.address && <p className="souvenir-addr">📍 {item.address}</p>}
                                {item.link && (
                                    <a href={item.link} target="_blank" rel="noopener noreferrer" className="souvenir-link btn btn-sm btn-primary">
                                        {t.info.visitSite}
                                    </a>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
