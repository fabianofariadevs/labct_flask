"""empty message

Revision ID: 708957ad58a0
Revises: 338cfdbda80a
Create Date: 2023-11-10 15:46:32.827450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708957ad58a0'
down_revision = '338cfdbda80a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funcao', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('funcao', sa.Column('cadastrado_em', sa.DateTime(), nullable=False))
    op.add_column('funcao', sa.Column('atualizado_em', sa.DateTime(), nullable=True))
    op.add_column('funcao', sa.Column('cliente_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'funcao', 'cliente', ['cliente_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'funcao', type_='foreignkey')
    op.drop_column('funcao', 'cliente_id')
    op.drop_column('funcao', 'atualizado_em')
    op.drop_column('funcao', 'cadastrado_em')
    op.drop_column('funcao', 'status')
    # ### end Alembic commands ###