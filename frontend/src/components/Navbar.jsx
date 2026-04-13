import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import { useTheme } from '../theme/ThemeContext'
import './Navbar.css'

export default function Navbar() {
    const { user } = useAuth()
    const { lang, t, setLanguage } = useLang()
    const { isDark, toggleTheme } = useTheme()
    const location = useLocation()

    const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

    return (
        <nav className="navbar">
            <div className="nav-container">
                <Link to="/" className="nav-brand">
                    <img src="/Logo.png" alt="Almatour" className="brand-icon-img" />
                    <span className="brand-text">{t.nav.title}</span>
                </Link>

                {user && (
                    <div className="nav-links">
                        <Link to="/info" className={isActive('/info')}>{t.nav.info}</Link>
                        <Link to="/places" className={isActive('/places')}>{t.nav.places}</Link>
                        <Link to="/events" className={isActive('/events')}>{t.nav.events}</Link>
                        <Link to="/calendar" className={isActive('/calendar')}>{t.nav.calendar}</Link>
                    </div>
                )}

                <div className="nav-right">
                    <button className="theme-toggle" onClick={toggleTheme} title="Toggle theme">
                        {isDark ? '☀️' : '🌙'}
                    </button>
                    <div className="lang-switcher">
                        {['en', 'ru', 'kz'].map((l) => (
                            <button
                                key={l}
                                className={`lang-btn ${lang === l ? 'active' : ''}`}
                                onClick={() => setLanguage(l)}
                            >
                                {l.toUpperCase()}
                            </button>
                        ))}
                    </div>
                    {user ? (
                        <Link to="/profile" className="nav-profile-btn">{t.nav.profile}</Link>
                    ) : (
                        <Link to="/login" className="nav-login-btn">{t.nav.login}</Link>
                    )}
                </div>
            </div>
        </nav>
    )
}
