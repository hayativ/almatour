/**
 * Build a safe image URL from whatever the API returns.
 * - Full URLs (http/https) are used as-is.
 * - Relative paths (e.g. "images/info/apps/onay.jpg") are prefixed with /media/.
 * - Null/empty values return the fallback placeholder.
 */

const FALLBACK =
    'data:image/svg+xml,' +
    encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" fill="%23334155">' +
        '<rect width="400" height="300" rx="12"/>' +
        '<text x="50%" y="50%" fill="%2394a3b8" font-size="18" text-anchor="middle" dy=".35em">No image</text>' +
        '</svg>'
    )

export function getImageUrl(raw) {
    if (!raw) return FALLBACK
    if (raw.startsWith('http://') || raw.startsWith('https://')) return raw
    // Ensure a single leading slash and /media/ prefix
    const clean = raw.replace(/^\/+/, '')
    return clean.startsWith('media/') ? `/${clean}` : `/media/${clean}`
}

export function handleImageError(e) {
    e.target.onerror = null
    e.target.src = FALLBACK
}
