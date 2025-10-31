import { describe, it, expect } from "vitest"

// TODO: Fix Vitest path alias resolution for @/lib imports in CI
// Tracked in issue #148 - Vercel deployment and proper frontend testing setup
describe.skip("ConferenceCard", () => {
  it.skip("placeholder - tests temporarily disabled pending alias resolution fix", () => {
    expect(true).toBe(true)
  })
})
