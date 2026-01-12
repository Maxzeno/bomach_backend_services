"""
Auth Client for Services Backend

This module provides utilities for communicating with the main auth backend.

Configuration:
- Set AUTH_SERVICE_URL environment variable (default: http://localhost:8000)

Usage:
    from api.utils.auth_client import AuthClient, verify_request_token

    # Verify a JWT token
    client = AuthClient()
    is_valid, user_id = client.verify_token(token)

    # In an endpoint
    is_valid, user_id, error = verify_request_token(request)
"""

import requests
from typing import Tuple, Optional, Dict, Any
from django.conf import settings


class AuthClientError(Exception):
    """Exception raised when auth client operations fail."""
    pass


class AuthClient:
    """
    Client for communicating with the main auth backend service.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 10
    ):
        self.base_url = base_url or getattr(
            settings, 'AUTH_SERVICE_URL',
            'http://localhost:9000'
        )
        self.timeout = timeout
        self._session = None

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def verify_token(self, token: str) -> Tuple[bool, Optional[int]]:
        """
        Verify a JWT token with the auth service.

        Returns:
            Tuple of (is_valid, user_id)
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/auth/verify-token",
                headers={"Authorization": f"Bearer {token}"},
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                return True, data.get('user_id')
            return False, None

        except requests.RequestException:
            return False, None

    def get_current_user(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Get current user information from token."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return True, response.json(), "Success"
            elif response.status_code == 401:
                return False, None, "Invalid or expired token"
            else:
                return False, None, f"Error: {response.status_code}"

        except requests.RequestException as e:
            return False, None, f"Connection error: {str(e)}"

    def get_employee_info(self, employee_id: str, token: str) -> Optional[Dict[str, Any]]:
        """Get employee information by employee ID."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/employees/{employee_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            return None

        except requests.RequestException:
            return None

    def get_client_info(self, client_id: str, token: str) -> Optional[Dict[str, Any]]:
        """
        Get client information by client ID from the main backend.

        Note: Services backend should migrate to using this instead of
        its local Client model.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/clients/{client_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            return None

        except requests.RequestException:
            return None

    def validate_employee_id(self, employee_id: str, token: str) -> bool:
        """Check if an employee ID exists."""
        return self.get_employee_info(employee_id, token) is not None

    def validate_client_id(self, client_id: str, token: str) -> bool:
        """Check if a client ID exists in the main backend."""
        return self.get_client_info(client_id, token) is not None


# Singleton instance
_default_client: Optional[AuthClient] = None


def get_auth_client() -> AuthClient:
    """Get the default auth client instance."""
    global _default_client
    if _default_client is None:
        _default_client = AuthClient()
    return _default_client


def verify_request_token(request) -> Tuple[bool, Optional[int], str]:
    """
    Verify the token from a Django/Ninja request.

    Returns:
        Tuple of (is_valid, user_id, error_message)
    """
    auth_header = request.headers.get('Authorization', '')

    if not auth_header:
        return False, None, "No authorization header"

    if not auth_header.startswith('Bearer '):
        return False, None, "Invalid authorization header format"

    token = auth_header[7:]
    client = get_auth_client()
    is_valid, user_id = client.verify_token(token)

    if not is_valid:
        return False, None, "Invalid or expired token"

    return True, user_id, ""


def get_request_user(request) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Get user information from request token."""
    auth_header = request.headers.get('Authorization', '')

    if not auth_header or not auth_header.startswith('Bearer '):
        return False, None, "Invalid authorization"

    token = auth_header[7:]
    client = get_auth_client()
    return client.get_current_user(token)
