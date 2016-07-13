import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""
first commit

Revision ID: 0e83d991a306
Revises: 593bbe8cc8c1
Create Date: 2016-07-12 12:27:38.581132
"""

# Revision identifiers, used by Alembic.
revision = '0e83d991a306'
down_revision = '593bbe8cc8c1'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
