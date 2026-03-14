from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.health_advisory import HealthAdvisoryCreate, HealthAdvisoryUpdate, HealthAdvisoryResponse
from app.services.health_advisory_service import HealthAdvisoryService

router = APIRouter(prefix="/health-advisories", tags=["Health Advisories"])
advisory_service = HealthAdvisoryService()


@router.post("/", response_model=dict, status_code=201)
async def create_advisory(advisory: HealthAdvisoryCreate):
    """Créer un conseil ou alerte sanitaire"""
    advisory_id = await advisory_service.create_advisory(advisory)
    return {"id": advisory_id, "message": "Health advisory created"}


@router.get("/", response_model=List[HealthAdvisoryResponse])
async def list_advisories(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les conseils sanitaires"""
    return await advisory_service.get_all_advisories(skip, limit)


@router.get("/active", response_model=List[HealthAdvisoryResponse])
async def get_active():
    """Récupérer les conseils ACTIFS"""
    return await advisory_service.get_active_advisories()


@router.get("/epidemics", response_model=List[HealthAdvisoryResponse])
async def get_epidemics():
    """Récupérer les alertes sur les épidémies"""
    return await advisory_service.get_epidemics()


@router.get("/vaccinations", response_model=List[HealthAdvisoryResponse])
async def get_vaccinations():
    """Récupérer les exigences de vaccination"""
    return await advisory_service.get_vaccination_requirements()


@router.get("/endemic-diseases", response_model=List[HealthAdvisoryResponse])
async def get_endemic(region: str = Query(None)):
    """Récupérer les maladies endémiques"""
    return await advisory_service.get_endemic_diseases(region)


@router.get("/high-risk", response_model=List[HealthAdvisoryResponse])
async def get_high_risk():
    """Récupérer les conseils à haut risque"""
    return await advisory_service.get_high_risk_advisories()


@router.get("/region/{region}", response_model=List[HealthAdvisoryResponse])
async def get_by_region(region: str):
    """Récupérer les conseils d'une région"""
    return await advisory_service.get_advisories_by_region(region)


@router.get("/{advisory_id}", response_model=HealthAdvisoryResponse)
async def get_one(advisory_id: str):
    """Récupérer un conseil sanitaire"""
    advisory = await advisory_service.get_advisory(advisory_id)
    if not advisory:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return advisory


@router.put("/{advisory_id}")
async def update_one(advisory_id: str, advisory: HealthAdvisoryUpdate):
    """Mettre à jour un conseil"""
    success = await advisory_service.update_advisory(advisory_id, advisory)
    if not success:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return {"message": "Advisory updated"}


@router.post("/{advisory_id}/deactivate")
async def deactivate(advisory_id: str, raison: str = Query(...)):
    """Désactiver un conseil (situation résolue)"""
    success = await advisory_service.deactivate_advisory(advisory_id, raison)
    if not success:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return {"message": "Advisory deactivated"}


@router.delete("/{advisory_id}")
async def delete_one(advisory_id: str):
    """Supprimer un conseil"""
    success = await advisory_service.delete_advisory(advisory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advisory not found")
    return {"message": "Advisory deleted"}
