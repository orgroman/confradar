"""empty migration to linearize heads after b752be5b88c0

This revision intentionally does nothing. A prior migration (b752be5b88c0)
already introduced conference_series and enhanced conferences. We chain this
revision to that head to resolve multiple-head state.

Revision ID: b2a3c4d5e6f7
Revises: b752be5b88c0
Create Date: 2025-11-02 00:00:00.000000+00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2a3c4d5e6f7'
down_revision = 'b752be5b88c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # No-op: schema already updated by b752be5b88c0
    pass


def downgrade() -> None:
    # No-op: nothing to revert in this empty migration
    pass
