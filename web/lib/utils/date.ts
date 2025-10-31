import { format, parseISO } from "date-fns"

export function formatDate(dateString: string, formatStr = "MMM d, yyyy"): string {
  try {
    const date = parseISO(dateString)
    return format(date, formatStr)
  } catch {
    return dateString
  }
}

export function formatDateTime(dateString: string): string {
  return formatDate(dateString, "MMM d, yyyy h:mm a")
}

export function isUpcoming(dateString: string): boolean {
  const date = parseISO(dateString)
  return date > new Date()
}

export function isPast(dateString: string): boolean {
  const date = parseISO(dateString)
  return date < new Date()
}
