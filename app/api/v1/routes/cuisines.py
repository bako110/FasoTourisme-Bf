from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.cuisine import CuisineCreate, CuisineUpdate, CuisineResponse
from app.services.cuisine_service import CuisineService

router = APIRouter(prefix="/cuisines", tags=["Local Cuisine"])
cuisine_service = CuisineService()


@router.post("/", response_model=dict, status_code=201)
async def create_restaurant(restaurant: CuisineCreate):
    """Créer un profil restaurant"""
    restaurant_id = await cuisine_service.create_cuisine(restaurant)
    return {"id": restaurant_id, "message": "Restaurant registered"}


@router.get("/", response_model=List[CuisineResponse])
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les restaurants"""
    return await cuisine_service.get_all_cuisines(skip, limit)


@router.get("/type/{type_cuisine}", response_model=List[CuisineResponse])
async def get_by_type(type_cuisine: str):
    """Récupérer les restaurants par type de cuisine"""
    return await cuisine_service.get_cuisines_by_type(type_cuisine)


@router.get("/city/{ville}", response_model=List[CuisineResponse])
async def get_by_city(ville: str):
    """Récupérer les restaurants d'une ville"""
    return await cuisine_service.get_cuisines_by_city(ville)


@router.get("/traditional", response_model=List[CuisineResponse])
async def get_traditional():
    """Récupérer les restaurants cuisines traditionnelles"""
    return await cuisine_service.get_traditional_cuisines()


@router.get("/bio-local", response_model=List[CuisineResponse])
async def get_bio_local():
    """Récupérer les restaurants avec produits bio/locaux"""
    return await cuisine_service.get_bio_local_cuisines()


@router.get("/top-rated", response_model=List[CuisineResponse])
async def get_top_rated():
    """Récupérer les restaurants les mieux notés"""
    return await cuisine_service.get_top_rated_cuisines()


@router.get("/{cuisine_id}", response_model=CuisineResponse)
async def get_one(cuisine_id: str):
    """Récupérer un restaurant"""
    restaurant = await cuisine_service.get_cuisine(cuisine_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{cuisine_id}")
async def update_one(cuisine_id: str, restaurant: CuisineUpdate):
    """Mettre à jour un profil restaurant"""
    success = await cuisine_service.update_cuisine(cuisine_id, restaurant)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant profile updated"}


@router.delete("/{cuisine_id}")
async def delete_one(cuisine_id: str):
    """Supprimer un profil restaurant"""
    success = await cuisine_service.delete_cuisine(cuisine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant profile deleted"}
