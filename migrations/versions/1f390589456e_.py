"""empty message

Revision ID: 1f390589456e
Revises: 750630854db5
Create Date: 2023-11-12 02:53:12.483172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f390589456e'
down_revision = '750630854db5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mixproduto', sa.Column('quantidade', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mixproduto', 'quantidade')
    # ### end Alembic commands ###