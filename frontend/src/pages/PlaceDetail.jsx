import { useState, useEffect, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getPlace } from '../api/client'
import { useLang } from '../i18n/translations'
import { getImageUrl, handleImageError } from '../utils/imageUrl'
import './PlaceDetail.css'

/* Map lang code to DB language_id: en=1, ru=2, kz=3 */
const LANG_ID_MAP = { en: 1, ru: 2, kz: 3 }

export default function PlaceDetail() {
    const { t, lang } = useLang()
    const { id } = useParams()
    const [place, setPlace] = useState(null)
    const [loading, setLoading] = useState(true)
    const [copied, setCopied] = useState(false)

    useEffect(() => {
        getPlace(id)
            .then((res) => setPlace(res.data))
            .catch(() => setPlace(null))
            .finally(() => setLoading(false))
    }, [id])

    const copyAddress = useCallback(() => {
        if (!place?.address) return
        navigator.clipboard.writeText(place.address).then(() => {
            setCopied(true)
            setTimeout(() => setCopied(false), 2000)
        })
    }, [place])

    if (loading)
        return (
            <div className="loading-container">
                <div className="spinner"></div>
            </div>
        )
    if (!place)
        return (
            <div className="detail-empty container">
                <p>{t.common.error}</p>
                <Link to="/places">{t.common.back}</Link>
            </div>
        )

    const langId = LANG_ID_MAP[lang] ?? 1
    const tr =
        place.translations?.find(t => t.language_id === langId) ||
        place.translations?.[0]

    const imageUrl = getImageUrl(place.image)

    return (
        <div className="place-detail container fade-in">
            <Link to="/places" className="back-link">{t.common.back}</Link>

            <div className="detail-hero">
                <img src={imageUrl} alt={tr?.name} className="detail-hero-img" onError={handleImageError} />
            </div>

            <div className="detail-body">
                <h1>{tr?.name || `Place #${place.id}`}</h1>

                {/* Timetable */}
                {tr?.timetable && (
                    <div className="detail-card">
                        <div className="detail-card-content">
                            <span className="detail-card-label">{t.places.schedule || 'Schedule'}</span>
                            <span className="detail-card-value">{tr.timetable}</span>
                        </div>
                    </div>
                )}

                {/* Address with copy */}
                <div className="detail-card">
                    <div className="detail-card-content">
                        <span className="detail-card-label">{t.places.addressLabel || 'Address'}</span>
                        <span className="detail-card-value">{place.address}</span>
                    </div>
                    <button
                        className={`copy-btn ${copied ? 'copied' : ''}`}
                        onClick={copyAddress}
                        title={t.places.copyAddress || 'Copy address'}
                    >
                        {copied ? '✓' : '🔗'}
                    </button>
                </div>

                {/* Website link */}
                {place.link && (
                    <div className="detail-card">
                        <div className="detail-card-content">
                            <span className="detail-card-label">{t.places.website || 'Website'}</span>
                            <a
                                href={place.link}
                                target="_blank"
                                rel="noreferrer"
                                className="detail-card-link"
                            >
                                {place.link.replace(/^https?:\/\//, '').replace(/\/$/, '')}
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
