# import inspect
# from typing import Tuple, Type
#
# from database import Database
# from models import (
#     PrincipalAttributeDbo,
#     PrincipalDbo,
#     # PrincipalGroupDbo,
# )
# from sqlalchemy import Row, and_
# from sqlalchemy.orm import Query
# from sqlalchemy.sql.elements import NamedColumn
#
# from .repository_base import RepositoryBase
#
#
# class PrincipalGroupRepository(RepositoryBase):
#
#     @staticmethod
#     def get_all(
#         session,
#         sort_col_name: str,
#         page_number: int,
#         page_size: int,
#         sort_ascending: bool = True,
#         search_term: str = "",
#     ) -> Tuple[int, list[PrincipalGroupDbo]]:
#         return RepositoryBase._get_all_with_search_and_pagination(
#             model=PrincipalGroupDbo,
#             session=session,
#             sort_col_name=sort_col_name,
#             page_number=page_number,
#             page_size=page_size,
#             sort_ascending=sort_ascending,
#             search_term=search_term,
#             search_column_names=["name"],
#         )
#
#     @staticmethod
#     def get_principal_group_by_id(
#         session, principal_group_id: int
#     ) -> PrincipalGroupDbo:
#         principal_group: PrincipalGroupDbo = (
#             session.query(PrincipalGroupDbo)
#             .filter(PrincipalGroupDbo.principal_group_id == principal_group_id)
#             .first()
#         )
#         return principal_group
#
#     @staticmethod
#     def get_principal_group_members(
#         session, principal_group_id: int
#     ) -> Tuple[int, list[PrincipalDbo]]:
#         query: Query = (
#             session.query(PrincipalDbo)
#             .join(PrincipalAttributeDbo)
#             .join(
#                 PrincipalGroupDbo,
#                 and_(
#                     PrincipalGroupDbo.membership_attribute_key
#                     == PrincipalAttributeDbo.attribute_key,
#                     PrincipalGroupDbo.membership_attribute_value
#                     == PrincipalAttributeDbo.attribute_value,
#                 ),
#             )
#             .filter(PrincipalGroupDbo.principal_group_id == principal_group_id)
#             .order_by(PrincipalDbo.last_name)
#         )
#         return query.count(), query.all()
