export interface Conference {
  id: string
  name: string
  acronym?: string
  location?: string
  startDate?: Date
  endDate?: Date
  submissionDeadline?: Date
  notificationDate?: Date
  website?: string
  status?: "upcoming" | "ongoing" | "past"
}
