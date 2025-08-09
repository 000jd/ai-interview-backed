import jwt
import time
from typing import Dict, Any, Optional
from livekit.api import LiveKitAPI, CreateRoomRequest, ListRoomsRequest
from app.core.config import settings
import uuid

class LiveKitManager:
    """LiveKit integration manager"""
    
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.server_url = settings.LIVEKIT_URL
        
        if not all([self.api_key, self.api_secret, self.server_url]):
            print("⚠️  Warning: LiveKit credentials not configured")
    
    def generate_token(
        self, 
        room_name: str, 
        participant_name: str, 
        identity: Optional[str] = None,
        permissions: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate LiveKit JWT token"""
        if not identity:
            identity = f"participant_{uuid.uuid4().hex[:8]}"
        
        current_time = int(time.time())
        
        # Default permissions
        default_permissions = {
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True,
            "canPublishData": True,
            "canUpdateOwnMetadata": True
        }
        
        if permissions:
            default_permissions.update(permissions)
        
        payload = {
            "iss": self.api_key,
            "sub": identity,
            "iat": current_time,
            "exp": current_time + 7200,  # 2 hours
            "nbf": current_time,
            "name": participant_name,
            "video": {
                "room": room_name,
                **default_permissions
            }
        }
        
        token = jwt.encode(payload, self.api_secret, algorithm="HS256")
        return token
    
    async def create_room(self, room_name: str, empty_timeout: int = 300) -> bool:
        """Create LiveKit room"""
        try:
            if not self.api_key or not self.api_secret or not self.server_url:
                return False
                
            lk_api = LiveKitAPI(
                base_url=self.server_url,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
            
            create_request = CreateRoomRequest(
                name=room_name,
                empty_timeout=empty_timeout,
                max_participants=10
            )
            
            await lk_api.room.create_room(create_request)
            await lk_api.aclose()
            return True
            
        except Exception as e:
            print(f"Error creating room: {e}")
            return False
    
    async def list_rooms(self) -> list:
        """List active LiveKit rooms"""
        try:
            if not self.api_key or not self.api_secret or not self.server_url:
                return []
                
            lk_api = LiveKitAPI(
                base_url=self.server_url,
                api_key=self.api_key,
                api_secret=self.api_secret,
            )
            rooms = await lk_api.room.list_rooms(ListRoomsRequest())
            await lk_api.aclose()
            
            return [
                {
                    "name": room.name,
                    "num_participants": room.num_participants,
                    "creation_time": room.creation_time
                }
                for room in rooms.rooms
            ]
            
        except Exception as e:
            print(f"Error listing rooms: {e}")
            return []
