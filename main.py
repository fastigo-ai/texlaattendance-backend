from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_routes
from routes import visit_routes
from routes import leave_routes
from routes import admin_routes

app = FastAPI(title="Texla Visit Tracking API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(visit_routes.router, prefix="/api/visits")
app.include_router(leave_routes.router, prefix="/api/leave")
app.include_router(admin_routes.router, prefix="/api/admin")


@app.get("/")
def root():
    return {"message": "Texla Visit Tracking API Running"}