"""
Firebase Authentication Routes

This module provides endpoints for Firebase-authenticated users.
These routes demonstrate how to protect endpoints using Firebase ID tokens.

To enable Firebase auth:
1. Install: pip install firebase-admin
2. Configure Firebase credentials in .env
3. Uncomment code in app/utils/firebase_auth.py
4. Call initialize_firebase() in main.py startup event
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.firebase_auth import verify_firebase_token
from config.database import get_db

router = APIRouter(
    prefix="/firebase",
    tags=["Firebase Authentication"]
)


@router.get(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify Firebase Token",
    description="Test endpoint to verify Firebase ID token"
)
async def verify_token(
    token_data: Dict[str, Any] = Depends(verify_firebase_token)
):
    """
    Verify Firebase authentication token.

    Requires Firebase ID token in Authorization header:
    Authorization: Bearer <firebase_id_token>

    Returns decoded token information including:
    - uid: Firebase user ID
    - email: User email
    - email_verified: Email verification status
    """
    return {
        "message": "Token is valid",
        "user_id": token_data.get("uid"),
        "email": token_data.get("email"),
        "email_verified": token_data.get("email_verified"),
    }


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    summary="Get Firebase User Profile",
    description="Get authenticated Firebase user profile"
)
async def get_profile(
    token_data: Dict[str, Any] = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Get Firebase user profile.

    This endpoint demonstrates how to:
    1. Verify Firebase token
    2. Access user information from token
    3. Optionally sync with local database

    You can extend this to:
    - Create/update local user record
    - Fetch additional user data from your database
    - Link Firebase UID with local user ID
    """
    return {
        "firebase_uid": token_data.get("uid"),
        "email": token_data.get("email"),
        "name": token_data.get("name"),
        "picture": token_data.get("picture"),
        "email_verified": token_data.get("email_verified"),
    }


@router.post(
    "/sync-user",
    status_code=status.HTTP_201_CREATED,
    summary="Sync Firebase User with Database",
    description="Create or update local user record from Firebase authentication"
)
async def sync_user(
    token_data: Dict[str, Any] = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_db)
):
    """
    Sync Firebase user with local database.

    This endpoint:
    1. Verifies Firebase token
    2. Checks if user exists in local database (by firebase_uid)
    3. Creates new user if not exists
    4. Updates existing user if found

    This is useful for maintaining a local copy of user data
    while using Firebase for authentication.

    Implementation example:
    ```python
    from app.repositories.UserRepository import UserRepository
    from app.models.User import User

    user_repo = UserRepository(db, User)
    firebase_uid = token_data.get("uid")

    # Check if user exists by firebase_uid
    # If not, create new user
    # If yes, update user information
    ```
    """
    firebase_uid = token_data.get("uid")
    email = token_data.get("email")
    name = token_data.get("name")

    # TODO: Implement user sync logic
    # 1. Add firebase_uid column to User model
    # 2. Check if user exists by firebase_uid
    # 3. Create or update user record

    return {
        "message": "User sync endpoint ready for implementation",
        "firebase_uid": firebase_uid,
        "email": email,
        "name": name,
        "note": "Add firebase_uid column to User model and implement sync logic"
    }
