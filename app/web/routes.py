from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates")

web_router = APIRouter(include_in_schema=False)


@web_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Root page of the web interface
    """
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "GovBid Pro"}
    )


@web_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Dashboard page
    """
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "title": "Dashboard - GovBid Pro"}
    )


@web_router.get("/opportunities", response_class=HTMLResponse)
async def opportunities_page(request: Request):
    """
    Opportunities listing page
    """
    return templates.TemplateResponse(
        "opportunities.html", {"request": request, "title": "Opportunities - GovBid Pro"}
    )


@web_router.get("/proposals", response_class=HTMLResponse)
async def proposals_page(request: Request):
    """
    Proposals listing page
    """
    return templates.TemplateResponse(
        "proposals.html", {"request": request, "title": "Proposals - GovBid Pro"}
    )


@web_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Login page
    """
    return templates.TemplateResponse(
        "login.html", {"request": request, "title": "Login - GovBid Pro"}
    )
