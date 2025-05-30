"""Criar tabela character

Revision ID: 5cb058718179
Revises: b74624eda213
Create Date: 2025-05-06 20:48:11.783965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb058718179'
down_revision = 'b74624eda213'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('skin', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_character_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_character_skin'), ['skin'], unique=True)

    with op.batch_alter_table('personagem', schema=None) as batch_op:
        batch_op.drop_index('ix_personagem_nome')
        batch_op.drop_index('ix_personagem_skin')

    op.drop_table('personagem')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personagem',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=100), nullable=True),
    sa.Column('skin', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('personagem', schema=None) as batch_op:
        batch_op.create_index('ix_personagem_skin', ['skin'], unique=1)
        batch_op.create_index('ix_personagem_nome', ['nome'], unique=1)

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_character_skin'))
        batch_op.drop_index(batch_op.f('ix_character_name'))

    op.drop_table('character')
    # ### end Alembic commands ###
