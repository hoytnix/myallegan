import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""
first commit

Revision ID: 593bbe8cc8c1
Revises: 67103e707302
Create Date: 2016-07-12 12:10:58.329414
"""

# Revision identifiers, used by Alembic.
revision = '593bbe8cc8c1'
down_revision = '67103e707302'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
