"""modify Sport property

Revision ID: b1c416bfa906
Revises: 80e02f45b160
Create Date: 2024-08-14 16:45:00.645318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c416bfa906'
down_revision = '80e02f45b160'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.alter_column('updated',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sport', schema=None) as batch_op:
        batch_op.alter_column('updated',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
