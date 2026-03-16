import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.services.guide_service import GuideService

async def test():
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        await client.admin.command("ping")
        print("✓ Connected to MongoDB")
        
        # Pass the database as parameter
        service = GuideService(db)
        guides = await service.get_all_guides(skip=0, limit=5)
        print(f"✓ Retrieved {len(guides)} guides")
        
        if guides:
            for i, guide in enumerate(guides[:2]):
                bio = guide.get("bio", "")
                bio_preview = bio[:50] + "..." if len(bio) > 50 else bio
                print(f"  {i+1}. {guide.get('nom_complet')}: {bio_preview}")
        else:
            print("No guides found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

asyncio.run(test())
