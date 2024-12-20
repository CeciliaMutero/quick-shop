"""Added cart_items relationship in User model, and  products models

Revision ID: 216513920ac2
Revises: 
Create Date: 2024-10-30 17:42:39.665057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '216513920ac2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)

    # ### end Alembic commands ###
