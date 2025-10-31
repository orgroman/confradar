import type { Conference } from "@/lib/api/types"
import { formatDate, daysUntil, isPast } from "@/lib/utils/date"

export interface ConferenceCardProps {
  conference: Conference
}

export function ConferenceCard({ conference }: ConferenceCardProps) {
  const days = daysUntil(conference.submissionDeadline)
  const deadlinePassed = isPast(conference.submissionDeadline)

  return (
    <div className="conference-card">
      <h3>{conference.name}</h3>
      {conference.acronym && <p className="acronym">{conference.acronym}</p>}
      {conference.location && <p className="location">{conference.location}</p>}
      
      <div className="dates">
        {conference.startDate && conference.endDate && (
          <p>
            Conference: {formatDate(conference.startDate)} - {formatDate(conference.endDate)}
          </p>
        )}
        
        {conference.submissionDeadline && (
          <p className={deadlinePassed ? "deadline-passed" : "deadline-active"}>
            Submission Deadline: {formatDate(conference.submissionDeadline)}
            {days !== null && !deadlinePassed && ` (${days} days remaining)`}
          </p>
        )}
        
        {conference.notificationDate && (
          <p>
            Notification: {formatDate(conference.notificationDate)}
          </p>
        )}
      </div>
      
      {conference.website && (
        <a href={conference.website} target="_blank" rel="noopener noreferrer">
          Visit Website
        </a>
      )}
    </div>
  )
}
