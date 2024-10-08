"""adding Game model

Revision ID: 80e02f45b160
Revises: 1836a278afde
Create Date: 2024-08-14 16:41:46.517330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80e02f45b160'
down_revision = '1836a278afde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('sport_key', sa.String(), nullable=False),
    sa.Column('sport_title', sa.String(), nullable=True),
    sa.Column('commence_time', sa.Float(), nullable=True),
    sa.Column('last_updated', sa.Float(), nullable=True),
    sa.Column('platform', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    # ### end Alembic commands ###
