import type { Conference, ConferenceFilters } from "./types"
import conferencesData from "@/mocks/conferences.json"

// Simulated API delay
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

export async function getConferences(filters?: ConferenceFilters): Promise<Conference[]> {
  await delay(300)

  let conferences = conferencesData as Conference[]

  // Apply filters
  if (filters?.tags && filters.tags.length > 0) {
    conferences = conferences.filter((conf) => filters.tags!.some((tag) => conf.tags.includes(tag)))
  }

  if (filters?.search) {
    const searchLower = filters.search.toLowerCase()
    conferences = conferences.filter(
      (conf) => conf.name.toLowerCase().includes(searchLower) || conf.description.toLowerCase().includes(searchLower),
    )
  }

  // Apply sorting
  if (filters?.sortBy) {
    conferences = [...conferences].sort((a, b) => {
      let comparison = 0
      switch (filters.sortBy) {
        case "deadline":
          comparison =
            new Date(a.deadlines[0]?.date || a.startDate).getTime() -
            new Date(b.deadlines[0]?.date || b.startDate).getTime()
          break
        case "name":
          comparison = a.name.localeCompare(b.name)
          break
        case "date":
          comparison = new Date(a.startDate).getTime() - new Date(b.startDate).getTime()
          break
      }
      return filters.sortOrder === "desc" ? -comparison : comparison
    })
  }

  return conferences
}

export async function getConferenceById(id: string): Promise<Conference | null> {
  await delay(200)
  const conferences = conferencesData as Conference[]
  return conferences.find((conf) => conf.id === id) || null
}
