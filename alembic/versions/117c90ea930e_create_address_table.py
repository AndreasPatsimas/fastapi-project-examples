"""create address table

Revision ID: 117c90ea930e
Revises: 655271d83a41
Create Date: 2022-08-23 11:55:44.512818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '117c90ea930e'
down_revision = '655271d83a41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(50), nullable=False),
                    sa.Column('address2', sa.String(50), nullable=False),
                    sa.Column('city', sa.String(50), nullable=False),
                    sa.Column('state', sa.String(50), nullable=False),
                    sa.Column('country', sa.String(50), nullable=False),
                    sa.Column('postalcode', sa.String(10), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('address')
