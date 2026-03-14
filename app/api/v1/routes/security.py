from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.schemas.security import SecurityCreate, SecurityUpdate, SecurityResponse
from app.services.security_service import SecurityService

router = APIRouter(prefix="/security-alerts", tags=["Security Alerts"])
security_service = SecurityService()


@router.post("/", response_model=dict, status_code=201)
async def create_alert(alert: SecurityCreate):
    """Créer une alerte de sécurité (CRITIQUE)"""
    alert_id = await security_service.create_alert(alert)
    return {"id": alert_id, "message": "Alert created - Awaiting verification"}


@router.get("/", response_model=List[SecurityResponse])
async def list_alerts(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer toutes les alertes"""
    return await security_service.get_all_alerts(skip, limit)


@router.get("/active", response_model=List[SecurityResponse])
async def get_active_alerts():
    """Récupérer les alertes ACTIVES (temps réel)"""
    return await security_service.get_active_alerts()


@router.get("/high-risk", response_model=List[SecurityResponse])
async def get_high_risk_alerts():
    """Récupérer les alertes à HAUT RISQUE"""
    return await security_service.get_high_risk_alerts()


@router.get("/region/{region}", response_model=List[SecurityResponse])
async def get_by_region(region: str):
    """Récupérer les alertes d'une région"""
    return await security_service.get_alerts_by_region(region)


@router.get("/reliable-sources", response_model=List[SecurityResponse])
async def get_reliable_sources(min_score: float = Query(0.7, ge=0, le=1)):
    """Récupérer les alertes de sources fiables"""
    return await security_service.get_alerts_by_source_reliability(min_score)


@router.get("/{alert_id}", response_model=SecurityResponse)
async def get_alert(alert_id: str):
    """Récupérer une alerte"""
    alert = await security_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}")
async def update_alert(alert_id: str, alert: SecurityUpdate):
    """Mettre à jour une alerte"""
    success = await security_service.update_alert(alert_id, alert)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert updated"}


@router.post("/{alert_id}/verify")
async def verify_alert(alert_id: str, verified_by: str = Query(...)):
    """Vérifier une alerte (ADMIN - MODÉRATION CRITIQUE)"""
    success = await security_service.verify_alert(alert_id, verified_by)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert verified and published"}


@router.post("/{alert_id}/deactivate")
async def deactivate_alert(alert_id: str, raison: str = Query(...)):
    """Désactiver une alerte (situation résolue)"""
    success = await security_service.deactivate_alert(alert_id, raison)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deactivated"}


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    """Supprimer une alerte"""
    success = await security_service.delete_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted"}
