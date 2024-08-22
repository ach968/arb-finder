"""initial migration

Revision ID: 1836a278afde
Revises: 
Create Date: 2024-08-14 16:31:42.314433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1836a278afde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.alter_column('key',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('group',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['key'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('description',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('group',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('key',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)

    op.create_table('game',
    sa.Column('event', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('+ odd', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('- odd', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='games_pkey')
    )
    # ### end Alembic commands ###
