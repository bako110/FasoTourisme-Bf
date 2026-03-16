import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.services.guide_service import GuideService
from app.schemas.guide import GuideResponse
import json

async def test():
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        await client.admin.command("ping")
        print("✓ Conectado ao MongoDB")
        
        service = GuideService(db)
        guides = await service.get_all_guides(skip=0, limit=1)
        
        if guides:
            guide = guides[0]
            print("\n✓ Recuperado 1 guides")
            print(f"  - ID: {guide.get('id')}")
            print(f"  - Nome: {guide.get('nom_complet')}")
            
            # Tentar validar com Pydantic
            print("\n✓ Validando com Pydantic...")
            response = GuideResponse(**guide)
            print("✓ ✓ ✓ Pydantic validation PASSOU!")
            
            # Tentar serializar
            print("\n✓ Serializando para JSON...")
            json_data = json.dumps(response.model_dump(), default=str)
            print("✓ ✓ ✓ JSON serialization PASSOU!")
            
        else:
            print("❌ Nenhum guide encontrado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

asyncio.run(test())
