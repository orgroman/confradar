"""Quick script to inspect ChairingTool HTML structure for deadline extraction."""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "confradar" / "src"))

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response


class InspectSpider(Spider):
    """Spider to inspect ChairingTool HTML."""

    name = "inspect"
    start_urls = ["https://chairingtool.com/conferences"]
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response: Response):
        """Parse and print structure."""
        print("\n" + "=" * 80)
        print("CHAIRING TOOL HTML STRUCTURE INSPECTION")
        print("=" * 80)
        
        # Try different selectors for conference containers
        selectors_to_try = [
            ".conference-card",
            ".conference-item",
            "tr.conference",
            ".event-card",
            ".conf-card",
            "article",
            ".card",
            "[class*='conference']",
            "[class*='event']",
        ]
        
        print("\n1. Testing conference container selectors:")
        for selector in selectors_to_try:
            matches = response.css(selector)
            if matches:
                print(f"   ✓ Found {len(matches)} elements with: {selector}")
        
        # Get the actual HTML structure
        print("\n2. Page body classes:")
        body_classes = response.css("body::attr(class)").get()
        print(f"   {body_classes}")
        
        print("\n3. Main container structure:")
        main_containers = response.css("main, #main, .main, .container, #content, .content")
        for i, container in enumerate(main_containers[:3]):
            classes = container.css("::attr(class)").get()
            print(f"   Container {i+1}: {container.root.tag} class='{classes}'")
        
        print("\n4. First 5 conference entries (if found):")
        # Try to find any conference-related elements
        conferences = response.css("[class*='conf'], [class*='event']")[:5]
        for i, conf in enumerate(conferences):
            print(f"\n   Entry {i+1}:")
            # Print element structure
            tag = conf.root.tag
            classes = conf.css("::attr(class)").get()
            print(f"      Tag: {tag}, Classes: {classes}")
            
            # Try to find title/name
            title = conf.css("h1::text, h2::text, h3::text, h4::text, .title::text, .name::text").get()
            if title:
                print(f"      Title: {title.strip()}")
            
            # Try to find dates/deadlines
            date_elements = conf.css(
                ".date, .deadline, .dates, [class*='date'], [class*='deadline']"
            )
            if date_elements:
                print(f"      Date elements found: {len(date_elements)}")
                for j, date_el in enumerate(date_elements[:3]):
                    text = date_el.css("::text").get()
                    classes = date_el.css("::attr(class)").get()
                    if text:
                        print(f"         {j+1}. class='{classes}': {text.strip()}")
        
        print("\n5. Looking for JavaScript with deadline data:")
        scripts = response.css("script:not([src])::text").getall()
        for i, script in enumerate(scripts):
            if "deadline" in script.lower() or "date" in script.lower() or "moment" in script.lower():
                print(f"\n   Script block {i+1} (first 500 chars):")
                print(f"   {script[:500]}")
        
        print("\n6. Sample HTML (first 2000 chars of body):")
        body_html = response.css("body").get()
        if body_html:
            print(body_html[:2000])
        
        print("\n" + "=" * 80)
        print("INSPECTION COMPLETE")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(InspectSpider)
    process.start()
