import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import './Profile.css'

export default function Profile() {
    const { t } = useLang()
    const { user, loading: authLoading, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    if (authLoading) return <div className="loading-container"><div className="spinner"></div></div>
    if (!user) return null

    return (
        <div className="profile-page container fade-in">
            <div className="profile-header">
                <div className="profile-avatar">{user.username?.[0]?.toUpperCase() || '?'}</div>
                <div>
                    <h1>{t.profile.title}</h1>
                    <p className="profile-email">{user.email}</p>
                </div>
            </div>

            <div className="profile-info-grid">
                <div className="info-card">
                    <span className="info-label">{t.profile.username}</span>
                    <span className="info-value">{user.username}</span>
                </div>
                <div className="info-card">
                    <span className="info-label">{t.profile.email}</span>
                    <span className="info-value">{user.email}</span>
                </div>
                <div className="info-card">
                    <span className="info-label">{t.profile.phone}</span>
                    <span className="info-value">{user.phone}</span>
                </div>
            </div>

            <button className="btn btn-danger" onClick={handleLogout}>{t.profile.signOut}</button>
        </div>
    )
}
