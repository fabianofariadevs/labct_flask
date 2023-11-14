"""empty message

Revision ID: 267c61442c4b
Revises: c386617e478f
Create Date: 2023-11-04 02:35:22.706314

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '267c61442c4b'
down_revision = 'c386617e478f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'producao', 'usuario', ['usuario_id'], ['id'])
    op.create_foreign_key(None, 'producao', 'pedidoproducao', ['pedidosprod_id'], ['id'])
    op.create_foreign_key(None, 'producao', 'mixproduto', ['mixproduto_id'], ['id'])
    op.drop_column('producao', 'pedidoproducao_id')
    op.drop_constraint('usuario_ibfk_3', 'usuario', type_='foreignkey')
    op.drop_column('usuario', 'producao_id', sa.Integer(), sa.ForeignKey('producao.id'), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('producao_id', sa.Integer(), sa.ForeignKey('producao.id'), nullable=False))
    op.create_foreign_key('usuario_ibfk_3', 'usuario', 'producao', ['producao_id'], ['id'])
    op.add_column('producao', sa.Column('pedidoproducao_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.drop_constraint(None, 'producao', type_='foreignkey')
    # ### end Alembic commands ###
