from fastapi import FastAPI, APIRouter
import uvicorn
from api.discipline import dis_router


app = FastAPI(
    title="Test FastAPI application"
)

main_router = APIRouter()

main_router.include_router(dis_router, prefix="/discipline", tags=["discipline"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)