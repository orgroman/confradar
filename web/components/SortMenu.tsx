"use client"

import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { ArrowUpDown } from "lucide-react"

export function SortMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm">
          <ArrowUpDown className="mr-2 size-4" />
          Sort
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem>Deadline (Earliest)</DropdownMenuItem>
        <DropdownMenuItem>Deadline (Latest)</DropdownMenuItem>
        <DropdownMenuItem>Name (A-Z)</DropdownMenuItem>
        <DropdownMenuItem>Name (Z-A)</DropdownMenuItem>
        <DropdownMenuItem>Date Added</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
