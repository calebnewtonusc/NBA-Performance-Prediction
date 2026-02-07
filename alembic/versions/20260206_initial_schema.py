"""Initial NBA Prediction Database Schema

Revision ID: 001_initial
Revises:
Create Date: 2026-02-06 14:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_email', 'users', ['email'])

    # Predictions table
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('prediction_type', sa.String(length=20), nullable=False),  # 'game' or 'player'
        sa.Column('model_name', sa.String(length=50), nullable=False),
        sa.Column('model_version', sa.String(length=20), nullable=False, server_default='v1'),
        # Game prediction fields
        sa.Column('home_team', sa.String(length=3), nullable=True),
        sa.Column('away_team', sa.String(length=3), nullable=True),
        sa.Column('prediction', sa.String(length=10), nullable=True),  # 'home' or 'away'
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('home_win_probability', sa.Float(), nullable=True),
        sa.Column('away_win_probability', sa.Float(), nullable=True),
        # Player prediction fields
        sa.Column('player_name', sa.String(length=100), nullable=True),
        sa.Column('predicted_points', sa.Float(), nullable=True),
        # Metadata
        sa.Column('features', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('cached', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_predictions_user_id', 'predictions', ['user_id'])
    op.create_index('idx_predictions_request_id', 'predictions', ['request_id'])
    op.create_index('idx_predictions_type', 'predictions', ['prediction_type'])
    op.create_index('idx_predictions_created_at', 'predictions', ['created_at'])
    op.create_index('idx_predictions_teams', 'predictions', ['home_team', 'away_team'])

    # Model metadata table
    op.create_table(
        'model_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_name', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('model_type', sa.String(length=50), nullable=False),  # 'classification' or 'regression'
        sa.Column('algorithm', sa.String(length=50), nullable=False),  # 'logistic', 'ridge', etc.
        sa.Column('accuracy', sa.Float(), nullable=True),
        sa.Column('metrics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('hyperparameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('feature_count', sa.Integer(), nullable=True),
        sa.Column('training_samples', sa.Integer(), nullable=True),
        sa.Column('trained_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('model_name', 'version', name='uq_model_name_version')
    )
    op.create_index('idx_model_metadata_name_version', 'model_metadata', ['model_name', 'version'])
    op.create_index('idx_model_metadata_active', 'model_metadata', ['is_active'])

    # Audit logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('resource', sa.String(length=100), nullable=True),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('idx_audit_logs_request_id', 'audit_logs', ['request_id'])

    # API keys table (for programmatic access)
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('prefix', sa.String(length=10), nullable=False),  # First few chars for identification
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('rate_limit', sa.Integer(), nullable=True),  # Custom rate limit per key
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash')
    )
    op.create_index('idx_api_keys_user_id', 'api_keys', ['user_id'])
    op.create_index('idx_api_keys_prefix', 'api_keys', ['prefix'])
    op.create_index('idx_api_keys_active', 'api_keys', ['is_active'])


def downgrade() -> None:
    op.drop_table('api_keys')
    op.drop_table('audit_logs')
    op.drop_table('model_metadata')
    op.drop_table('predictions')
    op.drop_table('users')
