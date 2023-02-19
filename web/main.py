from app_auth.router import rout_auth
from app_auth.updated_auth import UpdatedAuthJWT
from app_cash.router import rout_cash
from config import Settings, origins, server, static
from exceptions import authjwt_exception_handler, custom_http_exception_handler
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.exceptions import HTTPException

app = FastAPI(
    title="Project Alpha",
    version="0.0.1",
    contact={
        "name": "Andrey Butakov",
        "email": "6669.butakov@gmail.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    # prefix распространяется на все роуты и документацию
    # root_path="/web",
)

# static
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# templates
def get_templates() -> Jinja2Templates:
    templates = Jinja2Templates(directory="templates/")
    templates.env.globals["static"] = static
    templates.env.globals["server"] = server
    return templates


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()


@app.get("/", status_code=200, response_class=HTMLResponse)
async def home(request: Request, Authorize: UpdatedAuthJWT = Depends()):
    try:
        Authorize.jwt_optional()
    except AuthJWTException:
        context = {"request": request}
        response = get_templates().TemplateResponse(
            "home.html",
            context,
        )
        return response
    current_user = Authorize.get_jwt_subject() or None
    context = {"request": request, "user": current_user}
    response = get_templates().TemplateResponse(
        "home.html",
        context,
    )
    return response


app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(rout_auth)
app.include_router(rout_cash)
