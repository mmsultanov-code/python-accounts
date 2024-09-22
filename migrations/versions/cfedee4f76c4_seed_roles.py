"""'seed-roles'

Revision ID: cfedee4f76c4
Revises: d67b16498456
Create Date: 2024-09-21 06:26:10.235002

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

role_table = sa.table(
    'role',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
    sa.column('slug', sa.String),
    sa.column('created_at', sa.DateTime),
    sa.column('updated_at', sa.DateTime),
)

role_permission_table = sa.table(
    'role_permission',
    sa.column('role_id', sa.Integer),
    sa.column('permission_id', sa.Integer),
)

admin_permissions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]

# revision identifiers, used by Alembic.
revision: str = 'cfedee4f76c4'
down_revision: Union[str, None] = 'd67b16498456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Вставляем роли в таблицу role.
    op.bulk_insert(role_table,
        [
            {
                "id": 1,
                "name": "User",
                "slug": "user_role",
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()},
            {
                "id": 2,
                "name": "Admin",
                "slug": "admin_role",
                "created_at": datetime.datetime.now(),
                "updated_at": datetime.datetime.now()}
        ]
    )

    # Вставляем связи между ролью Admin и правами.
    op.bulk_insert(role_permission_table,
        [{"role_id": 2, "permission_id": permission_id} for permission_id in admin_permissions]
    )

def downgrade() -> None:
    op.execute(role_permission_table.delete())
    op.execute(role_table.delete())