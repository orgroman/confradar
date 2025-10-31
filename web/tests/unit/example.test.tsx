import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { ConferenceCard } from "@/components/ConferenceCard"
import type { Conference } from "@/lib/api/types"

const mockConference: Conference = {
  id: "test-conf",
  name: "Test Conference 2025",
  description: "A test conference",
  startDate: "2025-06-01",
  endDate: "2025-06-05",
  location: {
    venue: "Test Venue",
    city: "Test City",
    country: "Test Country",
  },
  deadlines: [
    {
      name: "Paper Submission",
      date: "2025-03-01",
      timezone: "AoE",
    },
  ],
  tags: ["AI/ML", "Computer Science"],
}

describe("ConferenceCard", () => {
  it("renders conference name", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("Test Conference 2025")).toBeDefined()
  })

  it("renders location information", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText(/Test City, Test Country/)).toBeDefined()
  })

  it("renders tags", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("AI/ML")).toBeDefined()
    expect(screen.getByText("Computer Science")).toBeDefined()
  })

  it("renders next deadline", () => {
    render(<ConferenceCard conference={mockConference} />)
    expect(screen.getByText("Next Deadline")).toBeDefined()
    expect(screen.getByText("Paper Submission")).toBeDefined()
  })
})
