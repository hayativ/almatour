import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import './Login.css'

export default function Register() {
    const { t } = useLang()
    const { registerUser } = useAuth()
    const navigate = useNavigate()
    const [email, setEmail] = useState('')
    const [username, setUsername] = useState('')
    const [phone, setPhone] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            await registerUser(email, username, phone, password)
            navigate('/profile')
        } catch (err) {
            const data = err.response?.data
            const msg = data ? Object.values(data).flat().join('. ') : t.common.error
            setError(msg)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>{t.auth.registerTitle}</h1>
                    <p>{t.auth.registerSub}</p>
                </div>
                <form onSubmit={handleSubmit} className="auth-form">
                    {error && <div className="auth-error">{error}</div>}
                    <div className="form-group">
                        <label>{t.auth.email}</label>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>{t.auth.username}</label>
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>{t.auth.phone}</label>
                        <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>{t.auth.password}</label>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
                    </div>
                    <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
                        {loading ? t.auth.creatingAccount : t.auth.signUp}
                    </button>
                </form>
                <p className="auth-switch">
                    {t.auth.haveAccount} <Link to="/login">{t.auth.signIn}</Link>
                </p>
            </div>
        </div>
    )
}
