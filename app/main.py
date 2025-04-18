import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.routes.post_routes import router as post_routes
from app.api.routes.user_group_routes import router as group_routes
from app.api.routes.user_routes import router as user_routes
from app.api.websockets.post_websockets import router as post_websockets


app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI application",
        version="1.0.0",
        description="JWT Authentication and Authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "name": "Authorization",
            "type": "apiKey",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "in": "header",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(user_routes)
app.include_router(group_routes)
app.include_router(post_routes)
app.include_router(post_websockets)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
