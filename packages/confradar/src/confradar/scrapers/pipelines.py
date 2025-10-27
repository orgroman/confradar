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
            conference = self.session.query(Conference).filter_by(key=item["key"]).first()

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
                    notes=f"Scraped by {item.get('source', 'unknown')} on {item.get('scraped_at', '')}",
                )
                self.session.add(source)
                self.session.flush()

            # Process deadlines
            for deadline_data in item.get("deadlines", []):
                # Parse due_at (ISO format string to datetime)
                from datetime import datetime

                if isinstance(deadline_data.get("due_at"), str):
                    try:
                        due_date = datetime.fromisoformat(deadline_data["due_at"])
                    except ValueError:
                        # Skip invalid dates
                        continue
                else:
                    due_date = deadline_data.get("due_at")

                # Check if deadline already exists
                existing_deadline = (
                    self.session.query(Deadline)
                    .filter_by(
                        conference_id=conference.id,
                        kind=deadline_data.get("kind", "submission"),
                        due_date=due_date,
                    )
                    .first()
                )

                if not existing_deadline:
                    deadline = Deadline(
                        conference_id=conference.id,
                        kind=deadline_data.get("kind", "submission"),
                        due_date=due_date,
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
