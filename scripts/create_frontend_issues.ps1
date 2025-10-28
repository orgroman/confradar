# Script to create all frontend issues for ConfRadar

# Infrastructure & Setup (#88)
gh issue create --title "Select and configure frontend framework" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Evaluate and select the appropriate frontend framework for ConfRadar, then set up the initial project structure.

## Options to Consider
- React with Vite
- Next.js (for SSR/SEO benefits)
- Vue 3 with Vite

## Tasks
- [ ] Research framework options
- [ ] Consider SEO requirements
- [ ] Set up project with chosen framework
- [ ] Configure TypeScript
- [ ] Set up ESLint and Prettier
- [ ] Create initial folder structure

## Acceptance Criteria
- Framework selected with documented rationale
- Project scaffolded with dev server running
- TypeScript configured
- Linting and formatting working
- Basic routing set up

## Priority
High

## Estimated Effort
3-5 days
"@

gh issue create --title "Set up UI component library and styling system" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Choose and configure a UI component library and styling approach for consistent, responsive design.

## Options
- Tailwind CSS (utility-first)
- Material-UI / MUI
- Ant Design
- Chakra UI
- shadcn/ui (for modern React)

## Tasks
- [ ] Select styling approach
- [ ] Install and configure chosen library
- [ ] Set up design tokens (colors, spacing, typography)
- [ ] Create base component wrappers if needed
- [ ] Set up responsive breakpoints
- [ ] Configure theme provider

## Acceptance Criteria
- Styling system installed and working
- Example components render correctly
- Responsive design utilities available
- Theme configuration documented

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Configure state management solution" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Set up state management for handling application state, API data, and user preferences.

## Options
- React Context + Hooks (for simple needs)
- Zustand (lightweight)
- Redux Toolkit
- TanStack Query (React Query) for server state
- Pinia (for Vue)

## Tasks
- [ ] Evaluate state management needs
- [ ] Choose solution(s) (may use multiple)
- [ ] Install and configure
- [ ] Set up stores/contexts for:
  - Conference data
  - Filter state
  - User preferences
  - UI state
- [ ] Create example state slice
- [ ] Document state management patterns

## Acceptance Criteria
- State management configured
- Clear separation of client/server state
- Patterns documented
- Developer experience is smooth

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Set up routing and navigation structure" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Configure client-side routing for the application with proper navigation structure.

## Routes Needed
- `/` - Home/Conference list
- `/conferences/:id` - Conference detail
- `/settings` - User settings (future)
- `/about` - About page (optional)

## Tasks
- [ ] Configure router (React Router / Vue Router / Next.js routing)
- [ ] Define route structure
- [ ] Set up navigation component
- [ ] Implement 404 page
- [ ] Configure route guards if needed
- [ ] Set up URL query param handling for filters

## Acceptance Criteria
- All routes defined and working
- Navigation between pages works
- URL parameters handled correctly
- 404 page shows for invalid routes
- Browser back/forward works correctly

## Priority
High

## Estimated Effort
2 days
"@

gh issue create --title "Configure build tools and optimization" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Set up build configuration, bundling, and optimization for production deployments.

## Tasks
- [ ] Configure build tool (Vite/Webpack/Next.js built-in)
- [ ] Set up environment variables handling
- [ ] Configure code splitting
- [ ] Set up bundle analysis
- [ ] Configure compression (gzip/brotli)
- [ ] Set up asset optimization (images, fonts)
- [ ] Configure source maps for debugging
- [ ] Set up production vs development builds

## Acceptance Criteria
- Production build generates optimized bundle
- Build completes in reasonable time
- Bundle size is optimized (<500KB initial)
- Environment variables work correctly
- Source maps available for debugging

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Set up CI/CD pipeline for frontend" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Create automated CI/CD pipeline for testing, building, and deploying the frontend.

## Tasks
- [ ] Set up GitHub Actions workflow
- [ ] Configure linting in CI
- [ ] Add build step
- [ ] Add test execution
- [ ] Set up deployment (Vercel/Netlify/AWS)
- [ ] Configure preview deployments for PRs
- [ ] Add build status badges
- [ ] Set up environment-specific deployments

## Acceptance Criteria
- CI runs on every PR
- Builds fail on linting errors
- Tests run automatically
- Successful builds deploy to staging
- PR previews available
- Production deployment process documented

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Configure testing framework and setup" --label "frontend,enhancement" --body @"
## Epic
#88 Frontend Infrastructure & Project Setup

## Description
Set up testing infrastructure including unit, integration, and E2E testing frameworks.

## Tasks
- [ ] Install Jest or Vitest for unit tests
- [ ] Set up React Testing Library / Vue Test Utils
- [ ] Configure test environment
- [ ] Install Playwright or Cypress for E2E
- [ ] Create test utilities and helpers
- [ ] Set up coverage reporting
- [ ] Add example tests
- [ ] Document testing patterns

## Acceptance Criteria
- Unit testing framework working
- E2E framework configured
- Example tests pass
- Coverage reports generated
- Testing documentation complete

## Priority
High

## Estimated Effort
3-4 days
"@

# Conference List View (#89)
gh issue create --title "Create conference list page layout" --label "frontend,enhancement" --body @"
## Epic
#89 Conference List View & Display

## Description
Implement the main conference list page with basic layout and structure.

## Tasks (PRD FR-1)
- [ ] Create ConferenceList page component
- [ ] Design layout (header, filter sidebar, main content)
- [ ] Create placeholder for search bar
- [ ] Create placeholder for filter panel
- [ ] Set up main content area for conference cards/table
- [ ] Add header with app branding
- [ ] Implement basic responsive breakpoints

## Acceptance Criteria
- Page layout renders correctly
- Responsive on mobile, tablet, desktop
- Header and navigation in place
- Content areas properly structured
- Clean, academic design aesthetic

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Design and implement conference card component" --label "frontend,enhancement" --body @"
## Epic
#89 Conference List View & Display

## Description
Create reusable conference card/row component to display conference information in the list.

## Tasks (PRD FR-1)
- [ ] Design card layout for desktop (table row style)
- [ ] Design card layout for mobile (stacked card style)
- [ ] Include: name, acronym, year, location
- [ ] Add next deadline with countdown
- [ ] Add status badge (Open/Closed/Upcoming)
- [ ] Add last updated timestamp
- [ ] Make card clickable to detail view
- [ ] Add hover effects
- [ ] Handle long text truncation
- [ ] Add loading skeleton variant

## Acceptance Criteria
- Card displays all required info
- Responsive design works
- Countdown updates correctly
- Status colors are clear
- Accessible (keyboard nav, ARIA labels)

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Implement deadline countdown and status indicators" --label "frontend,enhancement" --body @"
## Epic
#89 Conference List View & Display

## Description
Add deadline countdown timers and visual status indicators for conferences.

## Tasks (PRD FR-1, FR-10)
- [ ] Create countdown component (X days remaining)
- [ ] Calculate time until next deadline
- [ ] Update countdown in real-time or periodically
- [ ] Create status badge component
- [ ] Define status logic (Open, Closed, Upcoming, Ongoing)
- [ ] Add color coding for urgency
- [ ] Highlight deadlines within 7 days
- [ ] Show "Deadline Passed" for closed conferences

## Acceptance Criteria
- Countdown shows correct days/hours
- Status badges display correctly
- Urgent deadlines visually highlighted
- Updates without full page refresh
- Works across timezones

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Implement responsive table/card view toggle" --label "frontend,enhancement" --body @"
## Epic
#89 Conference List View & Display

## Description
Create responsive layout that switches between table and card views based on screen size.

## Tasks (PRD FR-13)
- [ ] Design table view for desktop
- [ ] Design card view for mobile/tablet
- [ ] Implement automatic switching at breakpoints
- [ ] Add optional manual toggle (desktop users)
- [ ] Ensure all data visible in both views
- [ ] Test on various screen sizes
- [ ] Optimize touch interactions for mobile

## Acceptance Criteria
- Table view on desktop (>1024px)
- Card view on mobile (<768px)
- Smooth transitions between views
- All features work in both modes
- Touch-friendly on mobile

## Priority
High

## Estimated Effort
3 days
"@

gh issue create --title "Add pagination or infinite scroll for conference list" --label "frontend,enhancement" --body @"
## Epic
#89 Conference List View & Display

## Description
Implement pagination or infinite scroll to handle large numbers of conferences efficiently.

## Tasks
- [ ] Decide: pagination vs infinite scroll
- [ ] Implement chosen approach
- [ ] Add loading indicators
- [ ] Handle page state in URL
- [ ] Add "back to top" button (if infinite scroll)
- [ ] Optimize rendering performance
- [ ] Test with large datasets (100+ conferences)

## Acceptance Criteria
- List handles 500+ conferences smoothly
- Load time under 2 seconds
- No lag when scrolling
- State persists on back navigation
- Mobile performance is good

## Priority
Medium

## Estimated Effort
2-3 days
"@

# Search & Filtering (#90)
gh issue create --title "Implement search bar with real-time filtering" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Create search functionality that filters conferences by name, acronym, or keywords in real-time.

## Tasks (PRD FR-2)
- [ ] Create SearchBar component
- [ ] Add input field with icon
- [ ] Implement debounced search (300ms)
- [ ] Search across: name, full_name, acronym
- [ ] Highlight matching text (optional)
- [ ] Add clear button
- [ ] Show "no results" message
- [ ] Make search case-insensitive
- [ ] Update URL with search param

## Acceptance Criteria
- Search updates list within 300ms
- Matches partial text
- Works with other filters
- Mobile-friendly input
- Accessible keyboard navigation

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Create filter panel with deadline date range picker" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Implement filter panel with date range picker for filtering by deadline dates.

## Tasks (PRD FR-3)
- [ ] Create FilterPanel component
- [ ] Add date range picker component
- [ ] Add quick filters (Next 7 days, Next month, etc.)
- [ ] Filter conferences by submission deadline
- [ ] Update list when dates change
- [ ] Show active filters clearly
- [ ] Add "Clear date filter" option
- [ ] Mobile-friendly date picker

## Acceptance Criteria
- Date picker works correctly
- Filters apply instantly
- Quick filters work
- Mobile-optimized
- Handles edge cases (no deadline, TBA)

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Add location and region filters" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Implement location-based filtering for conferences by region, country, or virtual.

## Tasks (PRD FR-4)
- [ ] Create location filter component
- [ ] Add country multi-select
- [ ] Add region grouping (Europe, Asia, Americas, etc.)
- [ ] Add "Virtual" filter option
- [ ] Fetch available locations from API or config
- [ ] Show conference count per location
- [ ] Allow multiple location selection
- [ ] Update URL with location params

## Acceptance Criteria
- Location filter works correctly
- Multi-select functional
- Virtual conferences filterable
- Shows correct counts
- Mobile-friendly

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Implement field/category tag filtering" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Add filtering by research field or conference category tags.

## Tasks (PRD FR-5)
- [ ] Create tag/category filter component
- [ ] Fetch available tags from API
- [ ] Display as multi-select or tag cloud
- [ ] Allow multiple tag selection
- [ ] Show conference count per tag
- [ ] Support AND/OR logic (optional)
- [ ] Update URL with tag params
- [ ] Add popular tags shortcuts

## Acceptance Criteria
- Tag filtering works
- Multiple tags selectable
- Clear what's selected
- Mobile-friendly
- Performance with many tags

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Add sort functionality for conference list" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Implement sorting options for the conference list.

## Tasks (PRD FR-10)
- [ ] Create sort dropdown/buttons
- [ ] Add sort by: Deadline (soonest first)
- [ ] Add sort by: Conference Name (A-Z)
- [ ] Add sort by: Conference Date
- [ ] Add sort by: Recently Updated
- [ ] Support ascending/descending
- [ ] Remember sort preference
- [ ] Update URL with sort param

## Acceptance Criteria
- All sort options work correctly
- Default sort is logical
- Sort persists in session
- Clear indication of current sort
- Fast sorting (no lag)

## Priority
Medium

## Estimated Effort
2 days
"@

gh issue create --title "Create active filter chips and clear filters UI" --label "frontend,enhancement" --body @"
## Epic
#90 Search & Filtering System

## Description
Display active filters as chips/tags and provide easy way to clear them.

## Tasks
- [ ] Create filter chip component
- [ ] Show all active filters as chips
- [ ] Add X button to remove individual filter
- [ ] Add "Clear All Filters" button
- [ ] Update list when filters removed
- [ ] Show filter count in panel
- [ ] Animate chip additions/removals
- [ ] Mobile-optimized chip layout

## Acceptance Criteria
- Active filters clearly visible
- Easy to remove filters
- Clear all works correctly
- Mobile-friendly
- Accessible

## Priority
Medium

## Estimated Effort
2 days
"@

# Conference Detail View (#91)
gh issue create --title "Create conference detail page layout" --label "frontend,enhancement" --body @"
## Epic
#91 Conference Detail View

## Description
Implement the conference detail page with structured layout for all conference information.

## Tasks (PRD FR-6)
- [ ] Create ConferenceDetail page component
- [ ] Design layout structure
- [ ] Add header section (name, year, status)
- [ ] Add conference dates section
- [ ] Add location section with map link
- [ ] Add website link prominently
- [ ] Add deadlines table/list section
- [ ] Add notes/description section
- [ ] Add back to list navigation
- [ ] Make responsive for mobile

## Acceptance Criteria
- Clean, readable layout
- All sections properly organized
- Responsive design
- Loads within 2 seconds
- Accessible

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Implement important dates section with all deadlines" --label "frontend,enhancement" --body @"
## Epic
#91 Conference Detail View

## Description
Create detailed display of all conference deadlines and important dates.

## Tasks (PRD FR-6)
- [ ] Create deadlines table component
- [ ] Show all deadlines chronologically
- [ ] Include: abstract, submission, notification, camera-ready
- [ ] Display date/time with timezone
- [ ] Mark past deadlines (strikethrough/grey)
- [ ] Show "TBA" for unconfirmed dates
- [ ] Add countdown for upcoming deadlines
- [ ] Include deadline notes if available

## Acceptance Criteria
- All deadlines displayed clearly
- Timezone shown correctly
- Past vs future distinction clear
- Mobile-friendly layout
- Easy to scan visually

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Add change history display with timeline" --label "frontend,enhancement" --body @"
## Epic
#91 Conference Detail View

## Description
Implement change history section showing modifications to conference dates.

## Tasks (PRD FR-7)
- [ ] Create ChangeHistory component
- [ ] Design as collapsible section or timeline
- [ ] Display chronologically (newest first)
- [ ] Show: field changed, old value, new value, date
- [ ] Add icons for change types
- [ ] Add "No changes" message if empty
- [ ] Make it clear what was extended/changed
- [ ] Mobile-optimized

## Acceptance Criteria
- Change history visible and clear
- Chronological order correct
- Easy to understand what changed
- Collapsible to save space
- Empty state handled

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Add location details with map integration" --label "frontend,enhancement" --body @"
## Epic
#91 Conference Detail View

## Description
Display conference location details with optional map link or embedded map.

## Tasks (PRD FR-6)
- [ ] Create location display component
- [ ] Show city, country, venue name
- [ ] Add Google Maps link
- [ ] Consider embedded map (optional, check API limits)
- [ ] Handle "Virtual" conferences differently
- [ ] Add timezone of location
- [ ] Link to venue website if available

## Acceptance Criteria
- Location clearly displayed
- Map link works correctly
- Virtual conferences indicated
- Mobile-friendly
- No API limit issues if using map

## Priority
Low (optional enhancement)

## Estimated Effort
1-2 days
"@

gh issue create --title "Add export and share actions to detail page" --label "frontend,enhancement" --body @"
## Epic
#91 Conference Detail View

## Description
Add action buttons to export single conference or share its details.

## Tasks
- [ ] Create action button group
- [ ] Add "Export to Calendar" button
- [ ] Add "Copy Link" button
- [ ] Add social share buttons (optional)
- [ ] Show confirmation toasts
- [ ] Make sticky/fixed on scroll (optional)
- [ ] Mobile-optimized placement

## Acceptance Criteria
- Export single conference to ICS works
- Copy link works
- User feedback (toast/message)
- Mobile-friendly
- Accessible

## Priority
Medium

## Estimated Effort
2 days
"@

# Timezone & Deadline Management (#92)
gh issue create --title "Implement AoE (Anywhere on Earth) timezone toggle" --label "frontend,enhancement" --body @"
## Epic
#92 Timezone & Deadline Management

## Description
Create toggle switch to view deadlines in AoE time (UTC-12) or local time.

## Tasks (PRD FR-8)
- [ ] Create AoE toggle component
- [ ] Add tooltip explaining AoE
- [ ] Implement UTC-12 conversion logic
- [ ] Update all deadline displays when toggled
- [ ] Show "AoE" label when enabled
- [ ] Persist toggle state in localStorage
- [ ] Add to header or settings panel
- [ ] Test conversion accuracy thoroughly

## Acceptance Criteria
- Toggle switches AoE on/off
- All deadlines update correctly
- AoE label shows when enabled
- Conversion is accurate (UTC-12)
- State persists across sessions
- Tooltip is helpful

## Priority
High (critical feature)

## Estimated Effort
3-4 days
"@

gh issue create --title "Add custom timezone selector" --label "frontend,enhancement" --body @"
## Epic
#92 Timezone & Deadline Management

## Description
Allow users to select their preferred timezone for viewing deadlines.

## Tasks (PRD FR-9)
- [ ] Create timezone selector component
- [ ] Use timezone library (Luxon/date-fns-tz)
- [ ] Auto-detect browser timezone as default
- [ ] Provide timezone dropdown with search
- [ ] Group timezones by region
- [ ] Convert all deadlines to selected timezone
- [ ] Save preference in localStorage
- [ ] Show current timezone in UI

## Acceptance Criteria
- Timezone selection works
- Auto-detection works
- All times convert correctly
- Dropdown searchable
- Mobile-friendly
- Preference persists

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Implement robust date/time conversion utilities" --label "frontend,enhancement" --body @"
## Epic
#92 Timezone & Deadline Management

## Description
Create utility functions and hooks for handling date/time conversions throughout the app.

## Tasks (PRD FR-8, FR-9)
- [ ] Choose date library (Luxon recommended)
- [ ] Create conversion utilities
- [ ] Handle AoE conversion (UTC-12)
- [ ] Handle custom timezone conversion
- [ ] Create hooks: useDeadlineTime, useConferenceDate
- [ ] Test daylight saving time transitions
- [ ] Test edge cases (year boundaries, etc.)
- [ ] Write comprehensive unit tests
- [ ] Document timezone handling

## Acceptance Criteria
- All conversions accurate
- DST handled correctly
- Edge cases tested
- Unit tests >90% coverage
- Well documented

## Priority
High (critical infrastructure)

## Estimated Effort
4-5 days
"@

gh issue create --title "Add timezone labels and indicators throughout UI" --label "frontend,enhancement" --body @"
## Epic
#92 Timezone & Deadline Management

## Description
Ensure timezone information is clearly displayed wherever dates/times are shown.

## Tasks
- [ ] Add timezone labels to all deadline displays
- [ ] Create consistent format (e.g., "Jan 10, 2026 23:59 AoE")
- [ ] Add timezone in list view (subtle)
- [ ] Add timezone in detail view (clear)
- [ ] Show current display timezone in header
- [ ] Add tooltips for timezone info
- [ ] Ensure consistency across all components

## Acceptance Criteria
- Timezone always visible with times
- Consistent formatting
- Clear without cluttering UI
- Tooltips helpful
- Mobile-friendly

## Priority
High

## Estimated Effort
2-3 days
"@

# Calendar Export (#93)
gh issue create --title "Implement ICS file generation for calendar export" --label "frontend,enhancement" --body @"
## Epic
#93 Calendar Export & Integration

## Description
Create ICS (iCalendar) file generation functionality for exporting conference deadlines.

## Tasks (PRD FR-11)
- [ ] Choose/create ICS library (ics.js or similar)
- [ ] Generate ICS for single conference
- [ ] Generate ICS for all visible/filtered conferences
- [ ] Include: deadline name, date/time, location, description
- [ ] Handle timezone in ICS format correctly
- [ ] Add VALARM for reminders (optional)
- [ ] Create download trigger
- [ ] Test on multiple calendar apps

## Acceptance Criteria
- ICS files generate correctly
- Import works in Google Calendar
- Import works in Outlook
- Import works in Apple Calendar
- Timezone handled properly
- Events have proper details

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Add Google Calendar integration links" --label "frontend,enhancement" --body @"
## Epic
#93 Calendar Export & Integration

## Description
Implement one-click Google Calendar integration for adding conferences.

## Tasks (PRD FR-12)
- [ ] Research Google Calendar API/URL scheme
- [ ] Create Google Calendar link generator
- [ ] Generate proper subscription URL
- [ ] Add "Add to Google Calendar" button
- [ ] Test link opening in Google Calendar
- [ ] Handle authenticated vs unauthenticated users
- [ ] Add success feedback

## Acceptance Criteria
- Button opens Google Calendar correctly
- Events subscribe properly
- Works for single conference
- Works for all filtered conferences
- User feedback provided
- Works on mobile

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Create export modal with options" --label "frontend,enhancement" --body @"
## Epic
#93 Calendar Export & Integration

## Description
Build modal/dialog for export options with clear UI for different export choices.

## Tasks
- [ ] Create ExportModal component
- [ ] Add option: Export this conference
- [ ] Add option: Export all conferences
- [ ] Add option: Export filtered results
- [ ] Show ICS download button
- [ ] Show Google Calendar button
- [ ] Add preview of what will be exported
- [ ] Add help text/instructions
- [ ] Mobile-friendly modal

## Acceptance Criteria
- Modal shows export options clearly
- Preview shows number of events
- All export options work
- Mobile-optimized
- Accessible (ESC to close, focus trap)

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Add calendar subscription feed (optional)" --label "frontend,enhancement" --body @"
## Epic
#93 Calendar Export & Integration

## Description
Create subscribable calendar feed URL that auto-updates with new conferences.

## Tasks
- [ ] Coordinate with backend for feed endpoint
- [ ] Generate unique subscription URLs
- [ ] Add "Subscribe" option in UI
- [ ] Provide instructions for adding to calendar apps
- [ ] Test subscription in multiple apps
- [ ] Add option to filter subscription (by field, etc.)

## Acceptance Criteria
- Subscription feed URL works
- Calendar apps can subscribe
- Feed updates automatically
- Instructions are clear
- Works in major calendar apps

## Priority
Low (future enhancement)

## Estimated Effort
3-4 days (includes backend work)
"@

# API Integration (#94)
gh issue create --title "Create API client service layer" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Build the API client service for making requests to the ConfRadar backend.

## Tasks
- [ ] Create API service module
- [ ] Set up Axios or Fetch wrapper
- [ ] Configure base URL and headers
- [ ] Add request/response interceptors
- [ ] Implement error handling
- [ ] Add retry logic for failed requests
- [ ] Set up request timeout
- [ ] Add TypeScript types for API responses
- [ ] Create API documentation

## Acceptance Criteria
- API client working
- Error handling robust
- TypeScript types defined
- Retry logic works
- Well documented

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Implement conference list API integration" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Connect conference list view to backend API with filtering and pagination.

## Tasks (PRD Data Model)
- [ ] Implement GET /api/conferences
- [ ] Pass search query params
- [ ] Pass filter params (deadline, location, field)
- [ ] Pass sort params
- [ ] Handle pagination if needed
- [ ] Parse and transform response
- [ ] Handle loading states
- [ ] Handle errors gracefully

## Acceptance Criteria
- List fetches from API successfully
- Filters work with API
- Search works with API
- Loading states show
- Errors handled gracefully
- Performance is good

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Implement conference detail API integration" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Connect conference detail view to backend API for fetching complete conference data.

## Tasks (PRD Data Model)
- [ ] Implement GET /api/conferences/:id
- [ ] Parse conference detail response
- [ ] Handle change history data
- [ ] Handle missing/optional fields
- [ ] Add loading state
- [ ] Handle 404 errors
- [ ] Add error boundary
- [ ] Cache detail data appropriately

## Acceptance Criteria
- Detail page fetches from API
- All fields displayed correctly
- 404 handled gracefully
- Loading state shown
- Change history works
- Caching reduces redundant calls

## Priority
High

## Estimated Effort
2-3 days
"@

gh issue create --title "Add loading states and skeleton screens" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Implement loading indicators and skeleton screens for better UX during data fetching.

## Tasks (PRD FR-16)
- [ ] Create loading spinner component
- [ ] Create skeleton loaders for:
  - Conference list items
  - Conference detail page
  - Filter panel
- [ ] Add global loading indicator
- [ ] Add progress bar for slow loads
- [ ] Ensure accessibility (aria-busy, etc.)
- [ ] Test on slow connections

## Acceptance Criteria
- Loading states are clear
- Skeleton screens match real content
- No layout shift when loading completes
- Accessible
- Works on slow connections

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Implement error handling and retry logic" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Build robust error handling with user-friendly messages and retry capabilities.

## Tasks (PRD FR-16)
- [ ] Create error boundary component
- [ ] Create error message components
- [ ] Define error types (network, 404, 500, etc.)
- [ ] Show user-friendly error messages
- [ ] Add "Retry" button for failed requests
- [ ] Log errors for debugging
- [ ] Handle offline mode gracefully
- [ ] Add global error toast/notification

## Acceptance Criteria
- Errors caught and handled
- User-friendly messages shown
- Retry button works
- App doesn't crash on errors
- Offline mode handled
- Errors logged appropriately

## Priority
High

## Estimated Effort
3 days
"@

gh issue create --title "Implement data caching and refresh strategy" --label "frontend,enhancement" --body @"
## Epic
#94 API Integration & Data Management

## Description
Add intelligent caching to reduce redundant API calls and improve performance.

## Tasks
- [ ] Implement cache layer (React Query / SWR / custom)
- [ ] Set cache TTL (time to live)
- [ ] Add manual refresh functionality
- [ ] Implement stale-while-revalidate
- [ ] Add "Last updated" indicator
- [ ] Cache invalidation strategy
- [ ] Prefetch detail pages on hover (optional)
- [ ] Test cache behavior

## Acceptance Criteria
- Caching reduces API calls significantly
- Data stays reasonably fresh
- Manual refresh works
- Cache invalidates appropriately
- Performance improved

## Priority
Medium

## Estimated Effort
3-4 days
"@

# Settings & Preferences (#95)
gh issue create --title "Create settings page/modal UI" --label "frontend,enhancement" --body @"
## Epic
#95 Settings & User Preferences

## Description
Build settings interface for user preferences and configuration.

## Tasks (PRD FR-15)
- [ ] Create Settings page or modal
- [ ] Add navigation to settings
- [ ] Design settings layout
- [ ] Add sections for:
  - Timezone preferences
  - Display preferences
  - Filter defaults
  - About/version info
- [ ] Add save/cancel actions
- [ ] Make mobile-friendly

## Acceptance Criteria
- Settings page accessible
- Clean, organized layout
- Mobile-responsive
- Easy to navigate
- Accessible

## Priority
Medium

## Estimated Effort
2-3 days
"@

gh issue create --title "Implement localStorage persistence for preferences" --label "frontend,enhancement" --body @"
## Epic
#95 Settings & User Preferences

## Description
Store user preferences in localStorage for persistence across sessions.

## Tasks (PRD FR-15)
- [ ] Create localStorage utility
- [ ] Store timezone preference
- [ ] Store AoE toggle state
- [ ] Store filter preferences (optional)
- [ ] Store display preferences
- [ ] Load preferences on app init
- [ ] Handle localStorage errors
- [ ] Add clear data option

## Acceptance Criteria
- Preferences persist across sessions
- Loads correctly on app start
- Handles localStorage unavailable
- Clear data works
- No performance impact

## Priority
Medium

## Estimated Effort
2 days
"@

# Testing & QA (#96)
gh issue create --title "Write unit tests for components" --label "frontend,enhancement,testing" --body @"
## Epic
#96 Testing & Quality Assurance

## Description
Create comprehensive unit tests for all React/Vue components.

## Tasks
- [ ] Set up test conventions
- [ ] Test ConferenceCard component
- [ ] Test SearchBar component
- [ ] Test FilterPanel components
- [ ] Test timezone conversion utilities
- [ ] Test API service layer
- [ ] Test hooks/composables
- [ ] Achieve >80% coverage
- [ ] Add tests to CI

## Acceptance Criteria
- All critical components tested
- >80% code coverage
- Tests pass in CI
- Tests run quickly (<30s)
- Well organized test files

## Priority
High

## Estimated Effort
5-7 days
"@

gh issue create --title "Create E2E tests for critical user flows" --label "frontend,enhancement,testing" --body @"
## Epic
#96 Testing & Quality Assurance

## Description
Implement end-to-end tests for main user journeys through the application.

## Tasks
- [ ] Set up Playwright/Cypress
- [ ] Test: Browse conference list
- [ ] Test: Search and filter
- [ ] Test: View conference detail
- [ ] Test: Export to calendar
- [ ] Test: Toggle AoE timezone
- [ ] Test: Mobile responsive flows
- [ ] Add to CI pipeline

## Acceptance Criteria
- All critical flows tested
- Tests pass consistently
- Run in CI on PRs
- Test on multiple browsers
- Mobile testing included

## Priority
High

## Estimated Effort
5-7 days
"@

gh issue create --title "Perform accessibility audit and fixes" --label "frontend,enhancement,testing" --body @"
## Epic
#96 Testing & Quality Assurance

## Description
Audit application for accessibility compliance (WCAG 2.1 AA) and fix issues.

## Tasks (PRD Non-Functional Requirements)
- [ ] Run axe-core accessibility scan
- [ ] Test with screen reader (NVDA/JAWS/VoiceOver)
- [ ] Test keyboard navigation
- [ ] Check color contrast ratios
- [ ] Add ARIA labels where needed
- [ ] Fix accessibility violations
- [ ] Add accessibility tests
- [ ] Document accessibility features

## Acceptance Criteria
- WCAG 2.1 AA compliant
- No axe violations
- Screen reader friendly
- Full keyboard navigation
- Proper focus management
- Color contrast meets standards

## Priority
High

## Estimated Effort
4-5 days
"@

gh issue create --title "Conduct cross-browser and device testing" --label "frontend,enhancement,testing" --body @"
## Epic
#96 Testing & Quality Assurance

## Description
Test application across multiple browsers and devices to ensure compatibility.

## Tasks (PRD Non-Functional Requirements)
- [ ] Test on Chrome (Windows, Mac, Android)
- [ ] Test on Firefox (Windows, Mac)
- [ ] Test on Safari (Mac, iOS)
- [ ] Test on Edge (Windows)
- [ ] Test on various screen sizes
- [ ] Test on tablets
- [ ] Document any browser-specific issues
- [ ] Fix critical compatibility issues

## Acceptance Criteria
- Works on Chrome, Firefox, Safari, Edge
- Mobile responsive on iOS and Android
- No critical browser bugs
- Graceful degradation on older browsers
- Documented compatibility matrix

## Priority
High

## Estimated Effort
3-4 days
"@

gh issue create --title "Performance testing and optimization" --label "frontend,enhancement,testing" --body @"
## Epic
#96 Testing & Quality Assurance

## Description
Audit and optimize frontend performance to meet PRD requirements.

## Tasks (PRD Non-Functional Requirements)
- [ ] Run Lighthouse audits
- [ ] Measure page load time (<3s target)
- [ ] Test with 500+ conferences
- [ ] Optimize bundle size (<500KB initial)
- [ ] Optimize images and assets
- [ ] Implement code splitting
- [ ] Test on slow 3G network
- [ ] Profile and fix performance bottlenecks

## Acceptance Criteria
- Lighthouse score >90
- Initial load <3 seconds
- Smooth scrolling with 500+ items
- Bundle size optimized
- Good performance on slow networks

## Priority
High

## Estimated Effort
4-5 days
"@

Write-Host "All frontend issues created successfully!" -ForegroundColor Green
