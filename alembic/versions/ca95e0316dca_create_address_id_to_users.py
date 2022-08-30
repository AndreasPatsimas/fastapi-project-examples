"""create address_id to users

Revision ID: ca95e0316dca
Revises: 117c90ea930e
Create Date: 2022-08-23 12:07:33.956008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca95e0316dca'
down_revision = '117c90ea930e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table="users", referent_table="address",
                          local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('address_users_fk', table_name="users")
    op.drop_column('users', 'address_id')
