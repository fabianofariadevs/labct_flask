"""empty message

Revision ID: 08190411f584
Revises: 8d1242e8572c
Create Date: 2023-11-22 16:13:12.845378

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '08190411f584'
down_revision = '8d1242e8572c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mixproduto_ibfk_6', 'mixproduto', type_='foreignkey')
    op.drop_column('mixproduto', 'producao_id')
    op.create_foreign_key(None, 'producao', 'mixproduto', ['mixproduto_id'], ['id'])
    op.drop_column('producao', 'mix_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('producao', sa.Column('mix_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.add_column('mixproduto', sa.Column('producao_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('mixproduto_ibfk_6', 'mixproduto', 'producao', ['producao_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
