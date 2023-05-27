import uvicorn
from fastapi import FastAPI

from app.api.routes.post_routes import router as post_routes
from app.api.routes.user_group_routes import router as group_routes
from app.api.routes.user_routes import router as user_routes
from app.api.websockets.post_websockets import router as post_websockets

app = FastAPI()

app.include_router(user_routes)
app.include_router(group_routes)
app.include_router(post_routes)
app.include_router(post_websockets)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
