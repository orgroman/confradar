import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/Header"
import { Footer } from "@/components/Footer"
import { Calendar, Clock, MapPin } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <section className="container mx-auto px-4 py-16 md:py-24">
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="mb-6 text-balance text-4xl font-bold tracking-tight md:text-6xl">
              Never Miss a Conference Deadline
            </h1>
            <p className="mb-8 text-pretty text-lg text-muted-foreground md:text-xl">
              Track important dates, locations, and submission deadlines for academic conferences. Stay organized and
              submit on time.
            </p>
            <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button asChild size="lg">
                <Link href="/conferences">Browse Conferences</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/conferences">View All Deadlines</Link>
              </Button>
            </div>
          </div>
        </section>

        <section className="border-t bg-muted/30 py-16">
          <div className="container mx-auto px-4">
            <div className="mx-auto grid max-w-5xl gap-8 md:grid-cols-3">
              <div className="flex flex-col items-center text-center">
                <div className="mb-4 flex size-12 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <Calendar className="size-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold">Track Deadlines</h3>
                <p className="text-sm text-muted-foreground">
                  Keep track of submission deadlines with timezone support including AoE (Anywhere on Earth).
                </p>
              </div>
              <div className="flex flex-col items-center text-center">
                <div className="mb-4 flex size-12 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <MapPin className="size-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold">Location Details</h3>
                <p className="text-sm text-muted-foreground">
                  View conference locations, venues, and travel information all in one place.
                </p>
              </div>
              <div className="flex flex-col items-center text-center">
                <div className="mb-4 flex size-12 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <Clock className="size-6" />
                </div>
                <h3 className="mb-2 text-lg font-semibold">Stay Organized</h3>
                <p className="text-sm text-muted-foreground">
                  Filter, sort, and organize conferences by field, deadline, or location.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
