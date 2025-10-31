import { Header } from "../../../components/Header"
import { Footer } from "../../../components/Footer"
import { getConferenceById } from "../../../lib/api/client"
import { Badge } from "../../../components/ui/badge"
import { Button } from "../../../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../../../components/ui/card"
import { Calendar, MapPin, ExternalLink, Download } from "lucide-react"
import { formatDate } from "../../../lib/utils/date"
import { notFound } from "next/navigation"
import type { Deadline } from "../../../lib/api/types"

export default async function ConferenceDetailPage({
  params,
}: {
  params: { id: string }
}) {
  const { id } = params
  const conference = await getConferenceById(id)

  if (!conference) {
    notFound()
    return null
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <div className="border-b bg-muted/30 py-8">
          <div className="container mx-auto px-4">
            <div className="mb-4 flex flex-wrap gap-2">
              {conference.tags.map((tag: string) => (
                <Badge key={tag} variant="secondary">
                  {tag}
                </Badge>
              ))}
            </div>
            <h1 className="mb-2 text-balance text-3xl font-bold md:text-4xl">{conference.name}</h1>
            <div className="flex flex-wrap items-center gap-4 text-muted-foreground">
              <div className="flex items-center gap-2">
                <MapPin className="size-4" />
                <span>
                  {conference.location.city}, {conference.location.country}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <Calendar className="size-4" />
                <span>
                  {formatDate(conference.startDate)} - {formatDate(conference.endDate)}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-4 py-8">
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>About</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{conference.description}</p>
                  {conference.website && (
                    <Button asChild variant="ghost" className="mt-4 px-0">
                      <a href={conference.website} target="_blank" rel="noopener noreferrer">
                        Visit Conference Website
                        <ExternalLink className="ml-2 size-4" />
                      </a>
                    </Button>
                  )}
                </CardContent>
              </Card>

              <Card className="mt-6">
                <CardHeader>
                  <CardTitle>Location</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <p>
                      <span className="font-medium">Venue:</span> {conference.location.venue}
                    </p>
                    <p>
                      <span className="font-medium">City:</span> {conference.location.city}
                    </p>
                    <p>
                      <span className="font-medium">Country:</span> {conference.location.country}
                    </p>
                  </div>
                  <div className="mt-4 h-48 rounded-lg bg-muted flex items-center justify-center text-muted-foreground">
                    Map placeholder
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Important Dates</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {conference.deadlines.map((deadline: Deadline, index: number) => (
                    <div key={index} className="border-b pb-4 last:border-0">
                      <p className="mb-1 font-medium">{deadline.name}</p>
                      <p className="text-sm text-muted-foreground">{formatDate(deadline.date)}</p>
                      {deadline.timezone && <p className="text-xs text-muted-foreground">{deadline.timezone}</p>}
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button className="w-full bg-transparent" variant="outline">
                    <Download className="mr-2 size-4" />
                    Export to Calendar
                  </Button>
                  <Button className="w-full bg-transparent" variant="outline">
                    Toggle Timezone (AoE)
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
