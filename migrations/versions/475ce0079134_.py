"""empty message

Revision ID: 475ce0079134
Revises: 20c49575539e
Create Date: 2023-10-11 23:59:45.767257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '475ce0079134'
down_revision = '20c49575539e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cliente', 'receita',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cliente', 'receita',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###