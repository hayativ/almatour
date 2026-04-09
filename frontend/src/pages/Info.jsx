import { Link } from 'react-router-dom'
import { useLang } from '../i18n/translations'
import './Info.css'

export default function Info() {
    const { t } = useLang()

    return (
        <div className="info-page container">
            <h1>{t.info.title}</h1>

            <div className="info-categories">
                <Link to="/souvenirs" className="info-category-card card fade-in">
                    <div className="category-content">
                        <h2>{t.info.souvenirsCategory}</h2>
                        <p>{t.info.souvenirsDesc}</p>
                    </div>
                    <span className="category-arrow">→</span>
                </Link>

                <Link to="/apps" className="info-category-card card fade-in">
                    <div className="category-content">
                        <h2>{t.info.appsCategory}</h2>
                        <p>{t.info.appsDesc}</p>
                    </div>
                    <span className="category-arrow">→</span>
                </Link>
            </div>
        </div>
    )
}
