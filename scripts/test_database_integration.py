"""Test database integration with a few sample conferences."""
from confradar.db.base import session_scope
from confradar.db.models import Conference, Source, Deadline
from datetime import datetime

# Clear test data first
print("Cleaning test data...")
with session_scope() as session:
    # Delete test conferences
    test_keys = ['test_icml25', 'test_neurips25']
    for key in test_keys:
        conf = session.query(Conference).filter_by(key=key).first()
        if conf:
            session.delete(conf)
    session.commit()

# Test creating conferences
print("\nCreating test conferences...")
with session_scope() as session:
    # Conference 1
    conf1 = Conference(
        key='test_icml25',
        name='ICML 2025 (Test)',
        homepage='https://icml.cc'
    )
    session.add(conf1)
    session.flush()
    
    # Add source
    source1 = Source(
        conference_id=conf1.id,
        url='https://aideadlines.org',
        notes='Test scrape'
    )
    session.add(source1)
    session.flush()
    
    # Add deadline
    deadline1 = Deadline(
        conference_id=conf1.id,
        kind='submission',
        due_date=datetime(2025, 2, 1, 23, 59, 59),
        timezone='UTC-12',
        source_id=source1.id
    )
    session.add(deadline1)
    
    print(f"Created conference: {conf1.key} (ID: {conf1.id})")

# Read back
print("\nReading conferences from database...")
with session_scope() as session:
    conferences = session.query(Conference).filter(
        Conference.key.in_(['test_icml25', 'test_neurips25'])
    ).all()
    
    for conf in conferences:
        print(f"\nConference: {conf.name} ({conf.key})")
        print(f"  ID: {conf.id}")
        print(f"  Homepage: {conf.homepage}")
        print(f"  Created: {conf.created_at}")
        
        # Get sources
        for source in conf.sources:
            print(f"  Source: {source.url}")
        
        # Get deadlines
        for deadline in conf.deadlines:
            print(f"  Deadline ({deadline.kind}): {deadline.due_date} [{deadline.timezone}]")

print("\n✓ Database integration test passed!")
