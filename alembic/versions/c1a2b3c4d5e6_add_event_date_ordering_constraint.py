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
    # Add check constraint to ensure event_end_date >= event_start_date when both are not null
    op.create_check_constraint(
        'ck_conference_event_date_order',
        'conferences',
        'event_start_date IS NULL OR event_end_date IS NULL OR event_end_date >= event_start_date'
    )


def downgrade() -> None:
    # Drop the check constraint
    op.drop_constraint('ck_conference_event_date_order', 'conferences', type_='check')
