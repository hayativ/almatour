import { useLang } from '../i18n/translations'
import './Footer.css'

export default function Footer() {
    const { t } = useLang()
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-brand">
                    <span className="footer-icon">🍏</span>
                    <span className="footer-name">Almatour</span>
                </div>
                <p className="footer-tagline">{t.footer.tagline}</p>
                <p className="footer-copy">{t.footer.copy}</p>
            </div>
        </footer>
    )
}
