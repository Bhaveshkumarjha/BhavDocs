from app import db

with db.engine.connect() as conn:
    conn.execute("DROP TABLE IF EXISTS alembic_version")