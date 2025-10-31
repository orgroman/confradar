import React from "react"
import ReactDOM from "react-dom/client"
import { ConferenceCard } from "@/components/ConferenceCard"
import type { Conference } from "@/lib/api/types"

const sampleConference: Conference = {
  id: "1",
  name: "International Conference on Software Engineering",
  acronym: "ICSE 2026",
  location: "Pittsburgh, PA, USA",
  startDate: new Date("2026-05-15"),
  endDate: new Date("2026-05-20"),
  submissionDeadline: new Date("2026-01-15"),
  notificationDate: new Date("2026-03-01"),
  website: "https://conf.researchr.org/home/icse-2026",
  status: "upcoming",
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div style={{ padding: "2rem" }}>
      <h1>ConfRadar</h1>
      <ConferenceCard conference={sampleConference} />
    </div>
  </React.StrictMode>
)
