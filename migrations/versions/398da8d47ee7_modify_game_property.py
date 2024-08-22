"""modify Game property

Revision ID: 398da8d47ee7
Revises: f2cb945998b7
Create Date: 2024-08-14 19:13:29.884492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398da8d47ee7'
down_revision = 'f2cb945998b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bookmaker_key', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('bookmaker', sa.String(), nullable=True))
        batch_op.drop_column('platform_key')
        batch_op.drop_column('platform')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('platform_key', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('bookmaker')
        batch_op.drop_column('bookmaker_key')

    # ### end Alembic commands ###
