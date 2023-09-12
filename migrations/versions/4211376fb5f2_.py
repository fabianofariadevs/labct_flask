"""empty message

Revision ID: 4211376fb5f2
Revises: bc51cd8b16f6
Create Date: 2023-09-07 17:55:07.759790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4211376fb5f2'
down_revision = 'bc51cd8b16f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pedidoproducao', 'quantidade',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pedidoproducao', 'quantidade',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
