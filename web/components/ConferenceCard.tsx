import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Badge } from "./ui/badge"
import { Calendar, MapPin } from "lucide-react"
import { formatDate } from "../lib/utils/date"
import type { Conference } from "../lib/api/types"

interface ConferenceCardProps {
  conference: Conference
}

export function ConferenceCard({ conference }: ConferenceCardProps) {
  const nextDeadline = conference.deadlines[0]

  return (
    <Link href={`/conferences/${conference.id}`}>
      <Card className="h-full transition-shadow hover:shadow-md">
        <CardHeader>
          <div className="mb-2 flex flex-wrap gap-2">
            {conference.tags.slice(0, 2).map((tag: string) => (
              <Badge key={tag} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
          <CardTitle className="text-balance text-lg">{conference.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <MapPin className="size-4 shrink-0" />
              <span className="truncate">
                {conference.location.city}, {conference.location.country}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="size-4 shrink-0" />
              <span>
                {formatDate(conference.startDate)} - {formatDate(conference.endDate)}
              </span>
            </div>
            {nextDeadline && (
              <div className="mt-4 rounded-lg bg-muted p-3">
                <p className="mb-1 text-xs font-medium text-foreground">Next Deadline</p>
                <p className="text-xs">{nextDeadline.name}</p>
                <p className="text-xs font-medium">{formatDate(nextDeadline.date)}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
