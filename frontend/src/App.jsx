import { Routes, Route, Navigate } from 'react-router-dom'
import { LangProvider } from './i18n/translations'
import { useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import PrivateRoute from './components/PrivateRoute'
import Info from './pages/Info'
import Souvenirs from './pages/Souvenirs'
import Apps from './pages/Apps'
import EmergencyNumbers from './pages/EmergencyNumbers'
import Places from './pages/Places'
import PlaceDetail from './pages/PlaceDetail'
import Events from './pages/Events'
import Calendar from './pages/Calendar'
import EventDetail from './pages/EventDetail'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'

function RootRedirect() {
    const { user, loading } = useAuth()
    if (loading) return <div className="loading-container"><div className="spinner"></div></div>
    return user ? <Navigate to="/events" replace /> : <Navigate to="/login" replace />
}

export default function App() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navbar />
            <main style={{ flex: 1 }}>
                <Routes>
                    <Route path="/" element={<RootRedirect />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/info" element={<PrivateRoute><Info /></PrivateRoute>} />
                    <Route path="/souvenirs" element={<PrivateRoute><Souvenirs /></PrivateRoute>} />
                    <Route path="/apps" element={<PrivateRoute><Apps /></PrivateRoute>} />
                    <Route path="/emergency" element={<PrivateRoute><EmergencyNumbers /></PrivateRoute>} />
                    <Route path="/places" element={<PrivateRoute><Places /></PrivateRoute>} />
                    <Route path="/places/:id" element={<PrivateRoute><PlaceDetail /></PrivateRoute>} />
                    <Route path="/events" element={<PrivateRoute><Events /></PrivateRoute>} />
                    <Route path="/calendar" element={<PrivateRoute><Calendar /></PrivateRoute>} />
                    <Route path="/events/:id" element={<PrivateRoute><EventDetail /></PrivateRoute>} />
                    <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
                </Routes>
            </main>
            <Footer />
        </div>
    )
}
