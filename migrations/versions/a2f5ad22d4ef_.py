"""empty message

Revision ID: a2f5ad22d4ef
Revises: af5d13b9f5a1
Create Date: 2023-08-01 19:10:56.695513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a2f5ad22d4ef'
down_revision = 'af5d13b9f5a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pedido',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('qtde_pedido', sa.Integer(), nullable=True),
    sa.Column('data_pedido', sa.DateTime(), nullable=True),
    sa.Column('data_entrega', sa.Date(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('obs', sa.Text(), nullable=True),
    sa.Column('tipo', sa.Enum('compra', 'producao', name='tipoenum'), nullable=False),
    sa.Column('cadastrado_em', sa.DateTime(), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), nullable=True),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('fornecedor_id', sa.Integer(), nullable=True),
    sa.Column('filial_pdv', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filial_pdv'], ['filial.id'], ),
    sa.ForeignKeyConstraint(['fornecedor_id'], ['fornecedor.id'], ),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receita_produto',
    sa.Column('receita_id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.ForeignKeyConstraint(['receita_id'], ['receita.id'], ),
    sa.PrimaryKeyConstraint('receita_id', 'produto_id')
    )
    op.drop_constraint('filial_ibfk_1', 'filial', type_='foreignkey')
    op.drop_column('filial', 'receita')
    op.drop_column('fornecedor', 'produto_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fornecedor', sa.Column('produto_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('filial', sa.Column('receita', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('filial_ibfk_1', 'filial', 'receita', ['receita'], ['id'])
    op.drop_table('receita_produto')
    op.drop_table('pedido')
    # ### end Alembic commands ###
