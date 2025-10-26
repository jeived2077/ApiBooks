"""Создание заново таблицы

Revision ID: bf1a006ee423
Revises: 1ce50d96ee7a
Create Date: 2025-10-12 14:47:29.948825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf1a006ee423'
down_revision: Union[str, Sequence[str], None] = '1ce50d96ee7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
