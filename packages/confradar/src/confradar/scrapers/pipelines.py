"""Scrapy pipelines for processing conference items."""

from typing import Any


class ValidationPipeline:
    """Validate conference items have required fields."""

    def process_item(self, item: dict, spider: Any) -> dict:
        """Validate item has required fields."""
        required = ["key", "name"]
        for field in required:
            if not item.get(field):
                raise ValueError(f"Missing required field: {field}")

        if "deadlines" not in item:
            item["deadlines"] = []

        return item


class DeduplicationPipeline:
    """Remove duplicate conferences within a scraping session."""

    def __init__(self):
        self.seen_keys = set()

    def open_spider(self, spider: Any) -> None:
        """Reset seen keys at start of spider."""
        self.seen_keys = set()

    def process_item(self, item: dict, spider: Any) -> dict:
        """Drop item if we've seen this conference key already."""
        key = item.get("key")
        if key in self.seen_keys:
            raise ValueError(f"Duplicate conference key: {key}")

        self.seen_keys.add(key)
        return item


class DatabasePipeline:
    """Store conferences in PostgreSQL database."""

    def __init__(self):
        self.session = None

    def open_spider(self, spider: Any) -> None:
        """Connect to database."""
        from confradar.db.base import get_session

        self.session = get_session()

    def close_spider(self, spider: Any) -> None:
        """Close database connection."""
        if self.session:
            self.session.close()

    def process_item(self, item: dict, spider: Any) -> dict:
        """Save conference to database.

        Creates or updates:
        - Conference record
        - Source record (linking to scraper source)
        - Deadline records (one for each deadline)
        """
        from sqlalchemy.exc import IntegrityError

        from confradar.db.models import Conference, Deadline, Source

        if not self.session:
            raise RuntimeError("Database session not initialized")

        try:
            # Find or create conference
            conference = (
                self.session.query(Conference)
                .filter_by(key=item["key"]) 
                .first()
            )

            if not conference:
                conference = Conference(
                    key=item["key"], name=item["name"], homepage=item.get("homepage")
                )
                self.session.add(conference)
                self.session.flush()  # Get the ID
            else:
                # Update existing conference
                conference.name = item["name"]
                if item.get("homepage"):
                    conference.homepage = item.get("homepage")

            # Create or update source
            source_url = item.get("url", "")
            source = (
                self.session.query(Source)
                .filter_by(conference_id=conference.id, url=source_url)
                .first()
            )

            if not source:
                source = Source(
                    conference_id=conference.id,
                    url=source_url,
                    notes=(
                        "Scraped by "
                        f"{item.get('source', 'unknown')} "
                        "on "
                        f"{item.get('scraped_at', '')}"
                    ),
                )
                self.session.add(source)
                self.session.flush()

            # Process deadlines
            for deadline_data in item.get("deadlines", []):
                # Parse due_date (could be date object, datetime object, or ISO string)
                from datetime import date, datetime

                # Handle both due_at and due_date keys (for compatibility)
                due_value = deadline_data.get("due_date") or deadline_data.get("due_at")
                
                if not due_value:
                    # Skip deadlines without dates
                    spider.logger.debug(f"Skipping deadline without date for {item['key']}")
                    continue

                # Convert to date object
                if isinstance(due_value, str):
                    try:
                        # Try parsing as ISO format datetime first
                        due_date_obj = datetime.fromisoformat(due_value).date()
                    except ValueError:
                        try:
                            # Try parsing as date string
                            due_date_obj = date.fromisoformat(due_value)
                        except ValueError:
                            # Skip invalid dates
                            spider.logger.warning(f"Invalid date format: {due_value}")
                            continue
                elif isinstance(due_value, datetime):
                    due_date_obj = due_value.date()
                elif isinstance(due_value, date):
                    due_date_obj = due_value
                else:
                    spider.logger.warning(f"Unknown date type: {type(due_value)}")
                    continue

                # Check if deadline already exists
                existing_deadline = (
                    self.session.query(Deadline)
                    .filter_by(
                        conference_id=conference.id,
                        kind=deadline_data.get("kind", "submission"),
                        due_date=due_date_obj,
                    )
                    .first()
                )

                if not existing_deadline:
                    deadline = Deadline(
                        conference_id=conference.id,
                        kind=deadline_data.get("kind", "submission"),
                        due_date=due_date_obj,
                        timezone=deadline_data.get("timezone"),
                        source_id=source.id,
                    )
                    self.session.add(deadline)

            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()
            spider.logger.warning(f"Database integrity error for {item['key']}: {e}")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Database error for {item['key']}: {e}")
            raise

        return item
