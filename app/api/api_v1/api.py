from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, opportunities, proposals

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["proposals"])
