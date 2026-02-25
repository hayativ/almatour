import { useLang } from '../i18n/translations'
import './Places.css'

export default function Places() {
    const { t } = useLang()

    return (
        <div className="places-page container">
            <h1>{t.places.mapTitle}</h1>

            <div className="map-container">
                <img
                    src="https://static-maps.yandex.ru/v1?lang=en_US&ll=76.9286,43.2380&z=12&size=650,450&l=map&apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
                    alt="Map of Almaty"
                    className="map-image"
                    onError={(e) => {
                        e.target.onerror = null
                        e.target.src = `https://tile.openstreetmap.org/12/2872/1510.png`
                        e.target.className = 'map-image map-fallback'
                    }}
                />
            </div>

            <div className="map-info">
                <p className="map-label">📍 Almaty, Kazakhstan</p>
                <p className="map-coords">43.2380° N, 76.9286° E</p>
            </div>
        </div>
    )
}
