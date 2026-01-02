"""Create tasks table with soft delete support

Revision ID: 2b75041faad1
Revises: 
Create Date: 2025-12-31 01:36:20.578322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b75041faad1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create tasks table with soft delete support."""
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('LENGTH(title) >= 1', name='check_title_not_empty')
    )

    # Create indexes
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'], unique=False)
    op.create_index('ix_tasks_user_created', 'tasks', ['user_id', 'created_at'], unique=False)
    op.create_index(
        'ix_tasks_active',
        'tasks',
        ['user_id', 'deleted_at'],
        unique=False,
        postgresql_where=sa.text('deleted_at IS NULL')
    )


def downgrade() -> None:
    """Downgrade schema - Drop tasks table."""
    # Drop indexes
    op.drop_index('ix_tasks_active', table_name='tasks')
    op.drop_index('ix_tasks_user_created', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_index('ix_tasks_id', table_name='tasks')

    # Drop table
    op.drop_table('tasks')
