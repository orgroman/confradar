import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useTheme } from '@/components/theme-provider'
import { Moon, Sun } from 'lucide-react'

function App() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="container mx-auto p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-4xl font-bold">ConfRadar UI</h1>
        <Button
          variant="outline"
          size="icon"
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
        >
          {theme === "light" ? (
            <Moon className="h-5 w-5" />
          ) : (
            <Sun className="h-5 w-5" />
          )}
          <span className="sr-only">Toggle theme</span>
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Conference Tracking</CardTitle>
            <CardDescription>
              Monitor deadlines and updates for academic conferences
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Stay up to date with the latest conference deadlines, CFP
              announcements, and important dates.
            </p>
          </CardContent>
          <CardFooter>
            <Button className="w-full">View Conferences</Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Automated Extraction</CardTitle>
            <CardDescription>
              AI-powered information gathering
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Automatically extract key dates and information from conference
              websites using LLM technology.
            </p>
          </CardContent>
          <CardFooter>
            <Button variant="secondary" className="w-full">
              Configure
            </Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Change Detection</CardTitle>
            <CardDescription>
              Get notified of deadline changes
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Receive alerts when conference deadlines are extended or changed
              so you never miss an opportunity.
            </p>
          </CardContent>
          <CardFooter>
            <Button variant="outline" className="w-full">
              Setup Alerts
            </Button>
          </CardFooter>
        </Card>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Button Variants</h2>
        <div className="flex flex-wrap gap-4">
          <Button>Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
          <Button variant="destructive">Destructive</Button>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Button Sizes</h2>
        <div className="flex flex-wrap items-center gap-4">
          <Button size="sm">Small</Button>
          <Button size="default">Default</Button>
          <Button size="lg">Large</Button>
          <Button size="icon">
            <Sun className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Design Tokens</CardTitle>
          <CardDescription>
            Colors, spacing, and typography configured
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-medium mb-2">Primary Colors</h3>
            <div className="flex gap-2">
              {[50, 100, 200, 300, 400, 500, 600, 700, 800, 900].map(
                (shade) => (
                  <div
                    key={shade}
                    className={`w-8 h-8 rounded bg-primary-${shade}`}
                    title={`primary-${shade}`}
                  />
                )
              )}
            </div>
          </div>
          <div>
            <h3 className="font-medium mb-2">Responsive Breakpoints</h3>
            <p className="text-sm text-muted-foreground">
              xs: 475px, sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl:
              1536px
            </p>
          </div>
          <div>
            <h3 className="font-medium mb-2">Typography</h3>
            <p className="text-sm text-muted-foreground font-sans">
              Font Family: Inter, system-ui
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default App

