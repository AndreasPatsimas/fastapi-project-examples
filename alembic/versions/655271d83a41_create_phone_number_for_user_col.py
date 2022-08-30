"""create phone number for user col

Revision ID: 655271d83a41
Revises: 
Create Date: 2022-08-23 11:42:37.325592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '655271d83a41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
