"""Dagster assets for storing conference data in the database.

These assets take scraped conference data and persist it to the database
using SQLAlchemy models.
"""
from typing import List, Dict, Any
from datetime import datetime, timezone

from dagster import asset, Output, MetadataValue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from confradar.db.base import Base
from confradar.db.models import Conference, Source
from confradar.settings import get_settings


@asset(
    description="Store all scraped conferences in the database",
    group_name="storage",
)
def store_conferences(
    ai_deadlines_conferences: List[Dict[str, Any]],
    acl_web_conferences: List[Dict[str, Any]],
    chairing_tool_conferences: List[Dict[str, Any]],
    elra_conferences: List[Dict[str, Any]],
    wikicfp_conferences: List[Dict[str, Any]],
) -> Output[Dict[str, int]]:
    """Store all scraped conferences in the database.
    
    Merges conferences from all sources and stores them in the database.
    Uses upsert logic to update existing conferences or insert new ones.
    
    Returns:
        Dictionary with statistics about stored conferences
    """
    settings = get_settings()
    
    # Create database engine and session
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Combine all conferences
        all_conferences = []
        source_counts = {}
        
        for source_name, conferences in [
            ("aideadlines", ai_deadlines_conferences),
            ("acl_web", acl_web_conferences),
            ("chairing_tool", chairing_tool_conferences),
            ("elra", elra_conferences),
            ("wikicfp", wikicfp_conferences),
        ]:
            all_conferences.extend(conferences)
            source_counts[source_name] = len(conferences)
        
        # Track stats
        new_count = 0
        updated_count = 0
        
        for conf_data in all_conferences:
            # Check if conference exists
            existing = session.query(Conference).filter_by(
                key=conf_data["key"]
            ).first()
            
            if existing:
                # Update existing conference
                existing.name = conf_data["name"]
                existing.homepage = conf_data.get("homepage")
                updated_count += 1
                
                # Check if we need to add a new source URL
                source_url = conf_data.get("url")
                if source_url:
                    source_exists = session.query(Source).filter_by(
                        conference_id=existing.id,
                        url=source_url
                    ).first()
                    
                    if not source_exists:
                        source = Source(
                            conference_id=existing.id,
                            url=source_url,
                            notes=f"Scraped from {conf_data['source']}"
                        )
                        session.add(source)
            else:
                # Create new conference
                conference = Conference(
                    key=conf_data["key"],
                    name=conf_data["name"],
                    homepage=conf_data.get("homepage"),
                )
                session.add(conference)
                session.flush()  # Get the ID
                
                # Add source URL
                if conf_data.get("url"):
                    source = Source(
                        conference_id=conference.id,
                        url=conf_data["url"],
                        notes=f"Scraped from {conf_data['source']}"
                    )
                    session.add(source)
                
                new_count += 1
        
        # Commit all changes
        session.commit()
        
        stats = {
            "total_scraped": len(all_conferences),
            "new_conferences": new_count,
            "updated_conferences": updated_count,
            **{f"{k}_count": v for k, v in source_counts.items()},
        }
        
        return Output(
            value=stats,
            metadata={
                "total": len(all_conferences),
                "new": new_count,
                "updated": updated_count,
                "breakdown": MetadataValue.md(
                    "\n".join([f"- **{k}**: {v}" for k, v in source_counts.items()])
                ),
            },
        )
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
