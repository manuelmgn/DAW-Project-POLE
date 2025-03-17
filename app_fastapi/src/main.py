"""Aplicación"""

from fastapi import FastAPI
import uvicorn

from users.router import router as user_router
from user_logs.router import router as logs_router
from auth.router import router as auth_router
from pollens.router import router as pollen_router
from external_apis.router import router as externals_router
from database.database import init_db

app = FastAPI()

# Inicio da base de datos
init_db()

# Rexistro dos routers de cada módulo
app.include_router(user_router, prefix="/user")
app.include_router(logs_router, prefix="/userlogs")
app.include_router(auth_router, prefix="/auth")
app.include_router(pollen_router, prefix="/pollen-types")
app.include_router(externals_router, prefix="/external-apis")
# app.include_router(logs_router, prefix="/calculations")

DEBUG = True

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
