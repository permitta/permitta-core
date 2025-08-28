from database import Database
from database.src.database_seeder import DatabaseSeeder

db: Database = Database()
db.connect(echo_statements=True)
db.drop_all_tables()
db.create_all_tables()
database_seeder: DatabaseSeeder = DatabaseSeeder(db=db)
database_seeder.seed()
