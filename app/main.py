from typing import Union

import uvicorn
from fastapi import FastAPI

from app.api.routes.user_routes import router
from app.api.routes.user_group_routes import router as group_routers

app = FastAPI()

app.include_router(router)
app.include_router(group_routers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
