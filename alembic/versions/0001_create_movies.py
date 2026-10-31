from alembic import op
import sqlalchemy as sa

revision = "0001_create_movies"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("genre", sa.String(length=100), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False, server_default="0"),
        sa.CheckConstraint("year >= 1888 AND year <= 2100", name="ck_movies_year"),
        sa.CheckConstraint("rating >= 0 AND rating <= 10", name="ck_movies_rating"),
    )
    op.create_index("ix_movies_title", "movies", ["title"])
    op.create_index("ix_movies_year", "movies", ["year"])
    op.create_index("ix_movies_genre", "movies", ["genre"])


def downgrade():
    op.drop_index("ix_movies_genre", table_name="movies")
    op.drop_index("ix_movies_year", table_name="movies")
    op.drop_index("ix_movies_title", table_name="movies")
    op.drop_table("movies")
