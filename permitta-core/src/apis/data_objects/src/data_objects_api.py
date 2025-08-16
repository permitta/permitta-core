from dataclasses import asdict

from app_logger import Logger, get_logger
from flask import Blueprint, Response, g, jsonify, make_response

logger: Logger = get_logger("api.data_objects")

bp = Blueprint("data_objects_api_v1", __name__, url_prefix="/api/v1/data-objects")

TABLES_SORT_KEY: str = "tables.table_name"
SCHEMAS_SORT_KEY: str = "schemas.schema_name"
SCOPE_TABLES: str = "tables"
SCOPE_SCHEMAS: str = "schemas"


@bp.route("/tables", methods=["GET"])
def index_tables():
    logged_in_user: str = None

    query_function = DataObjectsController.get_tables_paginated_with_access

    with g.database.Session.begin() as session:
        table_count, tables = query_function(
            session=session,
            logged_in_user=logged_in_user,
            sort_col_name=TABLES_SORT_KEY,
            page_number=0,
            page_size=50,
            search_term="",
            attributes=None,
        )

        response: Response = make_response(
            jsonify(tables=[asdict(table) for table in tables], total_count=table_count)
        )

        response.headers.set("Access-Control-Allow-Origin", "*")
    return response
