"""empty message

Revision ID: 46a9765eb2ad
Revises: b586d2beb83f
Create Date: 2023-11-17 18:57:07.662549

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '46a9765eb2ad'
down_revision = 'b586d2beb83f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quantidade_mix_produtos', 'produto_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('quantidade_mix_produtos', 'mix_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quantidade_mix_produtos', 'mix_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('quantidade_mix_produtos', 'produto_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
