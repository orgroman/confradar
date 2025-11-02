"""Backfill series_id and year for existing conferences.

This script:
1. Seeds conference_series table with major series (NeurIPS, ACL, EMNLP, etc.)
2. Extracts year from conference keys where possible
3. Links conferences to series via series_id
4. Is idempotent and re-runnable without creating duplicates

Usage:
    python scripts/backfill_series_and_year.py [--dry-run]
"""

import argparse
import logging
import re
from typing import Optional

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from confradar.db.models import Conference, ConferenceSeries
from confradar.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Major conference series to seed
MAJOR_SERIES = [
    # Top-tier ML/AI conferences
    {"short_name": "NeurIPS", "name": "Conference on Neural Information Processing Systems"},
    {"short_name": "ICLR", "name": "International Conference on Learning Representations"},
    {"short_name": "ICML", "name": "International Conference on Machine Learning"},
    {"short_name": "AAAI", "name": "AAAI Conference on Artificial Intelligence"},
    
    # NLP conferences
    {"short_name": "ACL", "name": "Association for Computational Linguistics"},
    {"short_name": "EMNLP", "name": "Conference on Empirical Methods in Natural Language Processing"},
    {"short_name": "NAACL", "name": "North American Chapter of the Association for Computational Linguistics"},
    {"short_name": "EACL", "name": "European Chapter of the Association for Computational Linguistics"},
    {"short_name": "COLING", "name": "International Conference on Computational Linguistics"},
    {"short_name": "AACL", "name": "Asia-Pacific Chapter of the Association for Computational Linguistics"},
    {"short_name": "IJCNLP", "name": "International Joint Conference on Natural Language Processing"},
    
    # Computer vision
    {"short_name": "CVPR", "name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition"},
    {"short_name": "ICCV", "name": "IEEE International Conference on Computer Vision"},
    {"short_name": "ECCV", "name": "European Conference on Computer Vision"},
    
    # Data mining & IR
    {"short_name": "KDD", "name": "ACM SIGKDD Conference on Knowledge Discovery and Data Mining"},
    {"short_name": "WWW", "name": "The Web Conference"},
    {"short_name": "SIGIR", "name": "ACM SIGIR Conference on Research and Development in Information Retrieval"},
    {"short_name": "CIKM", "name": "ACM International Conference on Information and Knowledge Management"},
    {"short_name": "WSDM", "name": "ACM International Conference on Web Search and Data Mining"},
    {"short_name": "RecSys", "name": "ACM Conference on Recommender Systems"},
    
    # Workshops and shared tasks (recurring)
    {"short_name": "WMT", "name": "Conference on Machine Translation"},
    {"short_name": "CRAC", "name": "CRAC Shared Task on Multilingual Coreference Resolution"},
    {"short_name": "DISRPT", "name": "DISRPT Shared Task on Discourse Relation Parsing and Treebanking"},
    {"short_name": "NLLP", "name": "Workshop on Natural Legal Language Processing"},
]


def extract_year_from_key(key: str) -> Optional[int]:
    """Extract year from conference key.
    
    Patterns:
    - emnlp25 -> 2025
    - 202525, 202626 -> 2025, 2026 (first 4 digits)
    - neurips -> None (no year in key)
    
    Args:
        key: Conference key
        
    Returns:
        Extracted year or None
    """
    # Pattern 1: Key ending with 2-digit year (e.g., emnlp25, nlp26)
    match = re.search(r'(\d{2})$', key)
    if match:
        year_suffix = int(match.group(1))
        # Assume 20XX for years 20-35, 19XX otherwise (though unlikely)
        if 20 <= year_suffix <= 35:
            return 2000 + year_suffix
        elif year_suffix < 20:
            return 2000 + year_suffix
    
    # Pattern 2: Key starting with 4-digit year (e.g., 202525)
    match = re.search(r'^(\d{4})', key)
    if match:
        year = int(match.group(1))
        if 2020 <= year <= 2035:
            return year
    
    # Pattern 3: Year embedded in key (e.g., wmt2025)
    match = re.search(r'(\d{4})', key)
    if match:
        year = int(match.group(1))
        if 2020 <= year <= 2035:
            return year
    
    return None


def extract_series_acronym_from_key(key: str) -> Optional[str]:
    """Extract series acronym from conference key.
    
    Patterns:
    - emnlp, emnlp25 -> EMNLP
    - neurips -> NeurIPS
    - acl -> ACL
    - wmt2525 -> WMT (extract before year)
    - 202525, 1225 -> None (no clear acronym)
    
    Args:
        key: Conference key
        
    Returns:
        Extracted acronym or None
    """
    # Pattern 1: Extract acronym before 4-digit year (e.g., wmt2525 -> wmt)
    match = re.search(r'^([a-z]+)\d{4}', key, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Pattern 2: Remove 2-digit year suffix (e.g., emnlp25 -> emnlp)
    base_key = re.sub(r'\d{2}$', '', key)
    
    # Skip pure numeric keys
    if base_key.isdigit() or not base_key:
        return None
    
    # Return uppercase version as acronym
    return base_key.upper()


def seed_conference_series(session: Session, dry_run: bool = False) -> dict[str, int]:
    """Seed conference_series table with major series.
    
    Args:
        session: Database session
        dry_run: If True, don't commit changes
        
    Returns:
        Mapping of series short_name to series_id
    """
    logger.info(f"Seeding {len(MAJOR_SERIES)} major conference series...")
    
    series_map = {}
    
    for series_data in MAJOR_SERIES:
        # Check if series already exists
        existing = session.execute(
            select(ConferenceSeries).where(
                ConferenceSeries.short_name == series_data["short_name"]
            )
        ).scalar_one_or_none()
        
        if existing:
            logger.info(f"Series '{series_data['short_name']}' already exists (id={existing.id})")
            series_map[series_data["short_name"]] = existing.id
        else:
            series = ConferenceSeries(**series_data)
            session.add(series)
            if not dry_run:
                session.flush()  # Get the ID
            logger.info(f"Created series '{series_data['short_name']}' (id={series.id if not dry_run else 'pending'})")
            series_map[series_data["short_name"]] = series.id if not dry_run else -1
    
    if not dry_run:
        session.commit()
    else:
        logger.info("DRY RUN: Not committing series changes")
    
    return series_map


def backfill_conferences(session: Session, series_map: dict[str, int], dry_run: bool = False) -> dict:
    """Backfill series_id and year for existing conferences.
    
    Args:
        session: Database session
        series_map: Mapping of series short_name to series_id
        dry_run: If True, don't commit changes
        
    Returns:
        Statistics about backfill coverage
    """
    logger.info("Backfilling conferences...")
    
    conferences = session.execute(select(Conference)).scalars().all()
    
    stats = {
        "total": len(conferences),
        "year_backfilled": 0,
        "series_backfilled": 0,
        "year_skipped": 0,
        "series_skipped": 0,
    }
    
    for conf in conferences:
        updated = False
        
        # Backfill year if missing
        if conf.year is None:
            year = extract_year_from_key(conf.key)
            if year:
                conf.year = year
                stats["year_backfilled"] += 1
                updated = True
                logger.info(f"Conference '{conf.key}': Set year={year}")
            else:
                stats["year_skipped"] += 1
                logger.debug(f"Conference '{conf.key}': Could not extract year")
        
        # Backfill series_id if missing
        if conf.series_id is None:
            acronym = extract_series_acronym_from_key(conf.key)
            if acronym and acronym in series_map:
                conf.series_id = series_map[acronym]
                stats["series_backfilled"] += 1
                updated = True
                logger.info(f"Conference '{conf.key}': Set series_id={series_map[acronym]} ({acronym})")
            else:
                stats["series_skipped"] += 1
                logger.debug(f"Conference '{conf.key}': Could not match series (acronym={acronym})")
        
        if updated and not dry_run:
            session.add(conf)
    
    if not dry_run:
        session.commit()
        logger.info("Changes committed to database")
    else:
        logger.info("DRY RUN: Not committing conference changes")
    
    return stats


def print_stats(stats: dict):
    """Print backfill statistics."""
    logger.info("\n=== Backfill Statistics ===")
    logger.info(f"Total conferences: {stats['total']}")
    logger.info(f"Year backfilled: {stats['year_backfilled']}")
    logger.info(f"Year skipped: {stats['year_skipped']}")
    logger.info(f"Series backfilled: {stats['series_backfilled']}")
    logger.info(f"Series skipped: {stats['series_skipped']}")
    
    year_coverage = (stats['year_backfilled'] / stats['total'] * 100) if stats['total'] > 0 else 0
    series_coverage = (stats['series_backfilled'] / stats['total'] * 100) if stats['total'] > 0 else 0
    
    logger.info(f"\nYear coverage: {year_coverage:.1f}%")
    logger.info(f"Series coverage: {series_coverage:.1f}%")
    
    if year_coverage < 90 or series_coverage < 90:
        logger.warning("⚠️  Coverage below 90% target")
    else:
        logger.info("✅ Coverage target met (>=90%)")


def main():
    parser = argparse.ArgumentParser(description="Backfill series_id and year for conferences")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without committing")
    args = parser.parse_args()
    
    logger.info("Starting backfill process...")
    if args.dry_run:
        logger.info("DRY RUN MODE: No changes will be committed")
    
    # Create engine and session
    db_url = settings.database_url
    engine = create_engine(db_url)
    
    with Session(engine) as session:
        # Step 1: Seed conference series
        series_map = seed_conference_series(session, dry_run=args.dry_run)
        
        # Step 2: Backfill conferences
        stats = backfill_conferences(session, series_map, dry_run=args.dry_run)
        
        # Step 3: Print statistics
        print_stats(stats)
    
    logger.info("Backfill process complete!")


if __name__ == "__main__":
    main()
