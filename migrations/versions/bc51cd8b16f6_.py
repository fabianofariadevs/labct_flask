"""empty message

Revision ID: bc51cd8b16f6
Revises: 9252d692b572
Create Date: 2023-09-07 16:43:54.553474

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc51cd8b16f6'
down_revision = '9252d692b572'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receita', sa.Column('quantidades', sa.Integer(), nullable=True))
    op.drop_column('receita', 'produto_quantidades')
    op.add_column('receita_produto', sa.Column('quantidades', sa.Integer(), nullable=False))
    op.drop_column('receita_produto', 'quantidade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receita_produto', sa.Column('quantidade', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('receita_produto', 'quantidades')
    op.add_column('receita', sa.Column('produto_quantidades', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('receita', 'quantidades')
    # ### end Alembic commands ###
