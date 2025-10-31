export interface Conference {
  id: string
  name: string
  description: string
  website?: string
  startDate: string
  endDate: string
  location: Location
  deadlines: Deadline[]
  tags: string[]
}

export interface Location {
  venue: string
  city: string
  country: string
  coordinates?: {
    lat: number
    lng: number
  }
}

export interface Deadline {
  name: string
  date: string
  timezone?: string
}

export interface ConferenceFilters {
  tags?: string[]
  search?: string
  sortBy?: "deadline" | "name" | "date"
  sortOrder?: "asc" | "desc"
}
