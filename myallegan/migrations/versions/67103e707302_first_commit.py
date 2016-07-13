import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""
first commit

Revision ID: 67103e707302
Revises: 
Create Date: 2016-07-12 11:46:43.702204
"""

# Revision identifiers, used by Alembic.
revision = '67103e707302'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
