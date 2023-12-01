"""empty message

Revision ID: 62c4d300fb37
Revises: 60728dafb7e1
Create Date: 2023-11-01 10:35:49.532113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '62c4d300fb37'
down_revision = '60728dafb7e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('produto', 'estoque_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('receita', 'usuario',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('receita', 'usuario',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('produto', 'estoque_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###