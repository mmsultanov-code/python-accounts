"""'seed-users'

Revision ID: 3013c26cfabb
Revises: cfedee4f76c4
Create Date: 2024-09-21 06:54:11.037349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_table = sa.table(
    'user',
    sa.Column('id', sa.Integer, primary_key=True, index=True),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('email', sa.String(255), nullable=False, unique=True),
    sa.Column('password', sa.String(255), nullable=False),
    sa.Column('avatar', sa.String(255), nullable=True),
    sa.Column('created_at', sa.Date, nullable=False, default=datetime.utcnow),
    sa.Column('updated_at', sa.Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
    sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id'), nullable=False)
)


# revision identifiers, used by Alembic.
revision: str = '3013c26cfabb'
down_revision: Union[str, None] = 'cfedee4f76c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(user_table, [
        {"id": 1, "name": "Super Admin", "email": "test@example.com", "password": pwd_context.hash("test"), "avatar": "test", "role_id": 2},
        {"id": 2, "name": "User", "email": "test_user@example.com", "password": pwd_context.hash("test"), "avatar": "test", "role_id": 1}
    ])


def downgrade() -> None:
    op.execute(user_table.delete())