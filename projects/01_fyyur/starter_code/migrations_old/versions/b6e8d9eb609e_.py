"""empty message

Revision ID: b6e8d9eb609e
Revises: c2d50b57595b
Create Date: 2021-03-22 20:52:25.378301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6e8d9eb609e'
down_revision = 'c2d50b57595b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('looking_for_description', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('looking_for_venues', sa.Boolean(), nullable=False))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'looking_for_venues')
    op.drop_column('Artist', 'looking_for_description')
    # ### end Alembic commands ###
