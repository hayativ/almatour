import { useState, useEffect } from 'react'
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
    const [menuOpen, setMenuOpen] = useState(false)

    const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

    // Close menu on route change
    useEffect(() => {
        setMenuOpen(false)
    }, [location.pathname])

    // Prevent body scroll when menu open
    useEffect(() => {
        if (menuOpen) {
            document.body.style.overflow = 'hidden'
        } else {
            document.body.style.overflow = ''
        }
        return () => { document.body.style.overflow = '' }
    }, [menuOpen])

    return (
        <nav className="navbar">
            <div className="nav-container">
                <Link to="/" className="nav-brand">
                    <img src="/Logo.png" alt="Almatour" className="brand-icon-img" />

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
                        <Link to="/profile" className="nav-profile-btn nav-profile-desktop">{t.nav.profile}</Link>
                    ) : (
                        <Link to="/login" className="nav-login-btn nav-login-desktop">{t.nav.login}</Link>
                    )}

                    {/* Hamburger button — visible only on mobile */}
                    <button
                        className="hamburger"
                        onClick={() => setMenuOpen(!menuOpen)}
                        aria-label="Toggle menu"
                        aria-expanded={menuOpen}
                    >
                        <span className={`hamburger-line ${menuOpen ? 'open' : ''}`} />
                        <span className={`hamburger-line ${menuOpen ? 'open' : ''}`} />
                        <span className={`hamburger-line ${menuOpen ? 'open' : ''}`} />
                    </button>
                </div>
            </div>

            {/* Mobile menu overlay */}
            <div className={`mobile-menu ${menuOpen ? 'mobile-menu--open' : ''}`}>
                <div className="mobile-menu-backdrop" onClick={() => setMenuOpen(false)} />
                <div className="mobile-menu-panel">
                    {user && (
                        <div className="mobile-nav-links">
                            <Link to="/info" className={isActive('/info')}>{t.nav.info}</Link>
                            <Link to="/places" className={isActive('/places')}>{t.nav.places}</Link>
                            <Link to="/events" className={isActive('/events')}>{t.nav.events}</Link>
                            <Link to="/calendar" className={isActive('/calendar')}>{t.nav.calendar}</Link>
                        </div>
                    )}
                    <div className="mobile-menu-bottom">
                        {user ? (
                            <Link to="/profile" className="btn btn-primary mobile-profile-btn">{t.nav.profile}</Link>
                        ) : (
                            <Link to="/login" className="btn btn-primary mobile-login-btn">{t.nav.login}</Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    )
}
