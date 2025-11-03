"""add event date ordering constraint

Revision ID: c1a2b3c4d5e6
Revises: b2a3c4d5e6f7
Create Date: 2025-11-02 21:08:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c1a2b3c4d5e6'
down_revision = 'b2a3c4d5e6f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Preflight check: verify no existing rows violate the constraint
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT COUNT(*) 
            FROM conferences 
            WHERE event_start_date IS NOT NULL 
              AND event_end_date IS NOT NULL 
              AND event_end_date < event_start_date
        """)
    )
    invalid_count = result.scalar()
    
    if invalid_count > 0:
        raise ValueError(
            f"Cannot add constraint: {invalid_count} conference(s) have "
            f"event_end_date < event_start_date. Please fix these rows first:\n"
            f"  SELECT id, key, event_start_date, event_end_date FROM conferences\n"
            f"  WHERE event_start_date IS NOT NULL AND event_end_date IS NOT NULL\n"
            f"    AND event_end_date < event_start_date;"
        )
    
    # Add check constraint to ensure event_end_date >= event_start_date when both are not null
    op.create_check_constraint(
        'ck_conference_event_date_order',
        'conferences',
        'event_start_date IS NULL OR event_end_date IS NULL OR event_end_date >= event_start_date'
    )


def downgrade() -> None:
    # Drop the check constraint
    op.drop_constraint('ck_conference_event_date_order', 'conferences', type_='check')
