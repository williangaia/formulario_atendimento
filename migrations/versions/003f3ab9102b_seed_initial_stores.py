"""seed initial stores

Revision ID: 003f3ab9102b
Revises: 5d58a213c91e
Create Date: 2026-09-29 11:21:46.540683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003f3ab9102b'
down_revision: Union[str, Sequence[str], None] = '5d58a213c91e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    stores_table = sa.table(
        "stores",
        sa.column("nroempresa", sa.Integer),
        sa.column("slug", sa.String),
        sa.column("name", sa.String),
        sa.column("is_active", sa.Boolean),
    )

    op.bulk_insert(
        stores_table,
        [
            {
                "nroempresa": 1,
                "slug": "matriz",
                "name" : "Matriz",
                "is_active": True,
            },
            {
                "nroempresa": 2,
                "slug": "express",
                "name" : "Express",
                "is_active": True,
            },
            {
                "nroempresa": 3,
                "slug": "vila",
                "name" : "Vila",
                "is_active": True,
            },
            {
                "nroempresa": 5,
                "slug": "getat",
                "name" : "Getat",
                "is_active": False,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DELETE FROM stores
            WHERE nroempresa in (1, 2, 3, 5)
            """
        )
    )
