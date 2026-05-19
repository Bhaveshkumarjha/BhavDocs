"""Add folder_id column to File

Revision ID: 87c029266fe0
Revises: fbacf2b83106
Create Date: 2025-08-31 11:58:43.031592
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '87c029266fe0'
down_revision = 'fbacf2b83106'
branch_labels = None
depends_on = None

def upgrade():
    # ✅ Folder table already exists — skip creating it

    # Add folder_id column to file table with named foreign key
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('folder_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_file_folder_id',  # Named constraint
            'folder',
            ['folder_id'],
            ['id']
        )

def downgrade():
    # Remove folder_id column and foreign key
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.drop_constraint('fk_file_folder_id', type_='foreignkey')
        batch_op.drop_column('folder_id')

    # ✅ Do NOT drop folder table — it was not created here