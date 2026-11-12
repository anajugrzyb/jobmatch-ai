"""Add normalized job source metadata and deduplication.

Revision ID: 0003
Revises: 0002
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("jobs", sa.Column("source", sa.String(40), nullable=False, server_default="manual"))
    op.add_column("jobs", sa.Column("source_id", sa.String(160), nullable=True))
    op.add_column("jobs", sa.Column("location", sa.String(200), nullable=False, server_default=""))
    op.add_column("jobs", sa.Column("remote", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("jobs", sa.Column("tags", sa.Text(), nullable=False, server_default=""))
    op.add_column("jobs", sa.Column("published_at", sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint("uq_jobs_source_id", "jobs", ["source", "source_id"])
    op.create_index("ix_jobs_published_at", "jobs", ["published_at"])


def downgrade():
    op.drop_index("ix_jobs_published_at", table_name="jobs")
    op.drop_constraint("uq_jobs_source_id", "jobs", type_="unique")
    for name in ("published_at", "tags", "remote", "location", "source_id", "source"):
        op.drop_column("jobs", name)
