"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"

type ButtonVariant = "default" | "outline" | "ghost"
type ButtonSize = "sm" | "md" | "lg"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
  variant?: ButtonVariant
  size?: ButtonSize
}

const base =
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"

const variants: Record<ButtonVariant, string> = {
  default: "bg-primary text-primary-foreground hover:opacity-90",
  outline: "border border-input bg-transparent hover:bg-accent hover:text-foreground",
  ghost: "bg-transparent hover:bg-accent",
}

const sizes: Record<ButtonSize, string> = {
  sm: "h-8 px-3",
  md: "h-9 px-4",
  lg: "h-10 px-6",
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", asChild, variant = "default", size = "md", ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    const cls = [base, variants[variant as ButtonVariant], sizes[size as ButtonSize], className].join(" ")
    return <Comp ref={ref as any} className={cls} {...props} />
  },
)

Button.displayName = "Button"
