const MILLISECONDS_PER_DAY = 1000 * 60 * 60 * 24

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
 * Calculate days until a date (can be negative for past dates)
 */
export function daysUntil(date: Date | undefined): number | null {
  if (!date) return null
  
  const now = new Date()
  const diff = date.getTime() - now.getTime()
  return Math.ceil(diff / MILLISECONDS_PER_DAY)
}

/**
 * Check if a date is in the past
 */
export function isPast(date: Date | undefined): boolean {
  if (!date) return false
  return date < new Date()
}
