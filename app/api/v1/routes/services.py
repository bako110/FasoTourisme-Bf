from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.services import EssentialServiceCreate, EssentialServiceUpdate, EssentialServiceResponse
from app.services.services_service import EssentialServiceService

router = APIRouter(prefix="/essential-services", tags=["Essential Services"])
service = EssentialServiceService()


@router.post("/", response_model=dict, status_code=201)
async def create_service(svc: EssentialServiceCreate):
    """Créer un service essentiel"""
    service_id = await service.create_service(svc)
    return {"id": service_id, "message": "Service created"}


@router.get("/", response_model=List[EssentialServiceResponse])
async def list_services(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les services"""
    return await service.get_all_services(skip, limit)


@router.get("/type/{type_service}", response_model=List[EssentialServiceResponse])
async def get_by_type(type_service: str):
    """Récupérer les services par type (eau, électricité, etc)"""
    return await service.get_services_by_type(type_service)


@router.get("/city/{ville}", response_model=List[EssentialServiceResponse])
async def get_by_city(ville: str):
    """Récupérer les services d'une ville"""
    return await service.get_services_by_city(ville)


@router.get("/internet/{ville}/reliable", response_model=List[EssentialServiceResponse])
async def get_reliable_internet(ville: str):
    """Récupérer les fournisseurs internet fiables"""
    return await service.get_reliable_internet_providers(ville)


@router.get("/water/{ville}", response_model=EssentialServiceResponse)
async def get_water(ville: str):
    """Récupérer les infos sur l'eau"""
    result = await service.get_water_info(ville)
    if not result:
        raise HTTPException(status_code=404, detail="Water info not found")
    return result


@router.get("/electricity/{ville}", response_model=EssentialServiceResponse)
async def get_electricity(ville: str):
    """Récupérer la stabilité électrique"""
    result = await service.get_electricity_stability(ville)
    if not result:
        raise HTTPException(status_code=404, detail="Electricity info not found")
    return result


@router.get("/banking/{ville}", response_model=List[EssentialServiceResponse])
async def get_banking(ville: str):
    """Récupérer les emplacements bancaires"""
    return await service.get_banking_locations(ville)


@router.get("/{service_id}", response_model=EssentialServiceResponse)
async def get_one(service_id: str):
    """Récupérer un service"""
    result = await service.get_service(service_id)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@router.put("/{service_id}")
async def update_one(service_id: str, svc: EssentialServiceUpdate):
    """Mettre à jour un service"""
    success = await service.update_service(service_id, svc)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service updated"}


@router.delete("/{service_id}")
async def delete_one(service_id: str):
    """Supprimer un service"""
    success = await service.delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted"}
