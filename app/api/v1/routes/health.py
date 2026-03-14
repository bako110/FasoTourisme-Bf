from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.schemas.health import HealthCreate, HealthUpdate, HealthResponse
from app.services.health_service import HealthService

router = APIRouter(prefix="/health-facilities", tags=["Health Facilities"])
health_service = HealthService()


@router.post("/", response_model=dict, status_code=201)
async def create_facility(facility: HealthCreate):
    """Créer une structure sanitaire"""
    facility_id = await health_service.create_facility(facility)
    return {"id": facility_id, "message": "Facility created successfully"}


@router.get("/", response_model=List[HealthResponse])
async def list_facilities(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer toutes les structures sanitaires"""
    return await health_service.get_all_facilities(skip, limit)


@router.get("/pharmacies", response_model=List[HealthResponse])
async def get_pharmacies():
    """Récupérer toutes les pharmacies"""
    return await health_service.get_pharmacies()


@router.get("/emergency", response_model=List[HealthResponse])
async def get_emergency_facilities():
    """Récupérer les structures avec urgences 24h"""
    return await health_service.get_emergency_facilities()


@router.get("/city/{ville}", response_model=List[HealthResponse])
async def get_by_city(ville: str):
    """Récupérer les structures d'une ville"""
    return await health_service.get_facilities_by_city(ville)


@router.get("/near", response_model=List[HealthResponse])
async def get_near_location(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(5, ge=1, le=50)
):
    """Trouver les structures proches d'une localisation"""
    return await health_service.get_facilities_near_location(latitude, longitude, radius_km)


@router.get("/{facility_id}", response_model=HealthResponse)
async def get_facility(facility_id: str):
    """Récupérer une structure sanitaire"""
    facility = await health_service.get_facility(facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


@router.put("/{facility_id}")
async def update_facility(facility_id: str, facility: HealthUpdate):
    """Mettre à jour une structure"""
    success = await health_service.update_facility(facility_id, facility)
    if not success:
        raise HTTPException(status_code=404, detail="Facility not found")
    return {"message": "Facility updated successfully"}


@router.post("/{facility_id}/verify")
async def verify_facility(facility_id: str):
    """Vérifier une structure (ADMIN)"""
    success = await health_service.verify_facility(facility_id)
    if not success:
        raise HTTPException(status_code=404, detail="Facility not found")
    return {"message": "Facility verified"}


@router.delete("/{facility_id}")
async def delete_facility(facility_id: str):
    """Supprimer une structure"""
    success = await health_service.delete_facility(facility_id)
    if not success:
        raise HTTPException(status_code=404, detail="Facility not found")
    return {"message": "Facility deleted"}
