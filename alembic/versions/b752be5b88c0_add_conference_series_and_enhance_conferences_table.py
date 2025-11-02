"""add conference series and enhance conferences table

Revision ID: b752be5b88c0
Revises: 6734aa7c5266
Create Date: 2025-02-11 14:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b752be5b88c0'
down_revision = '6734aa7c5266'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conference_series table
    op.create_table(
        'conference_series',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('short_name', sa.String(length=64), nullable=False),
        sa.Column('homepage', sa.String(length=512), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_name', name='uq_series_short_name')
    )
    op.create_index('ix_series_name', 'conference_series', ['name'], unique=False)
    
    # Add new columns to conferences table
    op.add_column('conferences', sa.Column('series_id', sa.Integer(), nullable=True))
    op.add_column('conferences', sa.Column('year', sa.Integer(), nullable=True))
    op.add_column('conferences', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('conferences', sa.Column('event_start_date', sa.Date(), nullable=True))
    op.add_column('conferences', sa.Column('event_end_date', sa.Date(), nullable=True))
    op.add_column('conferences', sa.Column('submission_url', sa.String(length=512), nullable=True))
    op.add_column('conferences', sa.Column('notes', sa.Text(), nullable=True))
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_conference_series',
        'conferences', 'conference_series',
        ['series_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # Create indexes
    op.create_index('ix_conference_year', 'conferences', ['year'], unique=False)
    op.create_index('ix_conference_series', 'conferences', ['series_id'], unique=False)
    op.create_index('ix_conference_dates', 'conferences', ['event_start_date', 'event_end_date'], unique=False)
    
    # Add check constraint for year
    op.create_check_constraint(
        'ck_conference_year',
        'conferences',
        'year IS NULL OR (year >= 2020 AND year <= 2035)'
    )


def downgrade() -> None:
    # Drop constraints and indexes from conferences
    op.drop_constraint('ck_conference_year', 'conferences', type_='check')
    op.drop_index('ix_conference_dates', table_name='conferences')
    op.drop_index('ix_conference_series', table_name='conferences')
    op.drop_index('ix_conference_year', table_name='conferences')
    op.drop_constraint('fk_conference_series', 'conferences', type_='foreignkey')
    
    # Drop new columns from conferences
    op.drop_column('conferences', 'notes')
    op.drop_column('conferences', 'submission_url')
    op.drop_column('conferences', 'event_end_date')
    op.drop_column('conferences', 'event_start_date')
    op.drop_column('conferences', 'location')
    op.drop_column('conferences', 'year')
    op.drop_column('conferences', 'series_id')
    
    # Drop conference_series table
    op.drop_index('ix_series_name', table_name='conference_series')
    op.drop_table('conference_series')
