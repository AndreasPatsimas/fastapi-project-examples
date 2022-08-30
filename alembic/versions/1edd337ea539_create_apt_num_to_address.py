"""create apt_num to address

Revision ID: 1edd337ea539
Revises: ca95e0316dca
Create Date: 2022-08-23 13:08:28.272427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1edd337ea539'
down_revision = 'ca95e0316dca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.String(10), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
