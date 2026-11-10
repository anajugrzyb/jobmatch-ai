"""Create local professional profile.

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "professional_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(160), nullable=False),
        sa.Column("headline", sa.String(240), nullable=False),
        sa.Column("location", sa.String(160), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("skills", sa.Text(), nullable=False),
        sa.Column("experience", sa.Text(), nullable=False),
        sa.Column("education", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("professional_profiles")
