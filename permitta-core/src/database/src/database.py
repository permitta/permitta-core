from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .database_config import DatabaseConfig

BaseModel = declarative_base()


class Database:
    """
    Usage:

    database: Database = Database()     # no config required
    database.Session.begin() as session:
        session.add(thing)
    # commit is automatic when exiting the with block
    """

    engine: Engine
    Session: sessionmaker
    config: DatabaseConfig

    def __init__(self):
        self.config: DatabaseConfig = DatabaseConfig.load()

    def create_engine(self, echo_statements: bool = False) -> Engine:
        engine: Engine = create_engine(
            self.config.connection_string,
            echo=echo_statements,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        return engine

    def connect(self, echo_statements: bool = False) -> None:
        self.engine: Engine = self.create_engine(
            echo_statements=echo_statements,
        )
        self.Session = sessionmaker(self.engine)

    def create_all_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_all_tables(self):
        BaseModel.metadata.drop_all(self.engine)

    def disconnect(self) -> None:
        self.engine.dispose()
