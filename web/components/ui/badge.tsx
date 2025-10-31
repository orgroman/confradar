import * as React from "react"

type BadgeVariant = "default" | "secondary" | "outline"

export function Badge({ className = "", variant = "default", ...props }: React.HTMLAttributes<HTMLSpanElement> & { variant?: BadgeVariant }) {
  const variants: Record<BadgeVariant, string> = {
    default: "bg-primary text-primary-foreground",
    secondary: "bg-secondary text-secondary-foreground",
    outline: "border border-input bg-transparent text-foreground",
  }
  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variants[variant],
        className,
      ].join(" ")}
      {...props}
    />
  )
}
