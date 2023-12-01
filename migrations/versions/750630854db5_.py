"""empty message

Revision ID: 750630854db5
Revises: 708957ad58a0
Create Date: 2023-11-10 16:01:10.157527

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '750630854db5'
down_revision = '708957ad58a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funcao', sa.Column('cadastrado_em', sa.DateTime(), nullable=True))
    op.add_column('funcao', sa.Column('atualizado_em', sa.DateTime(), nullable=True))
    op.add_column('funcao', sa.Column('cliente_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'funcao', 'cliente', ['cliente_id'], ['id'])
    op.drop_column('funcao', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funcao', sa.Column('status', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'funcao', type_='foreignkey')
    op.drop_column('funcao', 'cliente_id')
    op.drop_column('funcao', 'atualizado_em')
    op.drop_column('funcao', 'cadastrado_em')
    # ### end Alembic commands ###