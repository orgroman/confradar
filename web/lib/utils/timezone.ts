import { zonedTimeToUtc, utcToZonedTime, format } from "date-fns-tz"

export function convertToAoE(dateString: string): Date {
  // AoE is UTC-12
  const aoeTimezone = "Etc/GMT+12"
  return utcToZonedTime(dateString, aoeTimezone)
}

export function convertFromAoE(date: Date): Date {
  const aoeTimezone = "Etc/GMT+12"
  return zonedTimeToUtc(date, aoeTimezone)
}

export function formatInTimezone(dateString: string, timezone: string, formatStr = "MMM d, yyyy h:mm a zzz"): string {
  const zonedDate = utcToZonedTime(dateString, timezone)
  return format(zonedDate, formatStr, { timeZone: timezone })
}

export function getAoEDeadline(dateString: string): string {
  return formatInTimezone(dateString, "Etc/GMT+12")
}
