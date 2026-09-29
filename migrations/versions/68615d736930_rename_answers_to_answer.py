"""rename answers to answer

Revision ID: 68615d736930
Revises: 003f3ab9102b
Create Date: 2026-09-29 15:50:17.672875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68615d736930'
down_revision: Union[str, Sequence[str], None] = '003f3ab9102b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "form_answers",
        "answers",
        new_column_name="answer",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "form_answers",
        "answer",
        new_column_name="answers",
    )
