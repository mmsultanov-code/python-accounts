"""'seed-permissions'

Revision ID: d67b16498456
Revises: b6e14ca11190
Create Date: 2024-09-21 06:23:06.966657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd67b16498456'
down_revision: Union[str, None] = 'b6e14ca11190'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

permissions_table = sa.table(
    'permission',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
    sa.column('slug', sa.Date)
)

def upgrade() -> None:
    # Вставляем начальные данные в таблицу accounts с помощью bulk_insert.
    op.bulk_insert(permissions_table,
        [
            {"id": 1, "name": "Super Admin", "slug": "super_admin_index"},
            {"id": 2, "name": "Super Admin", "slug": "super_admin_create"},
            {"id": 3, "name": "Super Admin", "slug": "super_admin_read"},
            {"id": 4, "name": "Super Admin", "slug": "super_admin_update"},
            {"id": 5, "name": "Super Admin", "slug": "super_admin_delete"},
            {"id": 6, "name": "Super Admin", "slug": "super_admin_all"},
            {"id": 7, "name": "User", "slug": "user_index"},
            {"id": 8, "name": "User", "slug": "user_create"},
            {"id": 9, "name": "User", "slug": "user_read"},
            {"id": 10, "name": "User", "slug": "user_update"},
            {"id": 11, "name": "User", "slug": "user_delete"},
            {"id": 12, "name": "User", "slug": "user_all"},
            {"id": 13, "name": "Permission", "slug": "permission_index"},
            {"id": 14, "name": "Permission", "slug": "permission_create"},
            {"id": 15, "name": "Permission", "slug": "permission_read"},
            {"id": 16, "name": "Permission", "slug": "permission_update"},
            {"id": 17, "name": "Permission", "slug": "permission_delete"},
            {"id": 18, "name": "Permission", "slug": "permission_all"},
            {"id": 19, "name": "Role", "slug": "role_index"},
            {"id": 20, "name": "Role", "slug": "role_create"},
            {"id": 21, "name": "Role", "slug": "role_read"},
            {"id": 22, "name": "Role", "slug": "role_update"},
            {"id": 23, "name": "Role", "slug": "role_delete"},
            {"id": 24, "name": "Role", "slug": "role_all"},
            {"id": 25, "name": "Accounts", "slug": "accounts_index"},
            {"id": 26, "name": "Accounts", "slug": "accounts_create"},
            {"id": 27, "name": "Accounts", "slug": "accounts_read"},
            {"id": 28, "name": "Accounts", "slug": "accounts_update"},
            {"id": 29, "name": "Accounts", "slug": "accounts_delete"},
            {"id": 30, "name": "Accounts", "slug": "accounts_all"},
            {"id": 31, "name": "Incoming Funds", "slug": "incoming_funds_index"},
            {"id": 32, "name": "Incoming Funds", "slug": "incoming_funds_create"},
            {"id": 33, "name": "Incoming Funds", "slug": "incoming_funds_read"},
            {"id": 34, "name": "Incoming Funds", "slug": "incoming_funds_update"},
            {"id": 35, "name": "Incoming Funds", "slug": "incoming_funds_delete"},
            {"id": 36, "name": "Incoming Funds", "slug": "incoming_funds_all"}
        ]
    )

def downgrade() -> None:
    op.execute(permissions_table.delete())