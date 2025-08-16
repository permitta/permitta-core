from database import Database
from models import (
    AttributeDto,
    PrincipalAttributeStagingDbo,
    PrincipalDbo,
    PrincipalStagingDbo,
)

from ..src.principal_repository import PrincipalRepository


def test_truncate_staging(database: Database) -> None:
    repo: PrincipalRepository = PrincipalRepository()

    with database.Session.begin() as session:
        session.add(PrincipalStagingDbo())
        session.add(PrincipalAttributeStagingDbo())
        session.commit()

    with database.Session.begin() as session:
        assert session.query(PrincipalStagingDbo).count() == 1
        assert session.query(PrincipalAttributeStagingDbo).count() == 1

        repo.truncate_staging_tables(session=session)
        session.commit()

    with database.Session.begin() as session:
        assert session.query(PrincipalStagingDbo).count() == 0
        assert session.query(PrincipalAttributeStagingDbo).count() == 0


def test_get_all(database: Database) -> None:
    repo: PrincipalRepository = PrincipalRepository()

    with database.Session.begin() as session:
        principal_count, principals = repo.get_all(
            session=session,
        )

        assert principal_count == 5
        assert all([isinstance(p, PrincipalDbo) for p in principals])
        assert len(principals) == 5

        # TODO check attributes - each should have > 1 ad groups
        assert all([len(p.attributes) >= 1 for p in principals])
        assert all([p.attributes[0].attribute_key == "ad_group" for p in principals])


def test_get_by_username(database: Database) -> None:
    repo: PrincipalRepository = PrincipalRepository()

    with database.Session.begin() as session:
        principal: PrincipalDbo = repo.get_by_username(
            session=session, user_name="alice"
        )

        assert principal.user_name == "alice"
        assert principal.first_name == "Alice"
        assert principal.last_name == "Cooper"
