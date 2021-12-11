"""create_cats_table

Revision ID: 382b84a3c7af
Revises: 90c9385481ba
Create Date: 2021-12-11 12:11:00.474778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "382b84a3c7af"
down_revision = None
branch_labels = None
depends_on = None


def create_cats_table() -> None:
    op.create_table(
        "cats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("kind", sa.Text, nullable=False),
        sa.Column("age", sa.Integer, nullable=False),
        sa.Column("sex", sa.Text, nullable=False),
        sa.Column("favorite_foods", sa.ARRAY(sa.Text), nullable=False),
        sa.Column("owner", sa.Text, nullable=False),
    )


def upgrade() -> None:
    create_cats_table()


def downgrade() -> None:
    op.drop_table("cats")
