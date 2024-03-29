"""empty message

Revision ID: 4538d45fe75b
Revises: 1f390589456e
Create Date: 2023-11-13 13:52:49.775960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4538d45fe75b'
down_revision = '1f390589456e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mixproduto', 'quantidade',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mixproduto', 'quantidade',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
