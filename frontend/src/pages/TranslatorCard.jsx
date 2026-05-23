import { useState } from 'react'
import { useLang } from '../i18n/translations'
import { translateText } from '../api/client'
import './TranslatorCard.css'

const LANG_CODES = ['en', 'ru', 'kk', 'zh', 'tr', 'hi', 'fr', 'de', 'es', 'ar', 'ja', 'ko']
const MAX_CHARS = 2000

export default function TranslatorCard() {
    const { t } = useLang()
    const tr = t.info.translator

    const [text, setText] = useState('')
    const [source, setSource] = useState('auto')
    const [target, setTarget] = useState('ru')
    const [result, setResult] = useState('')
    const [detectedLang, setDetectedLang] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const canTranslate = text.trim().length > 0 && !loading

    const handleTranslate = async () => {
        if (!canTranslate) return
        setLoading(true)
        setError('')
        setResult('')
        setDetectedLang('')
        try {
            const { data } = await translateText({
                text: text.trim(),
                source,
                target,
            })
            setResult(data.translatedText)
            setDetectedLang(data.detectedSourceLanguage || '')
        } catch (err) {
            const msg = err.response?.data?.error || tr.errorGeneric
            setError(msg)
        } finally {
            setLoading(false)
        }
    }

    const handleClear = () => {
        setText('')
        setResult('')
        setDetectedLang('')
        setError('')
    }

    const handleSwap = () => {
        if (source === 'auto') return
        const prevSource = source
        setSource(target)
        setTarget(prevSource)
        if (result) {
            setText(result)
            setResult('')
            setDetectedLang('')
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey && canTranslate) {
            e.preventDefault()
            handleTranslate()
        }
    }

    const langName = (code) => tr.langs[code] || code

    return (
        <div className="translator-card card fade-in">
            <div className="translator-header">
                <h2>{tr.title}</h2>
                <p className="translator-desc">{tr.desc}</p>
            </div>

            <div className="translator-body">
                <textarea
                    className="translator-input"
                    value={text}
                    onChange={(e) => setText(e.target.value.slice(0, MAX_CHARS))}
                    onKeyDown={handleKeyDown}
                    placeholder={tr.placeholder}
                    rows={3}
                    maxLength={MAX_CHARS}
                />
                <div className="translator-char-count">
                    {text.length}/{MAX_CHARS} {tr.charLimit}
                </div>

                <div className="translator-controls">
                    <div className="translator-selects">
                        <select
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                            className="translator-select"
                        >
                            <option value="auto">{tr.autoDetect}</option>
                            {LANG_CODES.map((code) => (
                                <option key={code} value={code}>
                                    {langName(code)}
                                </option>
                            ))}
                        </select>

                        <button
                            className="translator-swap btn-secondary btn-sm"
                            onClick={handleSwap}
                            disabled={source === 'auto'}
                            title={tr.swapBtn}
                            type="button"
                        >
                            &#8646;
                        </button>

                        <select
                            value={target}
                            onChange={(e) => setTarget(e.target.value)}
                            className="translator-select"
                        >
                            {LANG_CODES.map((code) => (
                                <option key={code} value={code}>
                                    {langName(code)}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="translator-actions">
                        <button
                            className="btn btn-primary btn-sm"
                            onClick={handleTranslate}
                            disabled={!canTranslate}
                            type="button"
                        >
                            {loading ? tr.loading : tr.translateBtn}
                        </button>
                        {(text || result) && (
                            <button
                                className="btn btn-secondary btn-sm"
                                onClick={handleClear}
                                type="button"
                            >
                                {tr.clearBtn}
                            </button>
                        )}
                    </div>
                </div>

                {error && <div className="translator-error">{error}</div>}

                {result && (
                    <div className="translator-result">
                        {detectedLang && source === 'auto' && (
                            <span className="translator-detected">
                                {langName(detectedLang)}
                            </span>
                        )}
                        <p>{result}</p>
                    </div>
                )}
            </div>
        </div>
    )
}
