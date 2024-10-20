from fastapi import FastAPI

from src.config import settings
from src.setup_app import include_routers, add_exepton_handlers


app = FastAPI(
    title=settings.project.title,
    version=settings.project.version,
    description=settings.project.description,
    debug=settings.project.debug,
)


include_routers(app)
add_exepton_handlers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
