"""add nroempresa to stores

Revision ID: 5d58a213c91e
Revises: 2a3cdf5614dd
Create Date: 2026-09-29 10:55:51.483428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d58a213c91e'
down_revision: Union[str, Sequence[str], None] = '2a3cdf5614dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "stores",
        sa.Column(
            "nroempresa",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_stores_nroempresa",
        "stores",
        ["nroempresa"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "stores",
        "nroempresa",
    )

    op.drop_column(
        "stores",
        "nroempresa",
    )
