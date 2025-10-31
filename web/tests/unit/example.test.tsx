import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { ConferenceCard } from "@/components/ConferenceCard"
import type { Conference } from "@/lib/api/types"

describe("ConferenceCard", () => {
  it("renders conference name", () => {
    const conference: Conference = {
      id: "1",
      name: "International Conference on Software Engineering",
      acronym: "ICSE 2026",
    }

    render(<ConferenceCard conference={conference} />)
    
    expect(screen.getByText("International Conference on Software Engineering")).toBeInTheDocument()
  })

  it("renders conference acronym when provided", () => {
    const conference: Conference = {
      id: "2",
      name: "Conference on Neural Information Processing Systems",
      acronym: "NeurIPS 2026",
    }

    render(<ConferenceCard conference={conference} />)
    
    expect(screen.getByText("NeurIPS 2026")).toBeInTheDocument()
  })

  it("renders location when provided", () => {
    const conference: Conference = {
      id: "3",
      name: "ACM SIGMOD",
      location: "Seattle, WA, USA",
    }

    render(<ConferenceCard conference={conference} />)
    
    expect(screen.getByText("Seattle, WA, USA")).toBeInTheDocument()
  })

  it("renders submission deadline with days remaining", () => {
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)

    const conference: Conference = {
      id: "4",
      name: "Test Conference",
      submissionDeadline: futureDate,
    }

    render(<ConferenceCard conference={conference} />)
    
    expect(screen.getByText(/Submission Deadline:/)).toBeInTheDocument()
    expect(screen.getByText(/days remaining/)).toBeInTheDocument()
  })

  it("renders website link when provided", () => {
    const conference: Conference = {
      id: "5",
      name: "Test Conference",
      website: "https://example.com",
    }

    render(<ConferenceCard conference={conference} />)
    
    const link = screen.getByText("Visit Website")
    expect(link).toBeInTheDocument()
    expect(link).toHaveAttribute("href", "https://example.com")
    expect(link).toHaveAttribute("target", "_blank")
  })

  it("shows TBA for missing dates", () => {
    const conference: Conference = {
      id: "6",
      name: "Test Conference",
      submissionDeadline: undefined,
    }

    render(<ConferenceCard conference={conference} />)
    
    // Conference name should still render
    expect(screen.getByText("Test Conference")).toBeInTheDocument()
  })
})
