from database import Database
from models import *


def create_db():
    db: Database = Database()
    db.connect(echo_statements=True)
    db.drop_all_tables()
    db.create_all_tables()


if __name__ == "__main__":
    create_db()
