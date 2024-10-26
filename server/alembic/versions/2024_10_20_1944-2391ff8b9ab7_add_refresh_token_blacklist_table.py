"""Add 'refresh_token_blacklist' table

Revision ID: 2391ff8b9ab7
Revises: a2a3c10e738c
Create Date: 2024-10-20 19:44:19.114670

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2391ff8b9ab7"
down_revision: Union[str, None] = "a2a3c10e738c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refresh_token_blacklist",
        sa.Column("token_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("token_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("refresh_token_blacklist")
    # ### end Alembic commands ###