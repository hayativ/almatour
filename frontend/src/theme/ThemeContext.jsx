import { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext(null)

export function ThemeProvider({ children }) {
    const [isDark, setIsDark] = useState(() => {
        const stored = localStorage.getItem('almatour_theme')
        // Default to light mode (false)
        return stored === null ? false : stored === 'dark'
    })

    useEffect(() => {
        const root = window.document.body
        if (isDark) {
            root.classList.remove('light-mode')
            localStorage.setItem('almatour_theme', 'dark')
        } else {
            root.classList.add('light-mode')
            localStorage.setItem('almatour_theme', 'light')
        }
    }, [isDark])

    const toggleTheme = () => setIsDark(!isDark)

    return (
        <ThemeContext.Provider value={{ isDark, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    )
}

export const useTheme = () => useContext(ThemeContext)
