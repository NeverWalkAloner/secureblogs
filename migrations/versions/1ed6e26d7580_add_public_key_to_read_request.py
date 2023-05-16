"""Add public key to read request

Revision ID: 1ed6e26d7580
Revises: 815c08907f63
Create Date: 2023-05-16 09:19:00.026700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ed6e26d7580'
down_revision = '815c08907f63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('read_post_request', sa.Column('public_key_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'read_post_request', 'user_keys', ['public_key_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'read_post_request', type_='foreignkey')
    op.drop_column('read_post_request', 'public_key_id')
    # ### end Alembic commands ###