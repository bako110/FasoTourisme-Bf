"""
Role-based access control and permissions management for Tourisme API
"""
from fastapi import HTTPException, status
from app.models.user import UserRole
from app.schemas.auth import TokenPayload
from typing import List, Callable


class Permission:
    """Permission checks for different roles"""
    
    @staticmethod
    def check_admin(current_user: TokenPayload):
        """Verify user is ADMIN"""
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        return True
    
    @staticmethod
    def check_provider(current_user: TokenPayload):
        """Verify user is PROVIDER"""
        if current_user.role != UserRole.PROVIDER and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux providers"
            )
        return True
    
    @staticmethod
    def check_guide(current_user: TokenPayload):
        """Verify user is GUIDE"""
        if current_user.role != UserRole.GUIDE and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux guides"
            )
        return True
    
    @staticmethod
    def check_moderator(current_user: TokenPayload):
        """Verify user is MODERATOR or ADMIN"""
        if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux modérateurs"
            )
        return True
    
    @staticmethod
    def check_tourist(current_user: TokenPayload):
        """Verify user is TOURIST"""
        if current_user.role != UserRole.TOURIST and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux touristes"
            )
        return True
    
    @staticmethod
    def check_any_role(current_user: TokenPayload, allowed_roles: List[UserRole]):
        """Check if user has any of the allowed roles"""
        if current_user.role not in allowed_roles and current_user.role != UserRole.ADMIN:
            allowed_str = ", ".join([r.value for r in allowed_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé aux rôles: {allowed_str}"
            )
        return True


class AdminView:
    """Admin global views - admin can see everything"""
    
    @staticmethod
    def can_view_all(current_user: TokenPayload) -> bool:
        """Admin can view all data"""
        return current_user.role == UserRole.ADMIN
    
    @staticmethod
    def can_manage_users(current_user: TokenPayload) -> bool:
        """Admin can manage all users"""
        return current_user.role == UserRole.ADMIN
    
    @staticmethod
    def can_moderate_content(current_user: TokenPayload) -> bool:
        """Admin and Moderator can moderate"""
        return current_user.role in [UserRole.ADMIN, UserRole.MODERATOR]
    
    @staticmethod
    def can_verify_providers(current_user: TokenPayload) -> bool:
        """Only Admin can verify providers"""
        return current_user.role == UserRole.ADMIN


class DataFilter:
    """Filter data based on user role"""
    
    @staticmethod
    def filter_for_role(data: dict, current_user: TokenPayload) -> dict:
        """
        Filter sensitive data based on user role
        Admin sees everything, other roles have limited visibility
        """
        if current_user.role == UserRole.ADMIN:
            return data
        
        # Remove admin-specific fields for non-admin users
        if isinstance(data, dict):
            filtered = data.copy()
            sensitive_fields = ["_owner_notes", "_internal_flags", "_admin_tags"]
            for field in sensitive_fields:
                filtered.pop(field, None)
            return filtered
        
        return data
    
    @staticmethod
    def filter_list_for_role(items: list, current_user: TokenPayload) -> list:
        """Filter list of items by role"""
        return [DataFilter.filter_for_role(item, current_user) for item in items]


class RolePermissions:
    """Define what each role can do"""
    
    PERMISSIONS = {
        UserRole.ADMIN: {
            "view_all": True,
            "edit_all": True,
            "delete_all": True,
            "manage_users": True,
            "verify_providers": True,
            "moderate_content": True,
            "publish_content": True,
            "view_analytics": True,
            "system_settings": True,
        },
        UserRole.GUIDE: {
            "create_profile": True,
            "edit_own_profile": True,
            "view_own_tours": True,
            "create_tours": True,
            "edit_own_tours": True,
            "delete_own_tours": True,
            "view_bookings": True,
            "view_reviews": True,
            "respond_to_reviews": True,
            "create_stories": True,
            "edit_own_stories": True,
        },
        UserRole.PROVIDER: {
            "create_profile": True,
            "edit_own_profile": True,
            "view_own_data": True,
            "create_services": True,
            "edit_own_services": True,
            "delete_own_services": True,
            "view_bookings": True,
            "view_reviews": True,
            "respond_to_reviews": True,
        },
        UserRole.TOURIST: {
            "view_all_content": True,
            "create_reviews": True,
            "create_stories": True,
            "create_bookings": True,
            "manage_own_bookings": True,
            "view_own_profile": True,
            "edit_own_profile": True,
            "edit_own_reviews": True,
            "edit_own_stories": True,
        },
        UserRole.MODERATOR: {
            "view_all_content": True,
            "moderate_reviews": True,
            "moderate_stories": True,
            "moderate_comments": True,
            "flag_inappropriate": True,
            "view_reports": True,
        }
    }
    
    @staticmethod
    def has_permission(user_role: UserRole, permission: str) -> bool:
        """Check if role has specific permission"""
        permissions = RolePermissions.PERMISSIONS.get(user_role, {})
        return permissions.get(permission, False)
    
    @staticmethod
    def can_perform_action(current_user: TokenPayload, action: str) -> bool:
        """Check if current user can perform action"""
        return RolePermissions.has_permission(current_user.role, action)


class OwnershipCheck:
    """Check if user owns resource"""
    
    @staticmethod
    def is_owner_or_admin(current_user: TokenPayload, owner_id: str) -> bool:
        """Check if user is owner or admin"""
        return current_user.sub == owner_id or current_user.role == UserRole.ADMIN
    
    @staticmethod
    def ensure_ownership(current_user: TokenPayload, owner_id: str, resource_name: str = "ressource"):
        """Raise HTTPException if not owner or admin"""
        if not OwnershipCheck.is_owner_or_admin(current_user, owner_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Vous ne pouvez modifier que vos propres {resource_name}"
            )
        return True
