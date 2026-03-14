from fastapi import APIRouter, HTTPException, Query, Path
from typing import List
from app.schemas.roads import RoadCreate, RoadUpdate, RoadResponse
from app.services.roads_service import RoadService

router = APIRouter(prefix="/roads", tags=["Road Conditions"])
road_service = RoadService()


@router.post("/", response_model=dict, status_code=201)
async def create_condition(condition: RoadCreate):
    """Créer un report routier"""
    condition_id = await road_service.create_condition(condition)
    return {"id": condition_id, "message": "Road condition reported"}


@router.get("/", response_model=List[RoadResponse])
async def list_conditions(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer tous les rapports routiers"""
    return await road_service.get_all_conditions(skip, limit)


@router.get("/dangerous", response_model=List[RoadResponse])
async def get_dangerous():
    """Récupérer les ROUTES DANGEREUSES"""
    return await road_service.get_dangerous_routes()


@router.get("/safe", response_model=List[RoadResponse])
async def get_safe():
    """Récupérer les meilleures routes sûres"""
    return await road_service.get_best_safe_routes()


@router.get("/route", response_model=List[RoadResponse])
async def get_route(from_city: str = Query(...), to_city: str = Query(...)):
    """Récupérer les conditions entre deux villes"""
    return await road_service.get_routes_by_from_to(from_city, to_city)


@router.get("/accidents", response_model=List[RoadResponse])
async def get_with_accidents():
    """Récupérer les routes avec historique d'accidents"""
    return await road_service.get_routes_with_accidents()


@router.get("/surface/{surface_type}", response_model=List[RoadResponse])
async def get_by_surface(surface_type: str):
    """Récupérer les routes par type de surface"""
    return await road_service.get_routes_by_surface_type(surface_type)


@router.get("/banditry/{heure}", response_model=List[RoadResponse])
async def get_banditry_risks(heure: int = Path(..., ge=0, le=23)):
    """Récupérer les risques de banditisme pour une heure"""
    return await road_service.get_banditry_risks_by_hour(heure)


@router.get("/{condition_id}", response_model=RoadResponse)
async def get_one(condition_id: str):
    """Récupérer un report routier"""
    condition = await road_service.get_condition(condition_id)
    if not condition:
        raise HTTPException(status_code=404, detail="Road condition not found")
    return condition


@router.put("/{condition_id}")
async def update_one(condition_id: str, condition: RoadUpdate):
    """Mettre à jour un report"""
    success = await road_service.update_condition(condition_id, condition)
    if not success:
        raise HTTPException(status_code=404, detail="Road condition not found")
    return {"message": "Road condition updated"}


@router.delete("/{condition_id}")
async def delete_one(condition_id: str):
    """Supprimer un report"""
    success = await road_service.delete_condition(condition_id)
    if not success:
        raise HTTPException(status_code=404, detail="Road condition not found")
    return {"message": "Road condition deleted"}
