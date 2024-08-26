from fastapi import FastAPI

from src.backend.routers.router_unicorn import router as router_unicorn

app = FastAPI()
app.include_router(router=router_unicorn)


@app.get("/health", tags=["health check"])
async def root() -> dict[str, str]:
    return {"status": "ON"}
