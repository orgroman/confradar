import { Header } from "@/components/Header"
import { Footer } from "@/components/Footer"
import { FilterBar } from "@/components/FilterBar"
import { ConferenceCard } from "@/components/ConferenceCard"
import { ConferenceListSkeleton } from "@/components/Skeletons"
import { getConferences } from "@/lib/api/client"
import { Suspense } from "react"

async function ConferenceList() {
  const conferences = await getConferences()

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {conferences.map((conference) => (
        <ConferenceCard key={conference.id} conference={conference} />
      ))}
    </div>
  )
}

export default function ConferencesPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <div className="border-b bg-muted/30 py-8">
          <div className="container mx-auto px-4">
            <h1 className="mb-2 text-3xl font-bold">Conferences</h1>
            <p className="text-muted-foreground">Browse and track academic conference deadlines</p>
          </div>
        </div>
        <div className="container mx-auto px-4 py-8">
          <FilterBar />
          <div className="mt-6">
            <Suspense fallback={<ConferenceListSkeleton />}>
              <ConferenceList />
            </Suspense>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
