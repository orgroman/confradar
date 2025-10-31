import Link from "next/link"
import { Button } from "@/components/ui/button"

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
            CR
          </div>
          <span className="text-xl font-bold">ConfRadar</span>
        </Link>
        <nav className="flex items-center gap-6">
          <Link
            href="/conferences"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Conferences
          </Link>
          <Button variant="ghost" size="sm">
            Sign In
          </Button>
        </nav>
      </div>
    </header>
  )
}
