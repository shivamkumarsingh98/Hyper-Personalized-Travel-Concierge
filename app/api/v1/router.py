import importlib
import pkgutil
from fastapi import APIRouter
from app.api.v1 import endpoints

api_router = APIRouter()

for _, module_name, _ in pkgutil.iter_modules(endpoints.__path__):
    module = importlib.import_module(f"app.api.v1.endpoints.{module_name}")
    if hasattr(module, "router"):
        prefix = getattr(module, "router_prefix", f"/{module_name}")
        api_router.include_router(module.router, prefix=prefix, tags=[module_name.capitalize()])
