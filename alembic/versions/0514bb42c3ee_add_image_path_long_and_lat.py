"""Add image_path long and lat

Revision ID: 0514bb42c3ee
Revises: ab0f6ec08e70
Create Date: 2024-07-11 01:50:44.725156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0514bb42c3ee'
down_revision: Union[str, None] = 'ab0f6ec08e70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('latitude', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('longitude', sa.String(), nullable=True))
    op.add_column('projects', sa.Column('image_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'image_path')
    op.drop_column('projects', 'longitude')
    op.drop_column('projects', 'latitude')
    # ### end Alembic commands ###