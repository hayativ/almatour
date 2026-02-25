import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getApps } from '../api/client'
import { useLang } from '../i18n/translations'
import './Apps.css'

export default function Apps() {
    const { t } = useLang()
    const [apps, setApps] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        getApps()
            .then((res) => setApps(res.data.results || res.data || []))
            .catch(() => setApps([]))
            .finally(() => setLoading(false))
    }, [])

    return (
        <div className="apps-page container">
            <Link to="/" className="back-link">{t.common.back}</Link>
            <h1>{t.info.appsTitle}</h1>

            {loading ? (
                <div className="loading-container"><div className="spinner"></div></div>
            ) : apps.length === 0 ? (
                <p className="no-results">{t.info.noApps}</p>
            ) : (
                <div className="apps-grid">
                    {apps.map((item) => (
                        <div key={item.id} className="app-card card fade-in">
                            {item.image && <img src={item.image} alt={item.name} className="app-img" />}
                            <div className="app-body">
                                <h3>{item.name}</h3>
                                {item.description && <p className="app-desc">{item.description}</p>}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
