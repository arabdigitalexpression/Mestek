"""empty message

Revision ID: e888d9749456
Revises: 
Create Date: 2022-10-25 18:01:50.105951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e888d9749456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'interval', 'reservation', ['reservation_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'interval', 'calendar', ['calendar_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'interval', type_='foreignkey')
    op.drop_constraint(None, 'interval', type_='foreignkey')
    # ### end Alembic commands ###
