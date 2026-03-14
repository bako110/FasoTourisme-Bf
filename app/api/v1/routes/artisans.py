from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.artisan import ArtisanCreate, ArtisanUpdate, ArtisanResponse
from app.services.artisan_service import ArtisanService

router = APIRouter(prefix="/artisans", tags=["Local Artisans"])
artisan_service = ArtisanService()


@router.post("/", response_model=dict, status_code=201)
async def create_artisan(artisan: ArtisanCreate):
    """Créer un profil artisan"""
    artisan_id = await artisan_service.create_artisan(artisan)
    return {"id": artisan_id, "message": "Artisan registered"}


@router.get("/", response_model=List[ArtisanResponse])
async def list_artisans(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les artisans"""
    return await artisan_service.get_all_artisans(skip, limit)


@router.get("/craft/{type_metier}", response_model=List[ArtisanResponse])
async def get_by_craft(type_metier: str):
    """Récupérer les artisans par métier"""
    return await artisan_service.get_artisans_by_craft(type_metier)


@router.get("/city/{ville}", response_model=List[ArtisanResponse])
async def get_by_city(ville: str):
    """Récupérer les artisans d'une ville"""
    return await artisan_service.get_artisans_by_city(ville)


@router.get("/certified", response_model=List[ArtisanResponse])
async def get_certified():
    """Récupérer les artisans certifiés"""
    return await artisan_service.get_certified_artisans()


@router.get("/top-rated", response_model=List[ArtisanResponse])
async def get_top_rated():
    """Récupérer les artisans les mieux notés"""
    return await artisan_service.get_top_rated_artisans()


@router.get("/{artisan_id}", response_model=ArtisanResponse)
async def get_one(artisan_id: str):
    """Récupérer un artisan"""
    artisan = await artisan_service.get_artisan(artisan_id)
    if not artisan:
        raise HTTPException(status_code=404, detail="Artisan not found")
    return artisan


@router.put("/{artisan_id}")
async def update_one(artisan_id: str, artisan: ArtisanUpdate):
    """Mettre à jour un profil artisan"""
    success = await artisan_service.update_artisan(artisan_id, artisan)
    if not success:
        raise HTTPException(status_code=404, detail="Artisan not found")
    return {"message": "Artisan profile updated"}


@router.delete("/{artisan_id}")
async def delete_one(artisan_id: str):
    """Supprimer un profil artisan"""
    success = await artisan_service.delete_artisan(artisan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Artisan not found")
    return {"message": "Artisan profile deleted"}
