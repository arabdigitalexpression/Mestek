"""Updated m2m relation bettween reservations and tools

Revision ID: e32df03b6907
Revises: af9b427e2445
Create Date: 2022-10-04 16:40:56.971327

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e32df03b6907'
down_revision = 'af9b427e2445'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation_tool',
    sa.Column('reservation_id', sa.Integer(), nullable=True),
    sa.Column('tool_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservation.id'], ),
    sa.ForeignKeyConstraint(['tool_id'], ['tool.id'], )
    )
    op.drop_constraint('reservation_ibfk_5', 'reservation', type_='foreignkey')
    op.drop_column('reservation', 'tool_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('tool_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('reservation_ibfk_5', 'reservation', 'tool', ['tool_id'], ['id'])
    op.drop_table('reservation_tool')
    # ### end Alembic commands ###
