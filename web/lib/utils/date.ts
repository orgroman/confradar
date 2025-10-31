/**
 * Format a date to a human-readable string
 */
export function formatDate(date: Date | undefined): string {
  if (!date) return "TBA"
  
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date)
}

/**
 * Calculate days remaining until a date
 */
export function daysUntil(date: Date | undefined): number | null {
  if (!date) return null
  
  const now = new Date()
  const diff = date.getTime() - now.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

/**
 * Check if a date is in the past
 */
export function isPast(date: Date | undefined): boolean {
  if (!date) return false
  return date < new Date()
}
