/**
 * Format a date string from YYYY-MM-DD to DD.MM.YYYY (CIS region format).
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @returns {string} Date in DD.MM.YYYY format
 */
export function formatDateCIS(dateStr) {
    if (!dateStr) return ''
    const parts = dateStr.split('-')
    if (parts.length !== 3) return dateStr
    return `${parts[2]}.${parts[1]}.${parts[0]}`
}
