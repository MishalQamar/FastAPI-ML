from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Use package-relative imports so the app can be imported
# reliably regardless of how the project is executed.
from .api import routes_auth, routes_predict
from .middleware.logging_middleware import LoggingMiddleware
from .core.exceptions import register_exception_handlers
from .core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(LoggingMiddleware)

app.include_router(routes_auth.router,tags=['Auth'])
app.include_router(routes_predict.router,tags=['Predict'])


Instrumentator().instrument(app).expose(app)

register_exception_handlers(app)