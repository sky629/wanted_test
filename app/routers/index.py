from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()


@router.get("/docs", include_in_schema=True)
def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger Documentation")
