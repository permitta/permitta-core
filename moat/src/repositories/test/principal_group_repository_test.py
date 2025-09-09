# from database import Database
# from models import (
#     PrincipalAttributeDbo,
#     PrincipalDbo,
# )
#
#
# def test_get_principal_groups(database: Database) -> None:
#     repo: PrincipalGroupRepository = PrincipalGroupRepository()
#
#     with database.Session.begin() as session:
#         count, principal_groups = repo.get_all(
#             session=session, sort_col_name="name", page_number=0, page_size=100000
#         )
#         assert count == 12
#         assert all([isinstance(pg, PrincipalGroupDbo) for pg in principal_groups])
#
#
# def test_get_principal_group_members(database: Database) -> None:
#     repo: PrincipalGroupRepository = PrincipalGroupRepository()
#
#     with database.Session.begin() as session:
#         count, principal_group_members_batch1 = repo.get_principal_group_members(
#             session=session, principal_group_id=1
#         )
#         assert len(principal_group_members_batch1) == 1
#         assert count == 1
#
#         count, principal_group_members_batch2 = repo.get_principal_group_members(
#             session=session, principal_group_id=2
#         )
#         assert not any(
#             [
#                 member in principal_group_members_batch2
#                 for member in principal_group_members_batch1
#             ]
#         )
