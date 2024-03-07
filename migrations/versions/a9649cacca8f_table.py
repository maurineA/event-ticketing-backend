"""table

Revision ID: a9649cacca8f
Revises: e13e1d42f577
Create Date: 2024-03-07 18:13:39.339825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9649cacca8f'
down_revision = 'e13e1d42f577'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('start_date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)
        batch_op.alter_column('end_date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_column('purchase_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase_date', sa.DATETIME(), nullable=True))

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('end_date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)
        batch_op.alter_column('start_date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###