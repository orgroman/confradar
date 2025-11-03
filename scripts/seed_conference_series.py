"""Seed major conference series with canonical names and homepages.

This script seeds the conference_series table with well-known academic conference series
in machine learning, NLP, and related fields. It is idempotent and safe to run multiple times.

Usage:
    python scripts/seed_conference_series.py [--dry-run]

The script can be run standalone or imported as a module for use in other scripts.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from confradar.data import MAJOR_SERIES
from confradar.db import ConferenceSeries
from confradar.db.base import get_engine


def seed_conference_series(session: Session, dry_run: bool = False) -> dict[str, int]:
    """Seed conference_series table with major series.
    
    This function is idempotent - it will skip series that already exist.
    
    Args:
        session: SQLAlchemy session
        dry_run: If True, only print what would be done without modifying the database
        
    Returns:
        Dictionary mapping short_name to series id
        
    Raises:
        Exception: If database operation fails
    """
    series_map = {}
    created_count = 0
    skipped_count = 0
    
    try:
        for short_name, name, homepage in MAJOR_SERIES:
            # Check if series already exists
            existing = session.execute(
                select(ConferenceSeries).where(ConferenceSeries.short_name == short_name)
            ).scalar_one_or_none()
            
            if existing:
                series_map[short_name] = existing.id
                print(f"✓ Series already exists: {short_name} (id={existing.id})")
                skipped_count += 1
            else:
                if dry_run:
                    print(f"[DRY RUN] Would create series: {short_name} - {name}")
                    print(f"           Homepage: {homepage}")
                    series_map[short_name] = -1  # Placeholder for dry run
                    created_count += 1
                else:
                    series = ConferenceSeries(
                        short_name=short_name,
                        name=name,
                        homepage=homepage
                    )
                    session.add(series)
                    session.flush()  # Get the ID
                    series_map[short_name] = series.id
                    print(f"✓ Created series: {short_name} (id={series.id})")
                    created_count += 1
        
        if not dry_run:
            session.commit()
            
    except Exception as e:
        if not dry_run:
            session.rollback()
        raise RuntimeError(f"Failed to seed conference series: {e}") from e
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Total series in seed list: {len(MAJOR_SERIES)}")
    print(f"  Series created: {created_count}")
    print(f"  Series already existed: {skipped_count}")
    
    return series_map


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Seed major conference series into the database"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying the database"
    )
    args = parser.parse_args()
    
    try:
        engine = get_engine()
        
        with Session(engine) as session:
            print("Seeding conference_series table with major conferences...")
            seed_conference_series(session, dry_run=args.dry_run)
        
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}✓ Seeding complete!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
