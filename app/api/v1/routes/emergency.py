from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.emergency import EmergencyCreate, EmergencyUpdate, EmergencyResponse
from app.services.emergency_service import EmergencyServiceService

router = APIRouter(prefix="/emergency-services", tags=["Emergency Services"])
service = EmergencyServiceService()


@router.post("/", response_model=dict, status_code=201)
async def create_service(svc: EmergencyCreate):
    """Créer un service d'urgence"""
    service_id = await service.create_service(svc)
    return {"id": service_id, "message": "Emergency service created"}


@router.get("/", response_model=List[EmergencyResponse])
async def list_services(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les services"""
    return await service.get_all_services(skip, limit)


@router.get("/operational", response_model=List[EmergencyResponse])
async def get_operational():
    """Récupérer les services opérationnels"""
    return await service.get_operational_services()


@router.get("/type/{type_service}", response_model=List[EmergencyResponse])
async def get_by_type(type_service: str):
    """Récupérer les services par type (police, ambulance, pompiers)"""
    return await service.get_services_by_type(type_service)


@router.get("/region/{region}", response_model=List[EmergencyResponse])
async def get_by_region(region: str):
    """Récupérer les services d'une région"""
    return await service.get_services_by_region(region)


@router.get("/fastest/{type_service}", response_model=EmergencyResponse)
async def get_fastest(type_service: str):
    """Récupérer le service avec temps de réponse le plus court"""
    result = await service.get_fastest_response(type_service)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@router.get("/{service_id}", response_model=EmergencyResponse)
async def get_one(service_id: str):
    """Récupérer un service"""
    result = await service.get_service(service_id)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result


@router.put("/{service_id}")
async def update_one(service_id: str, svc: EmergencyUpdate):
    """Mettre à jour un service"""
    success = await service.update_service(service_id, svc)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service updated"}


@router.post("/{service_id}/response-time")
async def update_response_time(service_id: str, minutes: int = Query(..., ge=1, le=300)):
    """Mettre à jour le temps de réponse moyen"""
    success = await service.update_response_time(service_id, minutes)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": f"Response time updated to {minutes} minutes"}


@router.delete("/{service_id}")
async def delete_one(service_id: str):
    """Supprimer un service"""
    success = await service.delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted"}
