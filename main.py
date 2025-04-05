from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import router as user_router
from app.routers.store import router as store_router
from app.routers.category import router as category_router

app = FastAPI()

# Добавление CORS middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Это сервер приложения YummyYummy!"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(store_router, prefix="/store", tags=["Store"])
app.include_router(category_router, prefix="/category", tags=["Category"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8080, reload=True, ssl_keyfile="key.pem", ssl_certfile="cert.pem")