"use client"

import { Button } from "./ui/button"
import { Badge } from "./ui/badge"
import { LayoutGrid, List, SlidersHorizontal } from "lucide-react"
import { usePrefsStore } from "../lib/state/prefs"

export function FilterBar() {
  const { viewMode, setViewMode } = usePrefsStore()

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-wrap gap-2">
        <Badge variant="outline" className="cursor-pointer hover:bg-accent">
          Computer Science
        </Badge>
        <Badge variant="outline" className="cursor-pointer hover:bg-accent">
          AI/ML
        </Badge>
        <Badge variant="outline" className="cursor-pointer hover:bg-accent">
          Upcoming
        </Badge>
        <Button variant="ghost" size="sm">
          <SlidersHorizontal className="mr-2 size-4" />
          More Filters
        </Button>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground">View:</span>
        <Button variant={viewMode === "grid" ? "default" : "outline"} size="sm" onClick={() => setViewMode("grid")}>
          <LayoutGrid className="size-4" />
        </Button>
        <Button variant={viewMode === "list" ? "default" : "outline"} size="sm" onClick={() => setViewMode("list")}>
          <List className="size-4" />
        </Button>
      </div>
    </div>
  )
}
