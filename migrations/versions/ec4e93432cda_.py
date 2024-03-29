"""empty message

Revision ID: ec4e93432cda
Revises: 74cb471b6116
Create Date: 2023-11-05 10:10:20.233001

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ec4e93432cda'
down_revision = '74cb471b6116'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('inventario_ibfk_3', 'inventario', type_='foreignkey')
    op.drop_column('inventario', 'produto_id')
    op.create_foreign_key(None, 'producao', 'usuario', ['usuario_id'], ['id'])
    op.create_foreign_key(None, 'producao', 'mixproduto', ['mixproduto_id'], ['id'])
    op.create_foreign_key(None, 'producao', 'pedidoproducao', ['pedidosprod_id'], ['id'])
    op.drop_column('producao', 'pedidoproducao_id')
    op.add_column('produto', sa.Column('inventario_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'produto', 'inventario', ['inventario_id'], ['id'])
    op.drop_constraint('usuario_ibfk_3', 'usuario', type_='foreignkey')
    op.drop_column('usuario', 'producao_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('producao_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('usuario_ibfk_3', 'usuario', 'producao', ['producao_id'], ['id'])
    op.drop_constraint(None, 'produto', type_='foreignkey')
    op.drop_column('produto', 'inventario_id')
    op.add_column('producao', sa.Column('pedidoproducao_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.drop_constraint(None, 'producao', type_='foreignkey')
    op.add_column('inventario', sa.Column('produto_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('inventario_ibfk_3', 'inventario', 'produto', ['produto_id'], ['id'])
    # ### end Alembic commands ###
