from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.tourist_info import TouristInfo
from app.schemas.tourist_info import TouristInfoCreate, TouristInfoUpdate
from app.core.database import get_database


class TouristInfoService:
    
    def __init__(self):
        self.collection_name = "tourist_info"

    async def create_info(self, info: TouristInfoCreate) -> str:
        """Créer une information touristique/pratique"""
        db = get_database()
        info_dict = info.model_dump()
        info_dict["date_creation"] = datetime.utcnow()
        info_dict["date_modification"] = datetime.utcnow()
        result = await db[self.collection_name].insert_one(info_dict)
        return str(result.inserted_id)

    async def get_info(self, info_id: str) -> Dict[str, Any] | None:
        """Récupérer une information"""
        db = get_database()
        try:
            obj_id = ObjectId(info_id)
            info = await db[self.collection_name].find_one({"_id": obj_id})
            if info:
                info["_id"] = str(info["_id"])
            return info
        except:
            return None

    async def get_all_infos(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer toutes les informations"""
        db = get_database()
        infos = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**i, "_id": str(i["_id"])} for i in infos]

    async def update_info(self, info_id: str, info: TouristInfoUpdate) -> bool:
        """Mettre à jour une information"""
        db = get_database()
        try:
            obj_id = ObjectId(info_id)
            update_dict = info.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_info(self, info_id: str) -> bool:
        """Supprimer une information"""
        db = get_database()
        try:
            obj_id = ObjectId(info_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_info_by_category(self, categorie: str) -> List[Dict[str, Any]]:
        """Récupérer les infos par catégorie (visa, coutumes, etc)"""
        db = get_database()
        infos = await db[self.collection_name].find({"categorie": categorie}).to_list(None)
        return [{**i, "_id": str(i["_id"])} for i in infos]

    async def get_visa_requirements(self) -> Dict[str, Any] | None:
        """Récupérer les conditions de visa"""
        db = get_database()
        info = await db[self.collection_name].find_one({"categorie": "visa"})
        if info:
            info["_id"] = str(info["_id"])
        return info

    async def get_cultural_customs(self) -> List[Dict[str, Any]]:
        """Récupérer les coutumes culturelles"""
        db = get_database()
        infos = await db[self.collection_name].find({"categorie": "coutumes"}).to_list(None)
        return [{**i, "_id": str(i["_id"])} for i in infos]

    async def get_climate_info(self, region: str = None) -> Dict[str, Any] | None:
        """Récupérer les infos sur le climat"""
        db = get_database()
        query = {"categorie": "climat"}
        if region:
            query["region"] = region
        info = await db[self.collection_name].find_one(query)
        if info:
            info["_id"] = str(info["_id"])
        return info

    async def get_packing_guide(self, season: str = "toutes") -> Dict[str, Any] | None:
        """Récupérer le guide de packing"""
        db = get_database()
        query = {"categorie": "packing"}
        if season != "toutes":
            query["saison"] = season
        info = await db[self.collection_name].find_one(query)
        if info:
            info["_id"] = str(info["_id"])
        return info

    async def get_currency_exchange_info(self) -> Dict[str, Any] | None:
        """Récupérer les infos de change de devises"""
        db = get_database()
        info = await db[self.collection_name].find_one({"categorie": "devise"})
        if info:
            info["_id"] = str(info["_id"])
        return info

    async def get_languages_info(self) -> Dict[str, Any] | None:
        """Récupérer les infos sur les langues"""
        db = get_database()
        info = await db[self.collection_name].find_one({"categorie": "langues"})
        if info:
            info["_id"] = str(info["_id"])
        return info

    async def search_useful_tips(self, keyword: str) -> List[Dict[str, Any]]:
        """Rechercher des conseils utiles par mot-clé"""
        db = get_database()
        infos = await db[self.collection_name].find({
            "$text": {"$search": keyword}
        }).to_list(None)
        return [{**i, "_id": str(i["_id"])} for i in infos]
