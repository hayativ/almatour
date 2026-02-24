import { createContext, useContext, useState, useEffect } from 'react'
import { login as apiLogin, register as apiRegister, getProfile } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = localStorage.getItem('access_token')
        if (token) {
            getProfile()
                .then((res) => setUser(res.data))
                .catch(() => {
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                })
                .finally(() => setLoading(false))
        } else {
            setLoading(false)
        }
    }, [])

    const loginUser = async (email, password) => {
        const { data } = await apiLogin({ email, password })
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        const profile = await getProfile()
        setUser(profile.data)
        return profile.data
    }

    const registerUser = async (email, username, phone, password) => {
        await apiRegister({ email, username, phone, password })
        return loginUser(email, password)
    }

    const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, loginUser, registerUser, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
