from fastapi import APIRouter, Request
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
    get_redoc_html
)
from starlette.responses import HTMLResponse

from app.core.config import settings

router = APIRouter(include_in_schema=False)

@router.get("/docs")
async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = f"{root_path}/openapi.json"

    if settings.DOCS_OFFLINE:
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=f"{settings.PROJECT_NAME} - Swagger UI",
            oauth2_redirect_url = f"{root_path}/docs/oauth2_redirect",
            swagger_js_url=f"{root_path}/static/docs/swagger-ui-bundle.js",
            swagger_css_url=f"{root_path}/static/docs/swagger-ui.css",
            swagger_favicon_url=f"{root_path}/static/docs/favicon.ico",
        )

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        oauth2_redirect_url=f"{root_path}/docs/oauth2_redirect",
    )

@router.get("/docs/oauth2-redirect")
async def swagger_ui_redirect(request: Request) -> HTMLResponse:
    return get_swagger_ui_oauth2_redirect_html()

@router.get("/redoc")
async def custom_redoc_html(request: Request) -> HTMLResponse:
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = f"{root_path}/openapi.json"

    if settings.DOCS_OFFLINE:
        return get_redoc_html(
            openapi_url=openapi_url,
            title=f"{settings.PROJECT_NAME} - Swagger UI",
            redoc_js_url=f"{root_path}/static/docs/redoc.standalone.js",
            redoc_favicon_url=f"{root_path}/static/docs/favicon.ico",
        )

    return get_redoc_html(
        openapi_url=openapi_url,
        title=f"{settings.PROJECT_NAME} - ReDoc",
    )