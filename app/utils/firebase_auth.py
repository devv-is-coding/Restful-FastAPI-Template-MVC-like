"""
Firebase Authentication Integration Module

This module provides Firebase authentication functionality for the FastAPI application.
It handles Firebase Admin SDK initialization, token verification, and user management.

Usage:
    1. Install firebase-admin: pip install firebase-admin
    2. Add Firebase credentials to .env:
       - FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccountKey.json
       OR
       - FIREBASE_PROJECT_ID=your-project-id
       - FIREBASE_PRIVATE_KEY=your-private-key
       - FIREBASE_CLIENT_EMAIL=your-client-email
    3. Use verify_firebase_token() in dependencies for protected routes
"""

import os
import json
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Uncomment when firebase-admin is installed:
# import firebase_admin
# from firebase_admin import credentials, auth
# from firebase_admin.exceptions import FirebaseError

from config.settings import settings


# Global Firebase app instance
firebase_app = None
security = HTTPBearer()


def initialize_firebase():
    """
    Initialize Firebase Admin SDK.

    This function should be called once during application startup.
    It supports two initialization methods:
    1. Using a service account JSON file
    2. Using environment variables for credentials

    Add this to main.py startup event:
        @app.on_event("startup")
        async def startup_event():
            initialize_firebase()
    """
    global firebase_app

    # Uncomment when firebase-admin is installed:
    # if firebase_app is not None:
    #     return firebase_app

    # try:
    #     # Method 1: Initialize from service account file
    #     cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    #     if cred_path and os.path.exists(cred_path):
    #         cred = credentials.Certificate(cred_path)
    #         firebase_app = firebase_admin.initialize_app(cred)
    #         print("Firebase initialized from credentials file")
    #         return firebase_app
    #
    #     # Method 2: Initialize from environment variables
    #     project_id = os.getenv("FIREBASE_PROJECT_ID")
    #     private_key = os.getenv("FIREBASE_PRIVATE_KEY")
    #     client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
    #
    #     if project_id and private_key and client_email:
    #         cred_dict = {
    #             "type": "service_account",
    #             "project_id": project_id,
    #             "private_key": private_key.replace('\\n', '\n'),
    #             "client_email": client_email,
    #         }
    #         cred = credentials.Certificate(cred_dict)
    #         firebase_app = firebase_admin.initialize_app(cred)
    #         print("Firebase initialized from environment variables")
    #         return firebase_app
    #
    #     print("Warning: Firebase credentials not found. Firebase auth will not work.")
    #
    # except Exception as e:
    #     print(f"Error initializing Firebase: {e}")
    #     raise

    print("Firebase auth module ready (firebase-admin not installed)")
    return None


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify Firebase ID token from Authorization header.

    This function extracts and verifies the Firebase ID token from the
    Authorization Bearer token. It can be used as a FastAPI dependency
    for protected routes.

    Args:
        credentials: HTTP Authorization credentials (Bearer token)

    Returns:
        Dict containing decoded token claims with user information:
        - uid: Firebase user ID
        - email: User email
        - email_verified: Email verification status
        - name: User display name
        - picture: Profile picture URL
        - etc.

    Raises:
        HTTPException: 401 if token is invalid or expired

    Example:
        @router.get("/protected")
        async def protected_route(
            token_data: dict = Depends(verify_firebase_token)
        ):
            user_id = token_data['uid']
            return {"message": f"Hello {user_id}"}
    """

    # Uncomment when firebase-admin is installed:
    # try:
    #     token = credentials.credentials
    #
    #     # Verify the ID token
    #     decoded_token = auth.verify_id_token(token)
    #
    #     return decoded_token
    #
    # except auth.InvalidIdTokenError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication token",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # except auth.ExpiredIdTokenError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Authentication token has expired",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # except FirebaseError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail=f"Firebase authentication error: {str(e)}",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Internal server error during authentication: {str(e)}",
    #     )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Firebase authentication not yet configured. Install firebase-admin package.",
    )


async def get_firebase_user(uid: str) -> Optional[Dict[str, Any]]:
    """
    Get Firebase user by UID.

    Args:
        uid: Firebase user ID

    Returns:
        Dict containing user record information or None if not found

    Example:
        user = await get_firebase_user("firebase_uid_123")
        if user:
            print(f"User email: {user.email}")
    """

    # Uncomment when firebase-admin is installed:
    # try:
    #     user_record = auth.get_user(uid)
    #     return {
    #         "uid": user_record.uid,
    #         "email": user_record.email,
    #         "email_verified": user_record.email_verified,
    #         "display_name": user_record.display_name,
    #         "photo_url": user_record.photo_url,
    #         "disabled": user_record.disabled,
    #         "metadata": {
    #             "creation_timestamp": user_record.user_metadata.creation_timestamp,
    #             "last_sign_in_timestamp": user_record.user_metadata.last_sign_in_timestamp,
    #         }
    #     }
    # except auth.UserNotFoundError:
    #     return None
    # except FirebaseError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error fetching user: {str(e)}"
    #     )

    return None


async def create_firebase_custom_token(uid: str, claims: Optional[Dict] = None) -> str:
    """
    Create a custom Firebase token for a user.

    Useful for backend authentication where you want to sign in users
    programmatically without requiring their password.

    Args:
        uid: Firebase user ID
        claims: Optional custom claims to include in the token

    Returns:
        Custom token string

    Example:
        token = await create_firebase_custom_token(
            "user123",
            claims={"role": "admin"}
        )
    """

    # Uncomment when firebase-admin is installed:
    # try:
    #     custom_token = auth.create_custom_token(uid, claims)
    #     return custom_token.decode('utf-8')
    # except FirebaseError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error creating custom token: {str(e)}"
    #     )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Firebase authentication not yet configured"
    )


async def delete_firebase_user(uid: str) -> bool:
    """
    Delete a Firebase user account.

    Args:
        uid: Firebase user ID to delete

    Returns:
        True if deleted successfully

    Example:
        success = await delete_firebase_user("user123")
    """

    # Uncomment when firebase-admin is installed:
    # try:
    #     auth.delete_user(uid)
    #     return True
    # except auth.UserNotFoundError:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    # except FirebaseError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error deleting user: {str(e)}"
    #     )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Firebase authentication not yet configured"
    )
