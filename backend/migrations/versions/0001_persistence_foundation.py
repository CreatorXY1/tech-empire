"""Establish the migration baseline before Milestone 01 schema work.

Revision ID: 0001_persistence_foundation
Revises:
"""

revision = "0001_persistence_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Establish the migration revision before the initial schema migration.
    pass


def downgrade() -> None:
    pass
