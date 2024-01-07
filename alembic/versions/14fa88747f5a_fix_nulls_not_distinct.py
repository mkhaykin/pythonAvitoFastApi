"""fix nulls_not_distinct

Revision ID: 14fa88747f5a
Revises: 2d7ddf8c34ca
Create Date: 2024-01-07 09:36:56.701123

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "14fa88747f5a"
down_revision: str | None = "2d7ddf8c34ca"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uc_query", "query", type_="unique")
    op.create_unique_constraint(
        "uc_query",
        "query",
        ["region_id", "category_id", "query"],
        postgresql_nulls_not_distinct=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uc_query", "query", type_="unique")
    op.create_unique_constraint(
        "uc_query",
        "query",
        ["region_id", "category_id", "query"],
    )
    # ### end Alembic commands ###
