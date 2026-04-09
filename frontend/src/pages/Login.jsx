import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLang } from '../i18n/translations'
import './Login.css'

export default function Login() {
    const { t } = useLang()
    const { loginUser } = useAuth()
    const navigate = useNavigate()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            await loginUser(email, password)
            navigate('/profile')
        } catch (err) {
            setError(err.response?.data?.detail || t.common.error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>{t.auth.loginTitle}</h1>
                    <p>{t.auth.loginSub}</p>
                </div>
                <form onSubmit={handleSubmit} className="auth-form">
                    {error && <div className="auth-error">{error}</div>}
                    <div className="form-group">
                        <label>{t.auth.email}</label>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>{t.auth.password}</label>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
                        {loading ? t.auth.signingIn : t.auth.signIn}
                    </button>
                </form>
                <p className="auth-switch">
                    {t.auth.noAccount} <Link to="/register">{t.auth.signUp}</Link>
                </p>
            </div>
        </div>
    )
}
