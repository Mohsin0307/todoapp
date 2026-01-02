"""Add conversations and messages tables for chat sessions

Revision ID: 593e12a58a3
Revises: d5f30417d351
Create Date: 2025-12-31 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '593e12a58a3'
down_revision = 'd5f30417d351'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'], unique=False)
    op.create_index('ix_conversations_user_id_created', 'conversations', ['user_id', 'created_at'], unique=False)

    # Create message_role enum type
    message_role_enum = postgresql.ENUM('user', 'assistant', name='messagerole')
    message_role_enum.create(op.get_bind())

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', message_role_enum, nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'], unique=False)
    op.create_index('ix_messages_conversation_id_created', 'messages', ['conversation_id', 'created_at'], unique=False)
    op.create_index('ix_messages_user_id', 'messages', ['user_id'], unique=False)
    op.create_index('ix_messages_user_id_conversation_id', 'messages', ['user_id', 'conversation_id'], unique=False)


def downgrade() -> None:
    # Drop messages table and indexes
    op.drop_index('ix_messages_user_id_conversation_id', table_name='messages')
    op.drop_index('ix_messages_user_id', table_name='messages')
    op.drop_index('ix_messages_conversation_id_created', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    # Drop message_role enum type
    message_role_enum = postgresql.ENUM('user', 'assistant', name='messagerole')
    message_role_enum.drop(op.get_bind())

    # Drop conversations table and indexes
    op.drop_index('ix_conversations_user_id_created', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
