"""Backfill series_id and year fields for existing conferences.

This script:
1. Seeds the conference_series table with major known series
2. Extracts year and series acronym from conference keys
3. Updates conferences with matched series_id and year

Idempotent: Safe to run multiple times - only updates NULL fields.
"""

from __future__ import annotations

import argparse
import re
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from confradar.db import Conference, ConferenceSeries, get_engine


# Major conference series we want to track
MAJOR_SERIES = [
    ("NeurIPS", "Conference on Neural Information Processing Systems"),
    ("ICLR", "International Conference on Learning Representations"),
    ("ICML", "International Conference on Machine Learning"),
    ("AAAI", "AAAI Conference on Artificial Intelligence"),
    ("ACL", "Annual Meeting of the Association for Computational Linguistics"),
    ("EMNLP", "Conference on Empirical Methods in Natural Language Processing"),
    ("NAACL", "North American Chapter of the Association for Computational Linguistics"),
    ("EACL", "European Chapter of the Association for Computational Linguistics"),
    ("COLING", "International Conference on Computational Linguistics"),
    ("CVPR", "IEEE/CVF Conference on Computer Vision and Pattern Recognition"),
    ("ICCV", "IEEE/CVF International Conference on Computer Vision"),
    ("ECCV", "European Conference on Computer Vision"),
    ("ICRA", "IEEE International Conference on Robotics and Automation"),
    ("RSS", "Robotics: Science and Systems"),
    ("CoRL", "Conference on Robot Learning"),
    ("KDD", "ACM SIGKDD Conference on Knowledge Discovery and Data Mining"),
    ("WWW", "The Web Conference"),
    ("SIGIR", "ACM SIGIR Conference on Research and Development in Information Retrieval"),
    ("WSDM", "ACM International Conference on Web Search and Data Mining"),
    ("WMT", "Conference on Machine Translation"),
    ("CRAC", "Workshop on Computational Models of Reference, Anaphora and Coreference"),
    ("DISRPT", "Discourse Relation Parsing and Treebanking"),
    ("NLLP", "Natural Legal Language Processing Workshop"),
    ("NLRSE", "Natural Language Reasoning and Structured Explanations Workshop"),
]


def extract_year_from_key(key: str) -> Optional[int]:
    """Extract conference year from key.
    
    Examples:
        emnlp25 -> 2025
        neurips2024 -> 2024
        wmt2525 -> 2025 (handles duplicated digits)
        202525 -> 2025
    """
    # Find all 4-digit year matches
    four_digit_years = re.findall(r'20(\d{2})', key)
    if four_digit_years:
        # Prefer the last 4-digit year found
        return int(f"20{four_digit_years[-1]}")
    
    # Check for 2-digit year at the end, possibly duplicated (e.g., "2525")
    match = re.search(r'(\d{2})$', key)
    if match:
        year_suffix = int(match.group(1))
        # Check if the last four digits are a repeated two-digit sequence
        if len(key) >= 4 and key[-4:] == key[-2:] * 2:
            # Use the two-digit year from the repeated sequence
            # Assume 20xx for years 20-35 to match database constraint (2020-2035)
            if 20 <= year_suffix <= 35:
                return 2000 + year_suffix
        else:
            # Use the two-digit year if within database constraint range
            if 20 <= year_suffix <= 35:
                return 2000 + year_suffix
    
    return None


def extract_series_acronym_from_key(key: str) -> Optional[str]:
    """Extract series acronym from key.
    
    Examples:
        emnlp25 -> emnlp
        neurips2024 -> neurips
        wmt2525 -> wmt
    """
    # Remove year suffix (2 or 4 digits, possibly duplicated)
    clean_key = re.sub(r'20\d{2}$', '', key)  # Remove 4-digit year
    clean_key = re.sub(r'\d{2}(?:\d{2})?$', '', clean_key)  # Remove 2-digit year (possibly duplicated)
    
    if clean_key:
        return clean_key.lower()
    return None


def seed_conference_series(session: Session, dry_run: bool = False) -> dict[str, int]:
    """Seed conference_series table with major series.
    
    Returns dict mapping short_name to id.
    """
    series_map = {}
    
    for short_name, name in MAJOR_SERIES:
        # Check if series already exists
        existing = session.execute(
            select(ConferenceSeries).where(ConferenceSeries.short_name == short_name)
        ).scalar_one_or_none()
        
        if existing:
            series_map[short_name.lower()] = existing.id
            print(f"✓ Series already exists: {short_name} (id={existing.id})")
        else:
            if dry_run:
                print(f"[DRY RUN] Would create series: {short_name} - {name}")
                series_map[short_name.lower()] = -1  # Placeholder for dry run
            else:
                series = ConferenceSeries(short_name=short_name, name=name)
                session.add(series)
                session.flush()  # Get the ID
                series_map[short_name.lower()] = series.id
                print(f"✓ Created series: {short_name} (id={series.id})")
    
    if not dry_run:
        session.commit()
    
    return series_map


def backfill_conferences(session: Session, series_map: dict[str, int], dry_run: bool = False):
    """Backfill series_id and year for existing conferences."""
    conferences = session.execute(select(Conference)).scalars().all()
    
    updated_count = 0
    year_updated = 0
    series_updated = 0
    
    for conf in conferences:
        updated = False
        
        # Extract and set year if missing
        if conf.year is None:
            year = extract_year_from_key(conf.key)
            if year:
                if dry_run:
                    print(f"[DRY RUN] Would set year={year} for {conf.key}")
                else:
                    conf.year = year
                    print(f"✓ Set year={year} for {conf.key}")
                year_updated += 1
                updated = True
        
        # Extract and set series_id if missing
        if conf.series_id is None:
            acronym = extract_series_acronym_from_key(conf.key)
            if acronym and acronym in series_map:
                if dry_run:
                    print(f"[DRY RUN] Would set series_id={series_map[acronym]} ({acronym.upper()}) for {conf.key}")
                else:
                    conf.series_id = series_map[acronym]
                    print(f"✓ Set series_id={series_map[acronym]} ({acronym.upper()}) for {conf.key}")
                series_updated += 1
                updated = True
        
        if updated:
            updated_count += 1
    
    if not dry_run:
        session.commit()
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Total conferences: {len(conferences)}")
    print(f"  Conferences updated: {updated_count}")
    print(f"  Year fields set: {year_updated}")
    print(f"  Series fields set: {series_updated}")
    
    # Coverage stats
    total_with_year = sum(1 for c in conferences if c.year is not None or extract_year_from_key(c.key) is not None)
    
    total_with_series = 0
    for c in conferences:
        if c.series_id is not None:
            total_with_series += 1
        else:
            acronym = extract_series_acronym_from_key(c.key)
            if acronym and acronym in series_map:
                total_with_series += 1
    
    print(f"\nCoverage after backfill:")
    print(f"  Conferences with year: {total_with_year}/{len(conferences)} ({100*total_with_year/len(conferences):.1f}%)")
    print(f"  Conferences with series: {total_with_series}/{len(conferences)} ({100*total_with_series/len(conferences):.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="Backfill series_id and year for conferences")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without modifying DB")
    args = parser.parse_args()
    
    engine = get_engine()
    
    with Session(engine) as session:
        print("Step 1: Seeding conference_series table...")
        series_map = seed_conference_series(session, dry_run=args.dry_run)
        
        print(f"\nStep 2: Backfilling conferences...")
        backfill_conferences(session, series_map, dry_run=args.dry_run)
    
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}✓ Backfill complete!")


if __name__ == "__main__":
    main()
