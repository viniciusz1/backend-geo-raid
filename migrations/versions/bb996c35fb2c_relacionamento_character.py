from alembic import op
import sqlalchemy as sa

# revison identifiers
revision = "bb996c35fb2c"
down_revision = "5cb058718179"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        # 1) adiciona a coluna
        batch_op.add_column(sa.Column("character_id", sa.Integer(), nullable=True))
        # 2) cria a UNIQUE constraint com nome explícito
        batch_op.create_unique_constraint(
            "uq_usuario_character_id",  # <— nome da constraint
            ["character_id"],
        )
        # 3) cria a FK com nome explícito
        batch_op.create_foreign_key(
            "fk_usuario_character",  # <— nome da FK
            "character",  # tabela referenciada
            ["character_id"],  # coluna local
            ["id"],  # coluna referenciada
        )


def downgrade():
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.drop_constraint("fk_usuario_character", type_="foreignkey")
        batch_op.drop_constraint("uq_usuario_character_id", type_="unique")
        batch_op.drop_column("character_id")
