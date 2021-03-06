"""empty message

Revision ID: 388f372e7752
Revises: b6e8d9eb609e
Create Date: 2021-03-23 01:00:54.447398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '388f372e7752'
down_revision = 'b6e8d9eb609e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    # ### end Alembic commands ###
