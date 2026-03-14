from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.tourist_info import TouristInfoCreate, TouristInfoUpdate, TouristInfoResponse
from app.services.tourist_info_service import TouristInfoService

router = APIRouter(prefix="/tourist-info", tags=["Tourist Information"])
info_service = TouristInfoService()


@router.post("/", response_model=dict, status_code=201)
async def create_info(info: TouristInfoCreate):
    """Créer une information touristique"""
    info_id = await info_service.create_info(info)
    return {"id": info_id, "message": "Tourist information created"}


@router.get("/", response_model=List[TouristInfoResponse])
async def list_infos(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """Récupérer toutes les infos"""
    return await info_service.get_all_infos(skip, limit)


@router.get("/category/{categorie}", response_model=List[TouristInfoResponse])
async def get_by_category(categorie: str):
    """Récupérer les infos par catégorie"""
    return await info_service.get_info_by_category(categorie)


@router.get("/visa", response_model=TouristInfoResponse)
async def get_visa():
    """Récupérer les conditions de visa"""
    result = await info_service.get_visa_requirements()
    if not result:
        raise HTTPException(status_code=404, detail="Visa info not found")
    return result


@router.get("/culture/customs", response_model=List[TouristInfoResponse])
async def get_customs():
    """Récupérer les coutumes culturelles"""
    return await info_service.get_cultural_customs()


@router.get("/climate", response_model=TouristInfoResponse)
async def get_climate(region: str = Query(None)):
    """Récupérer les infos sur le climat"""
    result = await info_service.get_climate_info(region)
    if not result:
        raise HTTPException(status_code=404, detail="Climate info not found")
    return result


@router.get("/packing-guide", response_model=TouristInfoResponse)
async def get_packing(season: str = Query("toutes")):
    """Récupérer le guide de packing"""
    result = await info_service.get_packing_guide(season)
    if not result:
        raise HTTPException(status_code=404, detail="Packing guide not found")
    return result


@router.get("/currency", response_model=TouristInfoResponse)
async def get_currency():
    """Récupérer les infos de change"""
    result = await info_service.get_currency_exchange_info()
    if not result:
        raise HTTPException(status_code=404, detail="Currency info not found")
    return result


@router.get("/languages", response_model=TouristInfoResponse)
async def get_languages():
    """Récupérer les infos sur les langues"""
    result = await info_service.get_languages_info()
    if not result:
        raise HTTPException(status_code=404, detail="Languages info not found")
    return result


@router.get("/search", response_model=List[TouristInfoResponse])
async def search(keyword: str = Query(..., min_length=2)):
    """Rechercher des conseils utiles"""
    return await info_service.search_useful_tips(keyword)


@router.get("/{info_id}", response_model=TouristInfoResponse)
async def get_one(info_id: str):
    """Récupérer une information"""
    info = await info_service.get_info(info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Information not found")
    return info


@router.put("/{info_id}")
async def update_one(info_id: str, info: TouristInfoUpdate):
    """Mettre à jour une information"""
    success = await info_service.update_info(info_id, info)
    if not success:
        raise HTTPException(status_code=404, detail="Information not found")
    return {"message": "Information updated"}


@router.delete("/{info_id}")
async def delete_one(info_id: str):
    """Supprimer une information"""
    success = await info_service.delete_info(info_id)
    if not success:
        raise HTTPException(status_code=404, detail="Information not found")
    return {"message": "Information deleted"}
