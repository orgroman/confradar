import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { ConferenceCard } from "@/components/ConferenceCard"
import type { Conference } from "@/lib/api/types"

describe("ConferenceCard", () => {
  const mockConference: Conference = {
    id: "test-1",
    name: "Test Conference 2025",
    description: "A test conference",
    website: "https://test.com",
    startDate: "2025-06-01",
    endDate: "2025-06-05",
    location: {
      venue: "Test Center",
      city: "San Francisco",
      country: "USA",
    },
    deadlines: [
      {
        name: "Abstract Submission",
        date: "2025-03-01",
        timezone: "UTC",
      },
    ],
    tags: ["AI", "ML"],
  }

  it("renders conference name", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("Test Conference 2025")).toBeDefined()
  })

  it("renders location information", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText(/San Francisco, USA/)).toBeDefined()
  })

  it("renders tags", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("AI")).toBeDefined()
    expect(screen.getByText("ML")).toBeDefined()
  })

  it("renders next deadline when available", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("Next Deadline")).toBeDefined()
    expect(screen.getByText("Abstract Submission")).toBeDefined()
  })
})
