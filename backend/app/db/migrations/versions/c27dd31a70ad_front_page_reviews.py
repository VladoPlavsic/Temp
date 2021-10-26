"""front_page_reviews
Revision ID: c27dd31a70ad
Revises: 3ddd879e1720
Create Date: 2021-10-26 15:04:34.193027
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'c27dd31a70ad'
down_revision = '3ddd879e1720'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("review", sa.Text, nullable=False),
        schema='public'
    )

    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_review(name_ TEXT, review_ TEXT)
    RETURNS TABLE(id INT, name TEXT, review TEXT)
    AS $$
    DECLARE 
        id_ INT;
    BEGIN
        INSERT INTO public.reviews(name, review) VALUES(name_, review_) RETURNING public.reviews.id INTO id_;
        RETURN QUERY(SELECT * FROM public.reviews WHERE public.review.id = id_);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.select_all_reviews()
    RETURNS TABLE(id INT, name TEXT, review TEXT)
    AS $$
    BEGIN
        RETURN QUERY(SELECT * FROM public.reviews);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_review(id_ INT, name_ TEXT, review_ TEXT)
    RETURNS TABLE(id INT, name TEXT, review TEXT)
    AS $$
    BEGIN
        UPDATE public.reviews SET 
            name = COALESCE(name_, public.reviews.name),
            review = COALESCE(review_, public.reviews.review)
        WHERE public.reviews.id = id_; 
        RETURN QUERY(SELECT * FROM public.reviews WHERE public.review.id = id_);
    END $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_review(id_ INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM public.reviews WHERE id = id_;
    END $$ LANGUAGE plpgsql;
    """)

def drop_functions() -> None:
    functions = [
        'insert_review',
        'select_all_reviews',
        'update_review',
        'delete_review'
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")

def downgrade() -> None:
    op.execute("DROP TABLE public.reviews")
    drop_functions()

