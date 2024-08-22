"""modify Game property

Revision ID: f2cb945998b7
Revises: b1c416bfa906
Create Date: 2024-08-14 18:59:27.657026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2cb945998b7'
down_revision = 'b1c416bfa906'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_update', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('platform_key', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('market', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('time_sent', sa.Float(), nullable=True))
        batch_op.alter_column('platform',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('last_updated')
        batch_op.drop_column('type')

    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_sent', sa.Float(), nullable=True))
        batch_op.drop_column('updated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
        batch_op.drop_column('time_sent')

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('last_updated', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
        batch_op.alter_column('platform',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('time_sent')
        batch_op.drop_column('market')
        batch_op.drop_column('platform_key')
        batch_op.drop_column('last_update')

    # ### end Alembic commands ###
