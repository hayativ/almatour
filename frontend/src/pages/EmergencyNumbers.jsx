import { Link } from 'react-router-dom'
import { useLang } from '../i18n/translations'
import './EmergencyNumbers.css'

export default function EmergencyNumbers() {
    const { t } = useLang()
    const em = t.info.emergency

    return (
        <div className="emergency-page container">
            <Link to="/info" className="back-link">{t.common.back}</Link>
            <h1>{em.title}</h1>

            {/* Section 1: Main emergency numbers */}
            <section className="emergency-section fade-in">
                <h2>{em.mainTitle}</h2>
                <ul className="emergency-numbers-list">
                    {em.mainNumbers.map((item, i) => (
                        <li key={i}>
                            <a href={`tel:${item.number}`} className="emergency-number">{item.number}</a>
                            <span className="emergency-dash"> — </span>
                            <span className="emergency-label">{item.label}</span>
                        </li>
                    ))}
                </ul>
            </section>

            {/* Section 2: Additional information */}
            <section className="emergency-section fade-in">
                <h2>{em.additionalTitle}</h2>
                <ul className="emergency-list">
                    {em.additionalItems.map((text, i) => (
                        <li key={i}>{text}</li>
                    ))}
                </ul>
                <p className="emergency-free-note">{em.freeCallNote}</p>
            </section>

            {/* Section 3: Important notice */}
            <section className="emergency-section emergency-warning fade-in">
                <h2>⚠️ {em.importantTitle}</h2>
                <p>{em.importantText}</p>
            </section>
        </div>
    )
}
